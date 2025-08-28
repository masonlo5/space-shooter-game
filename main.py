######################載入套件######################
import pygame
import sys
import random

# 匯入遊戲設定
from config import *

# 匯入遊戲物件
from entities import Player, Enemy, Boss, Bullet, PowerUp, Firework

# 匯入遊戲系統
from systems import check_collision, UISystem, ShopSystem, MenuSystem, ShipBattleSystem, VisualEffectsSystem, HideSeekSystem

######################遊戲狀態常數######################
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_BOSS_FIGHT = "boss_fight"
GAME_STATE_BOSS_FIGHT_MODE = "boss_fight_mode"
GAME_STATE_VICTORY = "victory"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_SHIP_BATTLE = "ship_battle"
GAME_STATE_HIDE_SEEK = "hide_seek"

######################全域變數######################
score = 0
stars = 0
boss_killed = False
victory_timer = 0
enemies_killed = 0  # 新增：擊殺敵人計數器

######################遊戲主控制類別######################
class GameController:
    """
    遊戲主控制器 - 負責管理整個遊戲的流程和狀態\n
    \n
    負責處理:\n
    1. 遊戲初始化\n
    2. 遊戲狀態管理（主畫面、遊戲中、Boss戰、勝利等）\n
    3. 主遊戲迴圈\n
    4. 事件處理\n
    5. 遊戲物件管理\n
    6. 碰撞檢測協調\n
    7. Boss戰觸發和管理\n
    """
    
    def __init__(self):
        """
        初始化遊戲控制器\n
        """
        # 初始化 Pygame
        pygame.init()
        
        # 建立遊戲視窗
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Galaxy Blaster - Space Shooter")
        
        # 設定遊戲時鐘
        self.clock = pygame.time.Clock()
        
        # 初始化遊戲系統
        self.ui_system = UISystem()
        self.shop_system = ShopSystem()
        self.menu_system = MenuSystem()
        self.ship_battle_system = ShipBattleSystem()
        self.visual_effects_system = VisualEffectsSystem()
        self.hide_seek_system = None  # 躲貓貓系統（按需創建）
        self.boss_fight_system = None  # Boss Fight系統（按需創建）
        
        # 遊戲狀態管理
        self.game_state = GAME_STATE_MENU
        self.running = True
        
        # 初始化遊戲變數
        self.reset_game()
    
    def reset_game(self):
        """
        重置遊戲到初始狀態\n
        """
        global score, stars, boss_killed, victory_timer, enemies_killed
        
        # 初始化遊戲物件
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.fireworks = []
        self.boss = None
        self.boss_bullets = []  # Boss攻擊子彈
        
        # 遊戲狀態
        self.shop_open = False
        self.enemy_spawn_timer = 0
        
        # 重置全域變數
        score = 0
        stars = 0
        boss_killed = False
        victory_timer = 0
        enemies_killed = 0
    
    def start_ship_battle(self):
        """
        開始 Ship Battle 模式\n
        """
        print("開始 Ship Battle 模式")
        
        # 建立玩家物件
        player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80)
        player_name = self.menu_system.get_player_name()
        
        # 開始戰鬥
        self.ship_battle_system.start_battle(player, player_name)
        
        # 切換到 Ship Battle 狀態
        self.game_state = GAME_STATE_SHIP_BATTLE
    
    def start_hide_seek(self):
        """
        開始躲貓貓遊戲\n
        """
        print("開始躲貓貓遊戲")
        
        # 創建躲貓貓遊戲系統
        player_name = self.menu_system.get_player_name()
        self.hide_seek_system = HideSeekSystem(player_name)
        
        # 切換到躲貓貓狀態
        self.game_state = GAME_STATE_HIDE_SEEK
    
    def start_boss_fight_mode(self):
        """
        開始 Boss Fight 模式\n
        """
        print("開始 Boss Fight 模式")
        
        # 直接從 systems 導入
        from systems import BossFightSystem
        
        # 創建 Boss Fight 系統
        player_name = self.menu_system.get_player_name()
        self.boss_fight_system = BossFightSystem(player_name)
        
        # 切換到 Boss Fight 狀態
        self.game_state = GAME_STATE_BOSS_FIGHT_MODE
    
    def handle_events(self):
        """
        處理遊戲事件\n
        """
        global stars
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GAME_STATE_MENU:
                    # 主畫面點擊處理
                    if event.button == 1:  # 左鍵點擊
                        action = self.menu_system.handle_click(event.pos)
                        if action == "start_game":
                            self.game_state = GAME_STATE_PLAYING
                            self.reset_game()
                        elif action == "ship_battle":
                            self.start_ship_battle()
                        elif action == "hide_seek":
                            self.start_hide_seek()
                        elif action == "boss_fight":
                            self.start_boss_fight_mode()
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == GAME_STATE_MENU:
                    # 如果正在編輯名稱，先處理文字輸入
                    if self.menu_system.is_editing_name:
                        self.menu_system.handle_text_input(event)
                    else:
                        # 主畫面按鍵處理
                        action = self.menu_system.handle_key_press(event.key)
                        if action == "start_game":
                            self.game_state = GAME_STATE_PLAYING
                            self.reset_game()
                        elif action == "ship_battle":
                            self.start_ship_battle()
                        elif action == "hide_seek":
                            self.start_hide_seek()
                        elif action == "boss_fight":
                            self.start_boss_fight_mode()
                
                elif self.game_state == GAME_STATE_SHIP_BATTLE:
                    # Ship Battle 模式不需要特殊按鍵處理，所有邏輯在 update 中
                    pass
                
                elif self.game_state == GAME_STATE_HIDE_SEEK:
                    # 躲貓貓模式的按鍵處理
                    if self.hide_seek_system:
                        result = self.hide_seek_system.handle_key_press(event.key)
                        if result == "return_to_menu":
                            self.game_state = GAME_STATE_MENU
                            self.hide_seek_system = None
                
                elif self.game_state in [GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT]:
                    if self.shop_open:
                        # 商店開啟時的按鍵處理
                        if event.key == pygame.K_ESCAPE:
                            self.shop_open = False
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                         pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                            stars = self.shop_system.handle_purchase(event.key, self.player, stars)
                    else:
                        # 遊戲中的按鍵處理
                        if event.key == pygame.K_SPACE:
                            # 按下空白鍵切換武器
                            self.player.change_weapon()
                        elif event.key == pygame.K_s and stars >= SHOP_UNLOCK_STARS:
                            # 按下 S 鍵開啟商店（需要 40 顆星星）
                            self.shop_open = True
                        elif event.key == pygame.K_c:
                            # 按下 C 鍵切換太空船
                            self.player.change_spaceship()
                        elif event.key == pygame.K_x:
                            # 按下 X 鍵發動特殊攻擊
                            special_bullets = self.player.special_attack()
                            self.bullets.extend(special_bullets)
                
                elif self.game_state in [GAME_STATE_VICTORY, GAME_STATE_GAME_OVER]:
                    # 勝利或遊戲結束時的按鍵處理
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.game_state = GAME_STATE_MENU
                    elif event.key == pygame.K_r:
                        # 按 R 重新開始
                        self.game_state = GAME_STATE_PLAYING
                        self.reset_game()
            
            # 處理文字輸入事件（用於玩家命名）
            elif event.type == pygame.TEXTINPUT:
                if self.game_state == GAME_STATE_MENU:
                    self.menu_system.handle_text_input(event)
    
    def update_game_objects(self):
        """
        更新所有遊戲物件的狀態\n
        """
        global score, stars, boss_killed, victory_timer, enemies_killed
        
        # Ship Battle 模式的更新邏輯
        if self.game_state == GAME_STATE_SHIP_BATTLE:
            keys = pygame.key.get_pressed()
            battle_result = self.ship_battle_system.update(keys)
            
            # 更新視覺效果
            self.visual_effects_system.update()
            
            if battle_result == "victory":
                print("Ship Battle 玩家獲勝！")
                self.visual_effects_system.start_victory_effect()
            elif battle_result == "defeat":
                print("Ship Battle 玩家失敗！")
                self.visual_effects_system.start_defeat_effect()
            elif battle_result in ["end", "quit"]:
                print("Ship Battle 結束，返回主選單")
                self.visual_effects_system.stop_effects()
                self.ship_battle_system.reset()
                self.game_state = GAME_STATE_MENU
            
            return  # Ship Battle 模式不執行下面的邏輯
        
        # 躲貓貓模式的更新邏輯
        if self.game_state == GAME_STATE_HIDE_SEEK:
            if self.hide_seek_system:
                keys = pygame.key.get_pressed()
                result = self.hide_seek_system.update(keys)
                
                if result == "return_to_menu":
                    print("躲貓貓遊戲結束，返回主選單")
                    self.hide_seek_system = None
                    self.game_state = GAME_STATE_MENU
            
            return  # 躲貓貓模式不執行下面的邏輯
        
        # Boss Fight 模式的更新邏輯
        if self.game_state == GAME_STATE_BOSS_FIGHT_MODE:
            if self.boss_fight_system:
                keys = pygame.key.get_pressed()
                result = self.boss_fight_system.update(keys)
                
                if result == "victory":
                    print("Boss Fight 模式完成，恭喜擊敗所有Boss！")
                    self.boss_fight_system = None
                    self.game_state = GAME_STATE_MENU
                elif result == "defeat":
                    print("Boss Fight 模式失敗，被Boss擊敗")
                    self.boss_fight_system = None
                    self.game_state = GAME_STATE_MENU
                elif result == "quit":
                    print("退出 Boss Fight 模式")
                    self.boss_fight_system = None
                    self.game_state = GAME_STATE_MENU
            
            return  # Boss Fight 模式不執行下面的邏輯
        
        # 只有在一般遊戲狀態才更新遊戲邏輯
        if self.game_state not in [GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT]:
            return
        
        # 取得按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 只有在商店關閉時才更新遊戲邏輯
        if not self.shop_open:
            # 更新玩家
            self.player.move(keys)
            self.player.update()
            
            # 射擊控制（按住 Ctrl 或 Shift 鍵射擊）
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                new_bullet = self.player.shoot()
                if new_bullet:
                    self.bullets.append(new_bullet)
            
            # 更新所有子彈
            for bullet in self.bullets[:]:  # 用切片複製清單，避免修改時出錯
                bullet.move()
                # 移除飛出螢幕的子彈
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)
            
            # 更新Boss子彈
            for boss_bullet in self.boss_bullets[:]:
                boss_bullet.move()
                if boss_bullet.is_off_screen():
                    self.boss_bullets.remove(boss_bullet)
            
            # 根據遊戲狀態更新敵人或Boss
            if self.game_state == GAME_STATE_PLAYING:
                # 普通遊戲狀態：生成和更新敵人
                self.spawn_enemies()
                self.update_enemies()
                
                # 檢查是否達到Boss戰條件
                if enemies_killed >= BOSS_TRIGGER_KILLS and not self.boss:
                    self.trigger_boss_fight()
            
            elif self.game_state == GAME_STATE_BOSS_FIGHT:
                # Boss戰狀態：更新Boss
                self.update_boss()
            
            # 碰撞檢測
            self.handle_collisions()
            
            # 更新所有道具
            for powerup in self.powerups[:]:
                powerup.move()
                # 移除離開螢幕的道具
                if powerup.is_off_screen():
                    self.powerups.remove(powerup)
            
            # 碰撞檢測：玩家撿到道具
            for powerup in self.powerups[:]:
                if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                                 powerup.x, powerup.y, powerup.width, powerup.height):
                    # 套用道具效果
                    is_fatal, stars_gained, should_return_to_menu = powerup.apply_effect(self.player)
                    stars += stars_gained
                    
                    if is_fatal:
                        print(f"踩到炸彈！遊戲結束！最終分數：{score}，星星數量：{stars}")
                        self.game_state = GAME_STATE_GAME_OVER
                    elif should_return_to_menu:
                        # Boss掉落的禮物：返回主畫面
                        print(f"獲得Boss禮物！最終分數：{score}，星星數量：{stars}")
                        self.game_state = GAME_STATE_MENU
                    
                    self.powerups.remove(powerup)
        
        # 更新煙火效果
        for firework in self.fireworks[:]:
            firework.update()
            if firework.is_dead():
                self.fireworks.remove(firework)
        
        # 勝利條件檢查
        if boss_killed:
            victory_timer -= 1
            if victory_timer <= 0:
                print(f"Victory! Boss 擊敗！最終分數：{score}，星星數量：{stars}")
                self.game_state = GAME_STATE_VICTORY
    
    def trigger_boss_fight(self):
        """
        觸發Boss戰\n
        """
        print(f"Boss 出現！已擊敗 {enemies_killed} 個敵人")
        
        # 清除所有現有敵人
        self.enemies.clear()
        
        # 創建Boss
        boss_x = SCREEN_WIDTH // 2 - 40  # Boss較大，所以調整位置
        boss_y = 50
        self.boss = Boss(boss_x, boss_y)
        
        # 切換到Boss戰狀態
        self.game_state = GAME_STATE_BOSS_FIGHT
    
    def update_boss(self):
        """
        更新Boss狀態\n
        """
        if self.boss:
            # 移動Boss
            self.boss.move()
            
            # 更新Boss並獲取新產生的子彈
            new_boss_bullets = self.boss.update()
            self.boss_bullets.extend(new_boss_bullets)
    
    def spawn_enemies(self):
        """
        生成敵人的邏輯（只在普通遊戲狀態）\n
        """
        global score
        
        self.enemy_spawn_timer += 1
        enemy_spawn_delay = ENEMY_SPAWN_DELAY
        
        if self.enemy_spawn_timer >= enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            # 隨機選擇敵人類型和位置
            enemy_type = random.choice(["basic", "basic", "fast"])  # 增加基本敵人的比例
            enemy_x = random.randint(0, SCREEN_WIDTH - 30)
            self.enemies.append(Enemy(enemy_x, -30, enemy_type))
            
            # 隨著分數增加，敵人生成速度加快
            if score > 100:
                enemy_spawn_delay = max(30, 60 - score // 50)  # 最快每 0.5 秒生成一個
    
    def update_enemies(self):
        """
        更新所有敵人\n
        """
        for enemy in self.enemies[:]:
            enemy.move()
            # 移除離開螢幕的敵人
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
    
    def handle_collisions(self):
        """
        處理所有碰撞檢測\n
        """
        global score, stars, boss_killed, victory_timer, enemies_killed
        
        # 碰撞檢測：玩家子彈打中敵人
        for bullet in self.bullets[:]:
            hit_target = False
            
            # 檢查子彈是否打中普通敵人
            for enemy in self.enemies[:]:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 enemy.x, enemy.y, enemy.width, enemy.height):
                    # 子彈打中敵人
                    if enemy.take_damage(bullet.damage):
                        # 敵人死亡，隨機掉落道具
                        self.drop_powerups(enemy)
                        
                        self.enemies.remove(enemy)
                        score += enemy.score_value
                        stars += enemy.star_value
                        enemies_killed += 1  # 增加擊殺計數
                    
                    self.bullets.remove(bullet)
                    hit_target = True
                    break
            
            # 檢查子彈是否打中Boss
            if not hit_target and self.boss:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 self.boss.x, self.boss.y, self.boss.width, self.boss.height):
                    # 子彈打中Boss
                    if self.boss.take_damage(bullet.damage):
                        # Boss被擊敗
                        boss_killed = True
                        victory_timer = 180  # 3 秒勝利畫面
                        
                        # 生成Boss禮物
                        gift = self.boss.drop_gift()
                        self.powerups.append(gift)
                        
                        # 生成慶祝煙火
                        for _ in range(8):
                            firework_x = random.randint(100, SCREEN_WIDTH - 100)
                            firework_y = random.randint(100, SCREEN_HEIGHT - 100)
                            self.fireworks.append(Firework(firework_x, firework_y))
                        
                        # 獲得分數和星星
                        score += self.boss.score_value
                        stars += self.boss.star_value
                        
                        # 移除Boss
                        self.boss = None
                        # 清除Boss子彈
                        self.boss_bullets.clear()
                    
                    self.bullets.remove(bullet)
                    hit_target = True
        
        # 碰撞檢測：Boss子彈打中玩家
        for boss_bullet in self.boss_bullets[:]:
            if check_collision(boss_bullet.x, boss_bullet.y, boss_bullet.width, boss_bullet.height,
                             self.player.x, self.player.y, self.player.width, self.player.height):
                # Boss子彈打中玩家
                self.player.health -= boss_bullet.damage
                self.boss_bullets.remove(boss_bullet)
                
                # 檢查遊戲是否結束
                if self.player.health <= 0:
                    print(f"被Boss擊敗！最終分數：{score}，星星數量：{stars}")
                    self.game_state = GAME_STATE_GAME_OVER
        
        # 碰撞檢測：玩家撞到敵人
        for enemy in self.enemies[:]:
            if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                             enemy.x, enemy.y, enemy.width, enemy.height):
                # 玩家撞到敵人，減少生命值
                self.player.health -= 20
                self.enemies.remove(enemy)
                
                # 檢查遊戲是否結束
                if self.player.health <= 0:
                    print(f"遊戲結束！最終分數：{score}，星星數量：{stars}")
                    self.game_state = GAME_STATE_GAME_OVER
        
        # 碰撞檢測：玩家撞到Boss
        if self.boss:
            if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                             self.boss.x, self.boss.y, self.boss.width, self.boss.height):
                # 玩家撞到Boss，嚴重傷害
                self.player.health -= 50
                
                # 檢查遊戲是否結束
                if self.player.health <= 0:
                    print(f"撞到Boss！遊戲結束！最終分數：{score}，星星數量：{stars}")
                    self.game_state = GAME_STATE_GAME_OVER
    
    def drop_powerups(self, enemy):
        """
        敵人死亡時掉落道具的邏輯\n
        \n
        參數:\n
        enemy (Enemy): 死亡的敵人物件\n
        """
        drop_chance = random.randint(1, 100)
        if drop_chance <= POWERUP_DROP_CHANCE:  # 30% 機率掉落道具
            if drop_chance <= STAR_DROP_CHANCE:  # 15% 機率掉星星
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "star"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE:  # 5% 機率掉回血藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "health_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE:  # 5% 機率掉加速藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "speed_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE + PROTECT_POTION_CHANCE:  # 3% 機率掉防護藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "protect_potion"))
            else:  # 2% 機率掉炸彈
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "bomb"))
    
    def render(self):
        """
        繪製所有遊戲畫面\n
        """
        global victory_timer, enemies_killed
        
        if self.game_state == GAME_STATE_MENU:
            # 繪製主畫面
            self.menu_system.draw_menu(self.screen)
        
        elif self.game_state == GAME_STATE_SHIP_BATTLE:
            # 繪製 Ship Battle 模式
            self.ship_battle_system.draw_battle_objects(self.screen)
            
            # 繪製 Ship Battle UI
            battle_info = self.ship_battle_system.get_battle_info()
            self.ui_system.draw_ship_battle_ui(self.screen, battle_info)
            
            # 繪製視覺效果（雪花或烏鴉）
            self.visual_effects_system.draw(self.screen)
        
        elif self.game_state == GAME_STATE_HIDE_SEEK:
            # 繪製躲貓貓遊戲
            if self.hide_seek_system:
                self.hide_seek_system.draw(self.screen)
        
        elif self.game_state == GAME_STATE_BOSS_FIGHT_MODE:
            # 繪製 Boss Fight 模式
            if self.boss_fight_system:
                self.boss_fight_system.draw(self.screen)
        
        else:
            # 清空螢幕（填滿黑色）
            self.screen.fill(BLACK)
            
            # 繪製遊戲物件（只有在商店關閉時）
            if not self.shop_open:
                self.player.draw(self.screen)
                
                # 繪製所有子彈
                for bullet in self.bullets:
                    bullet.draw(self.screen)
                
                # 繪製Boss子彈
                for boss_bullet in self.boss_bullets:
                    boss_bullet.draw(self.screen)
                
                # 繪製所有敵人
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                
                # 繪製Boss
                if self.boss:
                    self.boss.draw(self.screen)
                    # 繪製Boss血量條
                    self.boss.draw_health_bar(self.screen)
                
                # 繪製所有道具
                for powerup in self.powerups:
                    powerup.draw(self.screen)
            
            # 繪製 UI 介面
            self.ui_system.draw_ui(self.screen, self.player, score, stars)
            
            # 顯示敵人擊殺計數和Boss觸發進度
            if self.game_state == GAME_STATE_PLAYING:
                progress_font = create_font(FONT_SIZES["normal"])
                remaining = BOSS_TRIGGER_KILLS - enemies_killed
                if remaining > 0:
                    progress_text = progress_font.render(f"Boss 出現倒數: {remaining} 敵人", True, YELLOW)
                    self.screen.blit(progress_text, (SCREEN_WIDTH - 200, 40))
                else:
                    boss_ready_text = progress_font.render("Boss 即將出現！", True, RED)
                    self.screen.blit(boss_ready_text, (SCREEN_WIDTH - 200, 40))
            
            # 繪製煙火效果
            for firework in self.fireworks:
                firework.draw(self.screen)
            
            # 如果 Boss 被擊敗，顯示勝利訊息
            if boss_killed and victory_timer > 0:
                self.ui_system.draw_victory_message(self.screen, victory_timer)
            
            # 如果商店開啟，繪製商店介面
            if self.shop_open:
                self.shop_system.draw_shop(self.screen, stars)
            
            # 遊戲結束畫面
            if self.game_state == GAME_STATE_GAME_OVER:
                self._draw_game_over_screen()
            
            # 勝利畫面
            elif self.game_state == GAME_STATE_VICTORY:
                self._draw_victory_screen()
        
        # 更新畫面
        pygame.display.flip()
    
    def _draw_game_over_screen(self):
        """
        繪製遊戲結束畫面\n
        """
        # 半透明黑色覆蓋
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 遊戲結束文字
        font_large = create_font(FONT_SIZES["extra_large"])
        font_medium = create_font(FONT_SIZES["medium"])
        font_small = create_font(FONT_SIZES["normal"])
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最終分數
        score_text = font_medium.render(f"最終分數: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        stars_text = font_medium.render(f"星星數量: {stars}", True, YELLOW)
        stars_rect = stars_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(stars_text, stars_rect)
        
        killed_text = font_medium.render(f"擊敗敵人: {enemies_killed}", True, GREEN)
        killed_rect = killed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(killed_text, killed_rect)
        
        # 操作提示
        restart_text = font_small.render("按 R 重新開始 | 按 Enter 返回主畫面", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
    
    def _draw_victory_screen(self):
        """
        繪製勝利畫面\n
        """
        # 半透明金色覆蓋
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((40, 40, 0))  # 深金色
        self.screen.blit(overlay, (0, 0))
        
        # 勝利文字
        font_large = create_font(FONT_SIZES["extra_large"])
        font_medium = create_font(FONT_SIZES["medium"])
        font_small = create_font(FONT_SIZES["normal"])
        
        victory_text = font_large.render("VICTORY!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(victory_text, victory_rect)
        
        boss_text = font_medium.render("Boss 已被擊敗！", True, WHITE)
        boss_rect = boss_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(boss_text, boss_rect)
        
        # 最終分數
        score_text = font_medium.render(f"最終分數: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        stars_text = font_medium.render(f"星星數量: {stars}", True, YELLOW)
        stars_rect = stars_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(stars_text, stars_rect)
        
        # 操作提示
        continue_text = font_small.render("按 Enter 返回主畫面 | 按 R 重新開始", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(continue_text, continue_rect)
    
    def run(self):
        """
        執行主遊戲迴圈\n
        """
        while self.running:
            # 處理事件
            self.handle_events()
            
            # 更新遊戲狀態
            self.update_game_objects()
            
            # 繪製畫面
            self.render()
            
            # 控制遊戲幀率
            self.clock.tick(FPS)
        
        # 關閉遊戲
        pygame.quit()
        sys.exit()

######################主程式函數######################
def main():
    """
    遊戲主程式 - 建立並執行遊戲控制器\n
    """
    game = GameController()
    game.run()

# 啟動遊戲
main()