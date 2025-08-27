######################載入套件######################
import pygame
import random
from config import *
from entities import Robot
from systems.collision import check_collision

######################Ship Battle 遊戲模式系統######################
class ShipBattleSystem:
    """
    Ship Battle 遊戲模式系統類別 - 處理玩家與機器人的對戰\n
    \n
    負責處理:\n
    1. 戰鬥開始前的準備階段（5秒倒數）\n
    2. 玩家與機器人的碰撞檢測\n
    3. 子彈碰撞檢測\n
    4. 血量管理\n
    5. 勝負判定\n
    6. 戰鬥結果處理\n
    \n
    屬性:\n
    player (Player): 玩家物件\n
    robot (Robot): 機器人對手\n
    player_bullets (list): 玩家子彈列表\n
    robot_bullets (list): 機器人子彈列表\n
    battle_state (str): 戰鬥狀態\n
    prepare_timer (int): 準備階段倒數計時器\n
    result_timer (int): 結果顯示計時器\n
    """
    
    def __init__(self):
        """
        初始化 Ship Battle 系統\n
        """
        # 戰鬥狀態
        self.battle_state = "inactive"  # inactive, prepare, fighting, victory, defeat
        self.prepare_timer = 0
        self.result_timer = 0
        
        # 戰鬥物件
        self.player = None
        self.robot = None
        self.player_bullets = []
        self.robot_bullets = []
        
        # 玩家資訊
        self.player_name = "Player"
        
        print("Ship Battle 系統初始化完成")
    
    def start_battle(self, player, player_name="Player"):
        """
        開始 Ship Battle 對戰\n
        \n
        參數:\n
        player (Player): 玩家物件\n
        player_name (str): 玩家名稱\n
        """
        print(f"開始 Ship Battle 對戰！玩家：{player_name} vs 機器人：RoboWarrior")
        
        # 設定玩家
        self.player = player
        self.player_name = player_name
        
        # 重置玩家狀態
        self.player.health = SHIP_BATTLE_STATS["initial_health"]
        self.player.max_health = SHIP_BATTLE_STATS["initial_health"]
        
        # 為玩家隨機分配太空船和武器
        available_ships = list(SPACESHIP_STATS.keys())
        available_weapons = list(WEAPON_STATS.keys())
        
        player_ship = random.choice(available_ships)
        player_weapon = random.choice(available_weapons)
        
        self.player.spaceship_type = player_ship
        self.player.current_weapon = player_weapon
        self.player.update_ship_stats()
        
        print(f"玩家獲得太空船：{player_ship}，武器：{player_weapon}")
        
        # 創建機器人
        robot_x = random.randint(100, SCREEN_WIDTH - 100)
        robot_y = 100
        self.robot = Robot(robot_x, robot_y)
        
        # 將玩家放在底部中央
        self.player.x = SCREEN_WIDTH // 2 - self.player.width // 2
        self.player.y = SCREEN_HEIGHT - 150
        
        # 清空子彈
        self.player_bullets.clear()
        self.robot_bullets.clear()
        
        # 設定戰鬥狀態
        self.battle_state = "prepare"
        self.prepare_timer = SHIP_BATTLE_STATS["prepare_time"]
        
        print("準備階段開始，5秒後戰鬥正式開始...")
    
    def update(self, keys):
        """
        更新 Ship Battle 系統狀態\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        \n
        回傳:\n
        str: 戰鬥結果狀態（"continue", "victory", "defeat", "quit"）\n
        """
        if self.battle_state == "inactive":
            return "continue"
        
        elif self.battle_state == "prepare":
            # 準備階段倒數
            self.prepare_timer -= 1
            if self.prepare_timer <= 0:
                self.battle_state = "fighting"
                print("戰鬥開始！")
            return "continue"
        
        elif self.battle_state == "fighting":
            # 戰鬥進行中
            return self._update_fighting(keys)
        
        elif self.battle_state in ["victory", "defeat"]:
            # 結果顯示階段
            self.result_timer -= 1
            if self.result_timer <= 0:
                return "end"  # 戰鬥結束，返回主選單
            return "continue"
        
        return "continue"
    
    def _update_fighting(self, keys):
        """
        更新戰鬥階段邏輯\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        \n
        回傳:\n
        str: 戰鬥結果\n
        """
        # 檢查退出鍵
        if keys[pygame.K_q]:
            print("玩家退出戰鬥")
            return "quit"
        
        # 更新玩家
        self._update_player(keys)
        
        # 更新機器人
        robot_bullets = self.robot.update(self.player.x, self.player.y)
        self.robot_bullets.extend(robot_bullets)
        
        # 更新子彈
        self._update_bullets()
        
        # 碰撞檢測
        battle_result = self._handle_collisions()
        if battle_result != "continue":
            return battle_result
        
        return "continue"
    
    def _update_player(self, keys):
        """
        更新玩家狀態\n
        \n
        參數:\n
        keys (pygame.key): 按鍵狀態\n
        """
        # 玩家移動（WASD 或方向鍵）
        self.player.move(keys)
        self.player.update()
        
        # 玩家射擊（按住 Shift 鍵）
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            new_bullet = self.player.shoot()
            if new_bullet:
                self.player_bullets.append(new_bullet)
        
        # 玩家特殊攻擊（Space 鍵）
        if keys[pygame.K_SPACE]:
            special_bullets = self.player.special_attack()
            self.player_bullets.extend(special_bullets)
        
        # 玩家使用血瓶（i 鍵）
        if keys[pygame.K_i]:
            self._use_player_health_potion()
    
    def _use_player_health_potion(self):
        """
        玩家使用血瓶\n
        """
        if (hasattr(self.player, 'health_potions') and 
            self.player.health_potions > 0 and 
            self.player.health < self.player.max_health):
            
            heal_amount = SHIP_BATTLE_STATS["health_potion_heal"]
            self.player.health = min(self.player.max_health, self.player.health + heal_amount)
            self.player.health_potions -= 1
            print(f"玩家使用血瓶！血量恢復到 {self.player.health}")
        else:
            # 為了 Ship Battle 模式，給玩家初始血瓶
            if not hasattr(self.player, 'health_potions'):
                self.player.health_potions = SHIP_BATTLE_STATS["health_potion_count"]
                self._use_player_health_potion()  # 遞迴呼叫使用血瓶
    
    def _update_bullets(self):
        """
        更新所有子彈位置\n
        """
        # 更新玩家子彈
        for bullet in self.player_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
        
        # 更新機器人子彈
        for bullet in self.robot_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.robot_bullets.remove(bullet)
    
    def _handle_collisions(self):
        """
        處理所有碰撞檢測\n
        \n
        回傳:\n
        str: 戰鬥結果（"continue", "victory", "defeat"）\n
        """
        # 玩家子彈打中機器人
        for bullet in self.player_bullets[:]:
            if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                             self.robot.x, self.robot.y, self.robot.width, self.robot.height):
                
                # 機器人受傷
                robot_dead = self.robot.take_damage(bullet.damage)
                self.player_bullets.remove(bullet)
                
                if robot_dead:
                    print(f"玩家獲勝！擊敗了機器人 {self.robot.name}")
                    self.battle_state = "victory"
                    self.result_timer = SHIP_BATTLE_STATS["victory_display_time"]
                    return "victory"
        
        # 機器人子彈打中玩家
        for bullet in self.robot_bullets[:]:
            if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                             self.player.x, self.player.y, self.player.width, self.player.height):
                
                # 玩家受傷
                self.player.health -= bullet.damage
                self.robot_bullets.remove(bullet)
                
                if self.player.health <= 0:
                    self.player.health = 0
                    print(f"機器人 {self.robot.name} 獲勝！玩家被擊敗")
                    self.battle_state = "defeat"
                    self.result_timer = SHIP_BATTLE_STATS["victory_display_time"]
                    return "defeat"
        
        # 玩家與機器人直接碰撞（同時扣血）
        if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                          self.robot.x, self.robot.y, self.robot.width, self.robot.height):
            
            # 雙方都受到撞擊傷害
            collision_damage = 30
            self.player.health -= collision_damage
            robot_dead = self.robot.take_damage(collision_damage)
            
            # 分離兩個物件，避免持續碰撞
            if self.player.x < self.robot.x:
                self.player.x -= 20
                self.robot.x += 20
            else:
                self.player.x += 20
                self.robot.x -= 20
            
            print(f"太空船碰撞！雙方各受到 {collision_damage} 點傷害")
            
            # 檢查是否有人死亡
            if self.player.health <= 0 and robot_dead:
                print("雙方同歸於盡！平手")
                self.battle_state = "defeat"  # 視為玩家失敗
                self.result_timer = SHIP_BATTLE_STATS["victory_display_time"]
                return "defeat"
            elif self.player.health <= 0:
                print(f"機器人 {self.robot.name} 獲勝！玩家在碰撞中被擊敗")
                self.battle_state = "defeat"
                self.result_timer = SHIP_BATTLE_STATS["victory_display_time"]
                return "defeat"
            elif robot_dead:
                print(f"玩家獲勝！在碰撞中擊敗了機器人 {self.robot.name}")
                self.battle_state = "victory"
                self.result_timer = SHIP_BATTLE_STATS["victory_display_time"]
                return "victory"
        
        return "continue"
    
    def get_battle_info(self):
        """
        取得戰鬥資訊用於 UI 顯示\n
        \n
        回傳:\n
        dict: 包含戰鬥資訊的字典\n
        """
        if not self.player or not self.robot:
            return {}
        
        # 確保玩家有血瓶屬性
        if not hasattr(self.player, 'health_potions'):
            self.player.health_potions = SHIP_BATTLE_STATS["health_potion_count"]
        
        return {
            "battle_state": self.battle_state,
            "prepare_timer": self.prepare_timer,
            "result_timer": self.result_timer,
            "player_name": self.player_name,
            "player_health": self.player.health,
            "player_max_health": self.player.max_health,
            "player_potions": self.player.health_potions,
            "robot_name": self.robot.name,
            "robot_health": self.robot.health,
            "robot_max_health": self.robot.max_health,
            "robot_potions": self.robot.health_potions
        }
    
    def draw_battle_objects(self, screen):
        """
        繪製所有戰鬥相關物件\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        if self.battle_state == "inactive":
            return
        
        # 清空螢幕（深太空背景）
        screen.fill((5, 5, 20))
        
        # 繪製簡單的星空背景
        import random
        random.seed(42)  # 固定種子確保星星位置一致
        for _ in range(80):
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT)
            star_brightness = random.randint(50, 200)
            star_color = (star_brightness, star_brightness, star_brightness)
            pygame.draw.circle(screen, star_color, (star_x, star_y), 1)
        
        # 繪製玩家和機器人
        if self.player:
            self.player.draw(screen)
        if self.robot:
            self.robot.draw(screen)
        
        # 繪製子彈
        for bullet in self.player_bullets:
            bullet.draw(screen)
        for bullet in self.robot_bullets:
            bullet.draw(screen)
    
    def reset(self):
        """
        重置 Ship Battle 系統\n
        """
        self.battle_state = "inactive"
        self.prepare_timer = 0
        self.result_timer = 0
        self.player = None
        self.robot = None
        self.player_bullets.clear()
        self.robot_bullets.clear()
        self.player_name = "Player"
        
        print("Ship Battle 系統已重置")