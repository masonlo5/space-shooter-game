######################載入套件######################
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SPACESHIP_STATS

######################玩家太空船類別######################
class Player:
    """
    玩家太空船類別 - 控制玩家在太空中的移動和射擊\n
    \n
    負責處理:\n
    1. 玩家輸入控制（移動、射擊）\n
    2. 太空船狀態管理（生命值、位置）\n
    3. 太空船外觀繪製\n
    4. 邊界碰撞檢測\n
    \n
    屬性:\n
    x (int): 太空船的 x 座標\n
    y (int): 太空船的 y 座標\n
    width (int): 太空船寬度\n
    height (int): 太空船高度\n
    health (int): 生命值，範圍 0-100\n
    speed (int): 移動速度，範圍 1-10\n
    """
    
    def __init__(self, x, y):
        """
        初始化玩家太空船\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        """
        self.x = x
        self.y = y
        self.spaceship_type = "explorer"  # 太空船類型
        self.current_weapon = "basic"  # 目前使用的武器類型
        
        # 從設定檔載入太空船屬性
        stats = SPACESHIP_STATS[self.spaceship_type]
        self.width = stats["width"]
        self.height = stats["height"]
        self.health = stats["max_health"]
        self.max_health = stats["max_health"]
        self.speed = stats["speed"]
        
        # 遊戲狀態
        self.shoot_cooldown = 0  # 射擊冷卻時間，避免子彈發射太快
        self.special_attack_cooldown = 0  # 特殊攻擊冷卻時間
        self.unlocked_weapons = ["basic"]  # 已解鎖的武器
        self.unlocked_ships = ["explorer"]  # 已解鎖的太空船
        
        # 藥水庫存系統
        self.health_potions = 0  # 回血藥水數量
        self.speed_potions = 0   # 加速藥水數量
        self.protect_potions = 0 # 防護藥水數量
        
        # 藥水效果狀態
        self.speed_boost_timer = 0  # 加速效果剩餘時間
        self.protect_boost_timer = 0  # 防護效果剩餘時間
        self.original_speed = self.speed  # 記錄原始速度
        
    def move(self, keys):
        """
        根據按鍵輸入移動太空船\n
        \n
        參數:\n
        keys (pygame.key): pygame 按鍵狀態字典\n
        """
        # 左右移動
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        
        # 上下移動
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # 邊界檢查，不讓太空船跑出螢幕外
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
    
    def shoot(self):
        """
        發射子彈\n
        \n
        回傳:\n
        Bullet or None: 如果冷卻時間到了就回傳新子彈，否則回傳 None\n
        """
        if self.shoot_cooldown <= 0:
            # 計算子彈發射位置（從太空船前端中央）
            bullet_x = self.x + self.width // 2 - 2
            bullet_y = self.y
            
            # 重置射擊冷卻時間
            self.shoot_cooldown = 10  # 10 幀才能再射擊一次
            
            from entities.bullet import Bullet
            return Bullet(bullet_x, bullet_y, self.current_weapon)
        return None
    
    def update(self):
        """
        更新太空船狀態（主要是冷卻時間）\n
        """
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # 更新藥水效果
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                # 加速效果結束，恢復原始速度
                self.speed = self.original_speed
                print("加速效果結束")
        
        if self.protect_boost_timer > 0:
            self.protect_boost_timer -= 1
            if self.protect_boost_timer == 0:
                print("防護效果結束")
    
    def change_weapon(self):
        """
        切換武器類型（按空白鍵）\n
        """
        current_index = self.unlocked_weapons.index(self.current_weapon)
        # 切換到下一種武器，到最後一種就回到第一種
        self.current_weapon = self.unlocked_weapons[(current_index + 1) % len(self.unlocked_weapons)]
    
    def change_spaceship(self):
        """
        切換太空船類型\n
        """
        if len(self.unlocked_ships) > 1:
            current_index = self.unlocked_ships.index(self.spaceship_type)
            self.spaceship_type = self.unlocked_ships[(current_index + 1) % len(self.unlocked_ships)]
            self.update_ship_stats()
    
    def update_ship_stats(self):
        """
        根據太空船類型更新屬性\n
        """
        stats = SPACESHIP_STATS[self.spaceship_type]
        self.max_health = stats["max_health"]
        self.speed = stats["speed"]
        self.width = stats["width"]
        self.height = stats["height"]
        
        # 調整當前生命值不超過最大值
        if self.health > self.max_health:
            self.health = self.max_health
    
    def special_attack(self):
        """
        發動特殊攻擊（大招）\n
        \n
        回傳:\n
        list: 特殊攻擊產生的子彈清單\n
        """
        if self.special_attack_cooldown > 0:
            return []
        
        from entities.bullet import Bullet
        bullets = []
        center_x = self.x + self.width // 2
        stats = SPACESHIP_STATS[self.spaceship_type]
        
        if self.spaceship_type == "explorer":
            # 探索者：三重射擊
            bullets.append(Bullet(center_x - 10, self.y, self.current_weapon))
            bullets.append(Bullet(center_x, self.y, self.current_weapon))
            bullets.append(Bullet(center_x + 10, self.y, self.current_weapon))
            self.special_attack_cooldown = stats["special_cooldown"]
        elif self.spaceship_type == "fighter":
            # 戰鬥機：快速連射
            for i in range(5):
                bullets.append(Bullet(center_x - 5 + i * 2, self.y - i * 5, self.current_weapon))
            self.special_attack_cooldown = stats["special_cooldown"]
        elif self.spaceship_type == "interceptor":
            # 攔截機：散射攻擊
            for angle in [-30, -15, 0, 15, 30]:
                bullet = Bullet(center_x, self.y, self.current_weapon)
                bullets.append(bullet)
            self.special_attack_cooldown = stats["special_cooldown"]
        elif self.spaceship_type == "destroyer":
            # 驅逐艦：重型飛彈
            bullets.append(Bullet(center_x, self.y, "missile"))
            self.special_attack_cooldown = stats["special_cooldown"]
        elif self.spaceship_type == "battleship":
            # 戰艦：離子砲轟擊
            bullets.append(Bullet(center_x, self.y, "ion_cannon"))
            self.special_attack_cooldown = stats["special_cooldown"]
        
        return bullets
    
    def use_health_potion(self):
        """
        使用回血藥水\n
        \n
        回傳:\n
        bool: 是否成功使用藥水\n
        """
        if self.health_potions > 0 and self.health < self.max_health:
            self.health_potions -= 1
            old_health = self.health
            self.health = min(self.max_health, self.health + 30)
            healed = self.health - old_health
            print(f"使用回血藥水！回復 {healed} 生命值，剩餘藥水：{self.health_potions}")
            return True
        elif self.health >= self.max_health:
            print("生命值已滿，無需使用回血藥水")
            return False
        else:
            print("沒有回血藥水可用")
            return False
    
    def use_speed_potion(self):
        """
        使用加速藥水\n
        \n
        回傳:\n
        bool: 是否成功使用藥水\n
        """
        if self.speed_potions > 0:
            self.speed_potions -= 1
            if self.speed_boost_timer <= 0:
                self.original_speed = self.speed  # 記錄當前速度
            self.speed = min(8, self.original_speed + 2)  # 增加速度
            self.speed_boost_timer = 300  # 5秒效果
            print(f"使用加速藥水！速度提升至 {self.speed}，剩餘藥水：{self.speed_potions}")
            return True
        else:
            print("沒有加速藥水可用")
            return False
    
    def use_protect_potion(self):
        """
        使用防護藥水\n
        \n
        回傳:\n
        bool: 是否成功使用藥水\n
        """
        if self.protect_potions > 0:
            self.protect_potions -= 1
            old_health = self.health
            self.health = min(self.max_health, self.health + 50)  # 回復生命值
            self.protect_boost_timer = 600  # 10秒防護效果
            healed = self.health - old_health
            print(f"使用防護藥水！回復 {healed} 生命值並獲得防護效果，剩餘藥水：{self.protect_potions}")
            return True
        else:
            print("沒有防護藥水可用")
            return False
    
    def add_potion(self, potion_type):
        """
        添加藥水到庫存\n
        \n
        參數:\n
        potion_type (str): 藥水類型 ("health_potion", "speed_potion", "protect_potion")\n
        """
        if potion_type == "health_potion":
            self.health_potions += 1
            print(f"獲得回血藥水！目前擁有：{self.health_potions}")
        elif potion_type == "speed_potion":
            self.speed_potions += 1
            print(f"獲得加速藥水！目前擁有：{self.speed_potions}")
        elif potion_type == "protect_potion":
            self.protect_potions += 1
            print(f"獲得防護藥水！目前擁有：{self.protect_potions}")
    
    def has_protect_effect(self):
        """
        檢查是否有防護效果\n
        \n
        回傳:\n
        bool: 是否有防護效果\n
        """
        return self.protect_boost_timer > 0
    
    def draw(self, screen):
        """
        在螢幕上繪製太空船\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        from config import CYAN, GREEN, YELLOW, PURPLE, MAGENTA, ORANGE, WHITE
        
        if self.spaceship_type == "explorer":
            # 探索者：基本三角形設計
            ship_points = [
                (self.x + self.width // 2, self.y),  # 船頭
                (self.x, self.y + self.height),      # 左下角
                (self.x + self.width, self.y + self.height)  # 右下角
            ]
            pygame.draw.polygon(screen, CYAN, ship_points)
        elif self.spaceship_type == "fighter":
            # 戰鬥機：銳利設計
            ship_points = [
                (self.x + self.width // 2, self.y),
                (self.x + 5, self.y + self.height),
                (self.x + self.width - 5, self.y + self.height)
            ]
            pygame.draw.polygon(screen, GREEN, ship_points)
            # 機翼
            pygame.draw.polygon(screen, GREEN, [
                (self.x, self.y + 15), (self.x + 10, self.y + 25), (self.x + 5, self.y + 35)
            ])
            pygame.draw.polygon(screen, GREEN, [
                (self.x + self.width, self.y + 15), (self.x + self.width - 10, self.y + 25), 
                (self.x + self.width - 5, self.y + 35)
            ])
        elif self.spaceship_type == "interceptor":
            # 攔截機：細長快速設計
            ship_points = [
                (self.x + self.width // 2, self.y),
                (self.x + 8, self.y + self.height),
                (self.x + self.width - 8, self.y + self.height)
            ]
            pygame.draw.polygon(screen, YELLOW, ship_points)
            # 加速器
            pygame.draw.rect(screen, ORANGE, (self.x + 5, self.y + 20, 5, 15))
            pygame.draw.rect(screen, ORANGE, (self.x + self.width - 10, self.y + 20, 5, 15))
        elif self.spaceship_type == "destroyer":
            # 驅逐艦：重型設計
            pygame.draw.rect(screen, PURPLE, (self.x, self.y + 10, self.width, self.height - 10))
            ship_points = [
                (self.x + self.width // 2, self.y),
                (self.x + 10, self.y + 15),
                (self.x + self.width - 10, self.y + 15)
            ]
            pygame.draw.polygon(screen, PURPLE, ship_points)
            # 武器掛載點
            from config import RED
            pygame.draw.rect(screen, RED, (self.x - 5, self.y + 20, 8, 6))
            pygame.draw.rect(screen, RED, (self.x + self.width - 3, self.y + 20, 8, 6))
        elif self.spaceship_type == "battleship":
            # 戰艦：最大型設計
            pygame.draw.rect(screen, MAGENTA, (self.x, self.y + 15, self.width, self.height - 15))
            ship_points = [
                (self.x + self.width // 2, self.y),
                (self.x + 15, self.y + 20),
                (self.x + self.width - 15, self.y + 20)
            ]
            pygame.draw.polygon(screen, MAGENTA, ship_points)
            # 主砲
            pygame.draw.rect(screen, WHITE, (self.x + self.width // 2 - 3, self.y, 6, 25))
        
        # 引擎（所有太空船都有）
        engine_width = max(6, self.width // 8)
        engine_height = 12
        left_engine_x = self.x + engine_width
        right_engine_x = self.x + self.width - engine_width * 2
        engine_y = self.y + self.height - 5
        
        pygame.draw.rect(screen, ORANGE, (left_engine_x, engine_y, engine_width, engine_height))
        pygame.draw.rect(screen, ORANGE, (right_engine_x, engine_y, engine_width, engine_height))