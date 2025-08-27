######################載入套件######################
import pygame
import random
import math
from config import *

######################機器人玩家類別######################
class Robot:
    """
    機器人對手類別 - RoboWarrior 的 AI 控制邏輯\n
    \n
    負責處理:\n
    1. 機器人的自動移動（在螢幕內隨機移動）\n
    2. 機器人的自動射擊\n
    3. 機器人的特殊攻擊\n
    4. 機器人的血瓶使用策略\n
    5. 邊界檢測和移動限制\n
    \n
    屬性:\n
    x (int): 機器人的 x 座標\n
    y (int): 機器人的 y 座標\n
    width (int): 機器人寬度\n
    height (int): 機器人高度\n
    health (int): 當前生命值\n
    max_health (int): 最大生命值\n
    spaceship_type (str): 太空船類型\n
    weapon_type (str): 武器類型\n
    health_potions (int): 剩餘血瓶數量\n
    """
    
    def __init__(self, x, y):
        """
        初始化機器人對手\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        """
        self.x = x
        self.y = y
        
        # 從配置檔載入機器人設定
        self.name = ROBOT_STATS["name"]
        self.health = ROBOT_STATS["initial_health"]
        self.max_health = ROBOT_STATS["initial_health"]
        self.health_potions = ROBOT_STATS["health_potion_count"]
        self.move_speed = ROBOT_STATS["move_speed"]
        
        # 隨機分配太空船類型
        available_ships = list(SPACESHIP_STATS.keys())
        self.spaceship_type = random.choice(available_ships)
        ship_stats = SPACESHIP_STATS[self.spaceship_type]
        
        # 套用太空船屬性
        self.width = ship_stats["width"]
        self.height = ship_stats["height"]
        self.max_health = ship_stats["max_health"]
        self.health = self.max_health
        
        # 隨機分配武器類型
        available_weapons = list(WEAPON_STATS.keys())
        self.weapon_type = random.choice(available_weapons)
        
        # AI 行為控制
        self.shoot_cooldown = 0
        self.special_attack_cooldown = 0
        self.move_timer = 0
        self.move_direction_x = random.choice([-1, 0, 1])  # 隨機初始移動方向
        self.move_direction_y = random.choice([-1, 0, 1])
        self.direction_change_timer = 0
        
        # AI 決策參數
        self.aggression_level = random.uniform(0.6, 1.0)  # 攻擊性 60%-100%
        self.movement_pattern = random.choice(["aggressive", "defensive", "random"])
        
        print(f"機器人 {self.name} 準備就緒！")
        print(f"  太空船: {self.spaceship_type}")
        print(f"  武器: {self.weapon_type}")
        print(f"  生命值: {self.health}")
        print(f"  行為模式: {self.movement_pattern}")
    
    def update(self, player_x, player_y):
        """
        更新機器人狀態和 AI 決策\n
        \n
        參數:\n
        player_x (int): 玩家 x 座標\n
        player_y (int): 玩家 y 座標\n
        \n
        回傳:\n
        list: 機器人射出的子彈列表\n
        """
        bullets_fired = []
        
        # 更新冷卻時間
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # 自動移動
        self._update_movement(player_x, player_y)
        
        # 自動射擊
        bullets_fired.extend(self._try_shoot())
        
        # 自動使用特殊攻擊
        bullets_fired.extend(self._try_special_attack())
        
        # 自動使用血瓶
        self._try_use_health_potion()
        
        return bullets_fired
    
    def _update_movement(self, player_x, player_y):
        """
        更新機器人移動邏輯\n
        \n
        參數:\n
        player_x (int): 玩家 x 座標\n
        player_y (int): 玩家 y 座標\n
        """
        self.direction_change_timer += 1
        
        # 每 60-120 幀（1-2秒）改變一次移動方向
        if self.direction_change_timer >= random.randint(60, 120):
            self.direction_change_timer = 0
            
            if self.movement_pattern == "aggressive":
                # 攻擊型：朝玩家靠近
                if player_x < self.x:
                    self.move_direction_x = -1
                elif player_x > self.x:
                    self.move_direction_x = 1
                else:
                    self.move_direction_x = 0
                
                if player_y < self.y:
                    self.move_direction_y = -1
                elif player_y > self.y:
                    self.move_direction_y = 1
                else:
                    self.move_direction_y = 0
            
            elif self.movement_pattern == "defensive":
                # 防禦型：保持距離
                distance = math.sqrt((player_x - self.x)**2 + (player_y - self.y)**2)
                if distance < 150:  # 距離太近就遠離
                    if player_x < self.x:
                        self.move_direction_x = 1
                    else:
                        self.move_direction_x = -1
                    
                    if player_y < self.y:
                        self.move_direction_y = 1
                    else:
                        self.move_direction_y = -1
                else:
                    # 距離夠遠就隨機移動
                    self.move_direction_x = random.choice([-1, 0, 1])
                    self.move_direction_y = random.choice([-1, 0, 1])
            
            else:  # random
                # 隨機移動
                self.move_direction_x = random.choice([-1, 0, 1])
                self.move_direction_y = random.choice([-1, 0, 1])
        
        # 計算新位置
        new_x = self.x + self.move_direction_x * self.move_speed
        new_y = self.y + self.move_direction_y * self.move_speed
        
        # 邊界檢查，不讓機器人移動出螢幕
        boundary_margin = SHIP_BATTLE_STATS["screen_boundary_margin"]
        if boundary_margin <= new_x <= SCREEN_WIDTH - self.width - boundary_margin:
            self.x = new_x
        else:
            # 撞到邊界就反向
            self.move_direction_x *= -1
        
        if boundary_margin <= new_y <= SCREEN_HEIGHT - self.height - boundary_margin:
            self.y = new_y
        else:
            # 撞到邊界就反向
            self.move_direction_y *= -1
    
    def _try_shoot(self):
        """
        嘗試射擊（根據 AI 攻擊性決定）\n
        \n
        回傳:\n
        list: 射出的子彈列表\n
        """
        bullets = []
        
        # 根據攻擊性決定射擊頻率
        shoot_chance = self.aggression_level * 0.8  # 最高 80% 機率射擊
        
        if (self.shoot_cooldown <= 0 and 
            random.random() < shoot_chance):
            
            # 計算子彈發射位置
            bullet_x = self.x + self.width // 2 - 2
            bullet_y = self.y + self.height  # 機器人從下方射擊
            
            # 設定射擊冷卻時間
            self.shoot_cooldown = ROBOT_STATS["shoot_cooldown"]
            
            # 建立子彈（需要建立一個適合機器人的子彈類別）
            from entities.bullet import RobotBullet
            bullets.append(RobotBullet(bullet_x, bullet_y, self.weapon_type))
        
        return bullets
    
    def _try_special_attack(self):
        """
        嘗試使用特殊攻擊\n
        \n
        回傳:\n
        list: 特殊攻擊產生的子彈列表\n
        """
        bullets = []
        
        # 只有在冷卻時間結束且隨機觸發時才使用特殊攻擊
        special_chance = self.aggression_level * 0.3  # 最高 30% 機率使用特殊攻擊
        
        if (self.special_attack_cooldown <= 0 and 
            random.random() < special_chance):
            
            from entities.bullet import RobotBullet
            center_x = self.x + self.width // 2
            bullet_y = self.y + self.height
            
            # 根據太空船類型執行不同的特殊攻擊
            if self.spaceship_type == "explorer":
                # 三重射擊
                bullets.append(RobotBullet(center_x - 10, bullet_y, self.weapon_type))
                bullets.append(RobotBullet(center_x, bullet_y, self.weapon_type))
                bullets.append(RobotBullet(center_x + 10, bullet_y, self.weapon_type))
            
            elif self.spaceship_type == "fighter":
                # 快速連射
                for i in range(5):
                    bullets.append(RobotBullet(center_x - 5 + i * 2, bullet_y + i * 3, self.weapon_type))
            
            elif self.spaceship_type == "interceptor":
                # 散射攻擊
                for offset in [-20, -10, 0, 10, 20]:
                    bullets.append(RobotBullet(center_x + offset, bullet_y, self.weapon_type))
            
            elif self.spaceship_type == "destroyer":
                # 重型飛彈
                bullets.append(RobotBullet(center_x, bullet_y, "missile"))
            
            elif self.spaceship_type == "battleship":
                # 離子砲
                bullets.append(RobotBullet(center_x, bullet_y, "ion_cannon"))
            
            # 設定特殊攻擊冷卻時間
            self.special_attack_cooldown = ROBOT_STATS["special_attack_cooldown"]
        
        return bullets
    
    def _try_use_health_potion(self):
        """
        自動使用血瓶（當血量過低時）\n
        """
        health_threshold = ROBOT_STATS["health_potion_use_threshold"]
        
        if (self.health <= health_threshold and 
            self.health_potions > 0):
            
            # 使用血瓶
            heal_amount = ROBOT_STATS["health_potion_heal"]
            self.health = min(self.max_health, self.health + heal_amount)
            self.health_potions -= 1
            
            print(f"機器人 {self.name} 使用了血瓶！血量恢復到 {self.health}")
    
    def take_damage(self, damage):
        """
        機器人受到傷害\n
        \n
        參數:\n
        damage (int): 傷害值\n
        \n
        回傳:\n
        bool: 如果機器人死亡返回 True\n
        """
        self.health -= damage
        
        if self.health <= 0:
            self.health = 0
            print(f"機器人 {self.name} 被擊敗！")
            return True  # 機器人死亡
        
        return False  # 機器人還活著
    
    def use_health_potion(self):
        """
        手動使用血瓶（供外部呼叫）\n
        \n
        回傳:\n
        bool: 如果成功使用血瓶返回 True\n
        """
        if self.health_potions > 0 and self.health < self.max_health:
            heal_amount = ROBOT_STATS["health_potion_heal"]
            self.health = min(self.max_health, self.health + heal_amount)
            self.health_potions -= 1
            return True
        return False
    
    def draw(self, screen):
        """
        在螢幕上繪製機器人太空船\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 機器人的太空船外觀與玩家類似，但使用紅色系配色
        robot_color = ROBOT_STATS["color"]
        
        if self.spaceship_type == "explorer":
            # 基本三角形設計
            ship_points = [
                (self.x + self.width // 2, self.y + self.height),  # 船頭（向下）
                (self.x, self.y),                                  # 左上角
                (self.x + self.width, self.y)                      # 右上角
            ]
            pygame.draw.polygon(screen, robot_color, ship_points)
        
        elif self.spaceship_type == "fighter":
            # 戰鬥機設計
            ship_points = [
                (self.x + self.width // 2, self.y + self.height),
                (self.x + 5, self.y),
                (self.x + self.width - 5, self.y)
            ]
            pygame.draw.polygon(screen, robot_color, ship_points)
            # 機翼
            pygame.draw.polygon(screen, robot_color, [
                (self.x, self.y + self.height - 15), (self.x + 10, self.y + self.height - 25), 
                (self.x + 5, self.y + self.height - 35)
            ])
            pygame.draw.polygon(screen, robot_color, [
                (self.x + self.width, self.y + self.height - 15), 
                (self.x + self.width - 10, self.y + self.height - 25), 
                (self.x + self.width - 5, self.y + self.height - 35)
            ])
        
        elif self.spaceship_type == "interceptor":
            # 攔截機設計
            ship_points = [
                (self.x + self.width // 2, self.y + self.height),
                (self.x + 8, self.y),
                (self.x + self.width - 8, self.y)
            ]
            pygame.draw.polygon(screen, robot_color, ship_points)
            # 加速器
            pygame.draw.rect(screen, ORANGE, (self.x + 5, self.y + self.height - 35, 5, 15))
            pygame.draw.rect(screen, ORANGE, (self.x + self.width - 10, self.y + self.height - 35, 5, 15))
        
        elif self.spaceship_type == "destroyer":
            # 驅逐艦設計
            pygame.draw.rect(screen, robot_color, (self.x, self.y, self.width, self.height - 10))
            ship_points = [
                (self.x + self.width // 2, self.y + self.height),
                (self.x + 10, self.y + self.height - 15),
                (self.x + self.width - 10, self.y + self.height - 15)
            ]
            pygame.draw.polygon(screen, robot_color, ship_points)
        
        elif self.spaceship_type == "battleship":
            # 戰艦設計
            pygame.draw.rect(screen, robot_color, (self.x, self.y, self.width, self.height - 15))
            ship_points = [
                (self.x + self.width // 2, self.y + self.height),
                (self.x + 15, self.y + self.height - 20),
                (self.x + self.width - 15, self.y + self.height - 20)
            ]
            pygame.draw.polygon(screen, robot_color, ship_points)
            # 主砲
            pygame.draw.rect(screen, WHITE, (self.x + self.width // 2 - 3, self.y + self.height - 25, 6, 25))
        
        # 引擎（紅色，表示機器人）
        engine_width = max(6, self.width // 8)
        engine_height = 12
        left_engine_x = self.x + engine_width
        right_engine_x = self.x + self.width - engine_width * 2
        engine_y = self.y + 5
        
        pygame.draw.rect(screen, RED, (left_engine_x, engine_y, engine_width, engine_height))
        pygame.draw.rect(screen, RED, (right_engine_x, engine_y, engine_width, engine_height))
        
        # 機器人標誌（在太空船上方顯示一個小圓點）
        pygame.draw.circle(screen, WHITE, (self.x + self.width // 2, self.y - 10), 3)
        pygame.draw.circle(screen, RED, (self.x + self.width // 2, self.y - 10), 2)