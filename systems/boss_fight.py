######################載入套件######################
import pygame
import random
from config import *
from entities import Player, Bullet

######################Boss Fight 系統類別######################
class BossFightSystem:
    """
    Boss Fight 系統類別 - 負責管理 8 個連續的 Boss 戰鬥\n
    \n
    功能包括:\n
    1. 8 個 Boss 的順序管理\n
    2. 玩家治療藥水系統（每場戰鬥 3 次）\n
    3. Boss 戰鬥狀態追蹤\n
    4. 勝利/失敗條件檢查\n
    5. UI 繪製和進度顯示\n
    """
    
    def __init__(self, player_name):
        """
        初始化 Boss Fight 系統\n
        \n
        參數:\n
        player_name (str): 玩家名稱\n
        """
        # 玩家資訊
        self.player_name = player_name
        
        # 初始化玩家物件
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80)
        
        # 隨機選擇太空船類型
        self._assign_random_spaceship()
        
        # 設置玩家生命值
        self.player.health = BOSS_FIGHT_SETTINGS["player_health"]
        
        # 治療藥水系統
        self.health_potions = BOSS_FIGHT_SETTINGS["health_potion_count"]
        self.potion_heal_amount = BOSS_FIGHT_SETTINGS["health_potion_heal"]
        
        # Boss 戰鬥狀態
        self.current_boss_index = 1  # 從第一個 Boss 開始
        self.current_boss = None
        self.boss_spawn_timer = 0
        
        # 遊戲物件列表
        self.player_bullets = []
        self.boss_bullets = []
        
        # 遊戲狀態
        self.game_state = "preparing"  # preparing, fighting, boss_defeated, victory, defeat
        self.state_timer = 0
        self.total_score = 0
        
        # 初始化字體
        pygame.font.init()
        self.title_font = create_font(BOSS_FIGHT_UI["boss_name_font_size"])
        self.info_font = create_font(BOSS_FIGHT_UI["progress_font_size"])
        
        print(f"Boss Fight 系統初始化完成，玩家：{self.player_name}")
        self._spawn_next_boss()
    
    def _assign_random_spaceship(self):
        """
        隨機分配一艘太空船給玩家\n
        """
        # 所有可用的太空船類型
        available_ships = list(SPACESHIP_STATS.keys())
        
        # 添加調試信息
        print(f"可用太空船：{available_ships}")
        
        # 隨機選擇一艘太空船
        selected_ship = random.choice(available_ships)
        
        # 設置玩家的太空船類型
        self.player.spaceship_type = selected_ship
        self.player.unlocked_ships = [selected_ship]  # 確保這艘船是已解鎖的
        
        # 更新太空船屬性
        self.player.update_ship_stats()
        
        # 根據太空船類型調整初始生命值
        ship_stats = SPACESHIP_STATS[selected_ship]
        self.player.health = ship_stats["max_health"]
        self.player.max_health = ship_stats["max_health"]
        
        print(f"隨機分配太空船：{selected_ship.title()}")
        print(f"太空船屬性 - 生命值：{self.player.max_health}, 速度：{self.player.speed}")
        
        # 顯示太空船的獨特特色
        ship_descriptions = {
            "explorer": "探索者 - 平衡型太空船",
            "fighter": "戰鬥機 - 攻守兼備",
            "interceptor": "攔截機 - 高速輕型",
            "destroyer": "驅逐艦 - 重裝甲高血量",
            "battleship": "戰列艦 - 最強火力"
        }
        
        if selected_ship in ship_descriptions:
            print(f"特色：{ship_descriptions[selected_ship]}")
    
    def _spawn_next_boss(self):
        """
        生成下一個 Boss\n
        """
        if self.current_boss_index > BOSS_FIGHT_SETTINGS["total_bosses"]:
            # 所有 Boss 都已擊敗
            self.game_state = "victory"
            self.state_timer = BOSS_FIGHT_SETTINGS["victory_display_time"]
            print("恭喜！你已經擊敗了所有 Boss！")
            return
        
        # 從配置中載入 Boss 屬性
        boss_config = BOSS_FIGHT_BOSSES[self.current_boss_index]
        
        # 延遲導入 BossFightBoss 類別避免循環導入
        from entities.boss_fight_boss import BossFightBoss
        
        # 創建新 Boss
        boss_x = SCREEN_WIDTH // 2 - boss_config["width"] // 2
        boss_y = 50
        self.current_boss = BossFightBoss(boss_x, boss_y, self.current_boss_index)
        
        # 設置狀態
        self.game_state = "preparing"
        self.boss_spawn_timer = BOSS_FIGHT_SETTINGS["boss_spawn_delay"]
        
        print(f"生成第 {self.current_boss_index} 個 Boss：{boss_config['name']}")
    
    def update(self, keys):
        """
        更新 Boss Fight 系統狀態\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        \n
        回傳:\n
        str: 遊戲結果 ("victory", "defeat", "quit", None)\n
        """
        # 檢查退出按鍵
        if keys[pygame.K_q]:
            print("玩家按下 Q 鍵退出 Boss Fight 模式")
            return "quit"
        
        # 根據遊戲狀態更新
        if self.game_state == "preparing":
            return self._update_preparing()
        elif self.game_state == "fighting":
            return self._update_fighting(keys)
        elif self.game_state == "boss_defeated":
            return self._update_boss_defeated()
        elif self.game_state == "victory":
            return self._update_victory()
        elif self.game_state == "defeat":
            return self._update_defeat()
        
        return None
    
    def _update_preparing(self):
        """
        更新準備階段（Boss 生成延遲）\n
        """
        self.boss_spawn_timer -= 1
        if self.boss_spawn_timer <= 0:
            self.game_state = "fighting"
            print(f"開始與第 {self.current_boss_index} 個 Boss 戰鬥！")
        
        return None
    
    def _update_fighting(self, keys):
        """
        更新戰鬥階段\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        """
        # 更新玩家
        self._update_player(keys)
        
        # 更新 Boss
        if self.current_boss:
            self._update_boss()
        
        # 更新子彈
        self._update_bullets()
        
        # 碰撞檢測
        self._handle_collisions()
        
        # 檢查戰鬥結果
        if self.player.health <= 0:
            self.game_state = "defeat"
            self.state_timer = BOSS_FIGHT_SETTINGS["defeat_display_time"]
            print("玩家被 Boss 擊敗！")
            return None
        
        if self.current_boss and self.current_boss.health <= 0:
            self._boss_defeated()
            return None
        
        return None
    
    def _update_player(self, keys):
        """
        更新玩家狀態\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        """
        # 玩家移動（WASD）
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.y = max(0, self.player.y - self.player.speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.y = min(SCREEN_HEIGHT - self.player.height, self.player.y + self.player.speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.x = max(0, self.player.x - self.player.speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.x = min(SCREEN_WIDTH - self.player.width, self.player.x + self.player.speed)
        
        # 射擊（Space）
        if keys[pygame.K_SPACE]:
            new_bullet = self.player.shoot()
            if new_bullet:
                self.player_bullets.append(new_bullet)
        
        # 特殊攻擊（X）
        if keys[pygame.K_x]:
            special_bullets = self.player.special_attack()
            self.player_bullets.extend(special_bullets)
        
        # 使用治療藥水（E）
        if keys[pygame.K_e]:
            self._use_health_potion()
        
        # 更新玩家內部狀態
        self.player.update()
    
    def _update_boss(self):
        """
        更新 Boss 狀態\n
        """
        if not self.current_boss:
            return
        
        # 移動 Boss
        self.current_boss.move()
        
        # 更新 Boss 並獲取新產生的子彈
        new_boss_bullets = self.current_boss.update()
        self.boss_bullets.extend(new_boss_bullets)
    
    def _update_bullets(self):
        """
        更新所有子彈\n
        """
        # 更新玩家子彈
        for bullet in self.player_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
        
        # 更新 Boss 子彈
        for bullet in self.boss_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.boss_bullets.remove(bullet)
    
    def _handle_collisions(self):
        """
        處理所有碰撞檢測\n
        """
        from systems.collision import check_collision
        
        # 玩家子彈打中 Boss
        for bullet in self.player_bullets[:]:
            if self.current_boss:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 self.current_boss.x, self.current_boss.y, 
                                 self.current_boss.width, self.current_boss.height):
                    # 造成傷害
                    self.current_boss.take_damage(bullet.damage)
                    self.player_bullets.remove(bullet)
        
        # Boss 子彈打中玩家
        for bullet in self.boss_bullets[:]:
            if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                             self.player.x, self.player.y, self.player.width, self.player.height):
                # 造成傷害
                self.player.health -= bullet.damage
                self.boss_bullets.remove(bullet)
        
        # 玩家撞到 Boss
        if self.current_boss:
            if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                             self.current_boss.x, self.current_boss.y, 
                             self.current_boss.width, self.current_boss.height):
                # 嚴重傷害
                self.player.health -= 30
    
    def _use_health_potion(self):
        """
        使用治療藥水\n
        """
        if self.health_potions > 0 and self.player.health < self.player.max_health:
            # 使用藥水
            self.health_potions -= 1
            old_health = self.player.health
            self.player.health = min(self.player.max_health, 
                                   self.player.health + self.potion_heal_amount)
            
            healed = self.player.health - old_health
            print(f"使用治療藥水，回復 {healed} 生命值，剩餘藥水：{self.health_potions}")
    
    def _boss_defeated(self):
        """
        Boss 被擊敗的處理\n
        """
        if not self.current_boss:
            return
        
        # 獲得分數
        boss_config = BOSS_FIGHT_BOSSES[self.current_boss_index]
        self.total_score += boss_config["score"]
        
        # 隨機獲得治療藥水
        if random.randint(1, 100) <= BOSS_FIGHT_POTIONS["random_drop_chance"]:
            self.health_potions = min(BOSS_FIGHT_POTIONS["max_potions"], 
                                    self.health_potions + 1)
            print("擊敗 Boss 獲得額外治療藥水！")
        
        print(f"擊敗第 {self.current_boss_index} 個 Boss！獲得 {boss_config['score']} 分")
        
        # 清除 Boss 和子彈
        self.current_boss = None
        self.boss_bullets.clear()
        
        # 前進到下一個 Boss
        self.current_boss_index += 1
        self.game_state = "boss_defeated"
        self.state_timer = 120  # 2秒間隔
    
    def _update_boss_defeated(self):
        """
        更新 Boss 被擊敗階段\n
        """
        self.state_timer -= 1
        if self.state_timer <= 0:
            self._spawn_next_boss()
        
        return None
    
    def _update_victory(self):
        """
        更新勝利階段\n
        """
        self.state_timer -= 1
        if self.state_timer <= 0:
            return "victory"
        
        return None
    
    def _update_defeat(self):
        """
        更新失敗階段\n
        """
        self.state_timer -= 1
        if self.state_timer <= 0:
            return "defeat"
        
        return None
    
    def draw(self, screen):
        """
        繪製 Boss Fight 畫面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 清空螢幕
        screen.fill(BLACK)
        
        # 繪製標題
        self._draw_title(screen)
        
        # 根據遊戲狀態繪製內容
        if self.game_state == "preparing":
            self._draw_preparing(screen)
        elif self.game_state == "fighting":
            self._draw_fighting(screen)
        elif self.game_state == "boss_defeated":
            self._draw_boss_defeated(screen)
        elif self.game_state == "victory":
            self._draw_victory(screen)
        elif self.game_state == "defeat":
            self._draw_defeat(screen)
    
    def _draw_title(self, screen):
        """
        繪製 Boss Fight 標題\n
        """
        title_text = self.title_font.render("Boss Fight", True, ORANGE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(title_text, title_rect)
    
    def _draw_preparing(self, screen):
        """
        繪製準備階段\n
        """
        if self.current_boss_index <= BOSS_FIGHT_SETTINGS["total_bosses"]:
            boss_config = BOSS_FIGHT_BOSSES[self.current_boss_index]
            prepare_text = self.info_font.render(f"準備迎戰：{boss_config['name']}", True, YELLOW)
            prepare_rect = prepare_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(prepare_text, prepare_rect)
            
            # 顯示分配的太空船
            ship_text = self.info_font.render(f"你的太空船：{self.player.spaceship_type.title()}", True, CYAN)
            ship_rect = ship_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(ship_text, ship_rect)
            
            # 顯示太空船屬性
            stats_text = self.info_font.render(f"生命值：{self.player.max_health} | 速度：{self.player.speed}", True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(stats_text, stats_rect)
            
            countdown = self.boss_spawn_timer // 60 + 1
            countdown_text = self.title_font.render(str(countdown), True, RED)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(countdown_text, countdown_rect)
    
    def _draw_fighting(self, screen):
        """
        繪製戰鬥階段\n
        """
        # 繪製玩家
        self.player.draw(screen)
        
        # 繪製玩家子彈
        for bullet in self.player_bullets:
            bullet.draw(screen)
        
        # 繪製 Boss
        if self.current_boss:
            self.current_boss.draw(screen)
            self.current_boss.draw_health_bar(screen)
        
        # 繪製 Boss 子彈
        for bullet in self.boss_bullets:
            bullet.draw(screen)
        
        # 繪製 UI
        self._draw_ui(screen)
    
    def _draw_boss_defeated(self, screen):
        """
        繪製 Boss 被擊敗階段\n
        """
        # 繪製玩家
        self.player.draw(screen)
        
        # 顯示勝利訊息
        victory_text = self.title_font.render("Boss 擊敗！", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(victory_text, victory_rect)
        
        # 繪製 UI
        self._draw_ui(screen)
    
    def _draw_victory(self, screen):
        """
        繪製勝利畫面\n
        """
        # 勝利訊息
        victory_text = self.title_font.render("恭喜！你已經擊敗了所有 Boss！", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(victory_text, victory_rect)
        
        # 最終分數
        score_text = self.info_font.render(f"最終分數：{self.total_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        # 返回提示
        return_text = self.info_font.render("即將返回主選單...", True, CYAN)
        return_rect = return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(return_text, return_rect)
    
    def _draw_defeat(self, screen):
        """
        繪製失敗畫面\n
        """
        # 失敗訊息
        defeat_text = self.title_font.render("遊戲結束，你被 Boss 擊敗了", True, RED)
        defeat_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(defeat_text, defeat_rect)
        
        # 最終分數
        score_text = self.info_font.render(f"最終分數：{self.total_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        # 返回提示
        return_text = self.info_font.render("即將返回主選單...", True, CYAN)
        return_rect = return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(return_text, return_rect)
    
    def _draw_ui(self, screen):
        """
        繪製遊戲 UI\n
        """
        # 玩家生命值條
        self._draw_player_health_bar(screen)
        
        # 治療藥水計數器
        self._draw_potion_counter(screen)
        
        # Boss 進度
        self._draw_boss_progress(screen)
        
        # 分數
        score_text = self.info_font.render(f"分數：{self.total_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # 太空船類型
        ship_text = self.info_font.render(f"太空船：{self.player.spaceship_type.title()}", True, CYAN)
        screen.blit(ship_text, (10, 35))
        
        # 操作提示
        controls_text = self.info_font.render("WASD:移動 Space:射擊 X:特攻 E:治療 Q:退出", True, WHITE)
        screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
    
    def _draw_player_health_bar(self, screen):
        """
        繪製玩家生命值條\n
        """
        bar_x = BOSS_FIGHT_UI["player_health_bar_x"]
        bar_y = BOSS_FIGHT_UI["player_health_bar_y"]
        bar_width = BOSS_FIGHT_UI["player_health_bar_width"]
        bar_height = BOSS_FIGHT_UI["player_health_bar_height"]
        
        # 背景
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # 生命值
        health_percentage = max(0, self.player.health / self.player.max_health)
        health_width = int(bar_width * health_percentage)
        
        if health_percentage > 0.6:
            health_color = GREEN
        elif health_percentage > 0.3:
            health_color = YELLOW
        else:
            health_color = RED
        
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # 邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 文字
        health_text = self.info_font.render(f"生命值：{self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (bar_x, bar_y - 25))
    
    def _draw_potion_counter(self, screen):
        """
        繪製治療藥水計數器\n
        """
        potion_x = BOSS_FIGHT_UI["potion_counter_x"]
        potion_y = BOSS_FIGHT_UI["potion_counter_y"]
        
        potion_text = self.info_font.render(f"治療藥水：{self.health_potions}", True, GREEN)
        screen.blit(potion_text, (potion_x, potion_y - 25))
        
        # 繪製藥水圖示
        potion_size = BOSS_FIGHT_POTIONS["potion_size"]
        for i in range(self.health_potions):
            potion_rect = pygame.Rect(potion_x + i * (potion_size + 5), potion_y, potion_size, potion_size)
            pygame.draw.rect(screen, BOSS_FIGHT_POTIONS["potion_color"], potion_rect)
            pygame.draw.rect(screen, WHITE, potion_rect, 1)
    
    def _draw_boss_progress(self, screen):
        """
        繪製 Boss 進度\n
        """
        progress_text = self.info_font.render(
            f"Boss 進度：{self.current_boss_index}/{BOSS_FIGHT_SETTINGS['total_bosses']}", 
            True, ORANGE
        )
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(progress_text, progress_rect)
        
        if self.current_boss_index <= BOSS_FIGHT_SETTINGS["total_bosses"]:
            boss_config = BOSS_FIGHT_BOSSES[self.current_boss_index]
            boss_name_text = self.info_font.render(boss_config["name"], True, YELLOW)
            boss_name_rect = boss_name_text.get_rect(center=(SCREEN_WIDTH // 2, 85))
            screen.blit(boss_name_text, boss_name_rect)