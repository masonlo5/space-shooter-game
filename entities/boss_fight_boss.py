######################載入套件######################
import pygame
import random
import math
from config import *

######################Boss Fight Boss 類別######################
class BossFightBoss:
    """
    Boss Fight 模式專用的 Boss 類別\n
    \n
    負責處理:\n
    1. 從配置載入不同 Boss 的屬性\n
    2. Boss 的移動邏輯\n
    3. Boss 的攻擊模式（普通攻擊和特殊攻擊）\n
    4. Boss 的生命值管理\n
    5. Boss 的繪製和血量條顯示\n
    """
    
    def __init__(self, x, y, boss_index):
        """
        初始化 Boss Fight Boss\n
        \n
        參數:\n
        x (int): Boss 初始 X 座標\n
        y (int): Boss 初始 Y 座標\n
        boss_index (int): Boss 索引（1-8）\n
        """
        self.boss_index = boss_index
        self.boss_config = BOSS_FIGHT_BOSSES[boss_index]
        
        # 基本屬性
        self.x = x
        self.y = y
        self.width = self.boss_config["width"]
        self.height = self.boss_config["height"]
        
        # 戰鬥屬性
        self.max_health = self.boss_config["health"]
        self.health = self.max_health
        self.speed = self.boss_config["speed"]
        self.attack_damage = self.boss_config["attack_damage"]
        
        # 攻擊冷卻
        self.attack_cooldown = 0
        self.special_attack_cooldown = 0
        self.attack_interval = self.boss_config["attack_cooldown"]
        self.special_interval = self.boss_config["special_attack_cooldown"]
        
        # 移動相關
        self.move_direction = 1  # 1 = 右, -1 = 左
        self.move_timer = 0
        
        # 外觀
        self.color = self.boss_config["color"]
        
        print(f"創建 Boss：{self.boss_config['name']}（第 {boss_index} 關）")
    
    def move(self):
        """
        Boss 移動邏輯\n
        """
        # 水平往返移動
        self.x += self.speed * self.move_direction
        
        # 碰到邊界時改變方向
        if self.x <= 0:
            self.move_direction = 1
            self.x = 0
        elif self.x >= SCREEN_WIDTH - self.width:
            self.move_direction = -1
            self.x = SCREEN_WIDTH - self.width
        
        # 偶爾垂直移動
        self.move_timer += 1
        if self.move_timer >= 180:  # 每3秒
            self.move_timer = 0
            # 隨機上下移動
            if random.random() < 0.5:
                new_y = self.y + random.randint(-20, 20)
                self.y = max(30, min(150, new_y))  # 限制在上半部
    
    def update(self, sounds=None):
        """
        更新 Boss 狀態並返回新產生的子彈\n
        \n
        參數:\n
        sounds (dict): 音效字典（可選）\n
        \n
        回傳:\n
        list: 新產生的子彈列表\n
        """
        new_bullets = []
        
        # 更新攻擊冷卻
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # 普通攻擊
        if self.attack_cooldown <= 0:
            new_bullets.extend(self._normal_attack())
            self.attack_cooldown = self.attack_interval
        
        # 特殊攻擊
        if self.special_attack_cooldown <= 0:
            new_bullets.extend(self._special_attack())
            self.special_attack_cooldown = self.special_interval
        
        return new_bullets
    
    def _normal_attack(self):
        """
        普通攻擊模式\n
        \n
        回傳:\n
        list: 產生的子彈列表\n
        """
        from entities.bullet import Bullet
        
        bullets = []
        
        # 根據 Boss 等級決定攻擊模式
        if self.boss_index <= 2:
            # 前兩個 Boss：單發子彈
            bullet_x = self.x + self.width // 2 - 3
            bullet_y = self.y + self.height
            bullets.append(BossBullet(bullet_x, bullet_y, "normal", self.attack_damage))
        
        elif self.boss_index <= 4:
            # 中級 Boss：雙發子彈
            left_bullet_x = self.x + self.width // 3 - 3
            right_bullet_x = self.x + self.width * 2 // 3 - 3
            bullet_y = self.y + self.height
            
            bullets.append(BossBullet(left_bullet_x, bullet_y, "normal", self.attack_damage))
            bullets.append(BossBullet(right_bullet_x, bullet_y, "normal", self.attack_damage))
        
        else:
            # 高級 Boss：三發子彈
            for i in range(3):
                bullet_x = self.x + (i + 1) * self.width // 4 - 3
                bullet_y = self.y + self.height
                bullets.append(BossBullet(bullet_x, bullet_y, "normal", self.attack_damage))
        
        return bullets
    
    def _special_attack(self):
        """
        特殊攻擊模式\n
        \n
        回傳:\n
        list: 產生的子彈列表\n
        """
        bullets = []
        
        # 根據 Boss 等級決定特殊攻擊
        if self.boss_index <= 2:
            # 前兩個 Boss：扇形散彈（3發）
            bullets.extend(self._create_spread_attack(3))
        
        elif self.boss_index <= 4:
            # 中級 Boss：扇形散彈（5發）
            bullets.extend(self._create_spread_attack(5))
        
        elif self.boss_index <= 6:
            # 高級 Boss：圓形彈幕（8發）
            bullets.extend(self._create_circle_attack(8))
        
        else:
            # 最終 Boss：混合攻擊
            bullets.extend(self._create_spread_attack(7))
            bullets.extend(self._create_circle_attack(6))
        
        return bullets
    
    def _create_spread_attack(self, bullet_count):
        """
        創建扇形散彈攻擊\n
        \n
        參數:\n
        bullet_count (int): 子彈數量\n
        \n
        回傳:\n
        list: 子彈列表\n
        """
        bullets = []
        center_x = self.x + self.width // 2
        center_y = self.y + self.height
        
        # 扇形角度範圍
        angle_range = 60  # 60度扇形
        angle_step = angle_range / (bullet_count - 1) if bullet_count > 1 else 0
        start_angle = 90 - angle_range // 2  # 從中心向下擴散
        
        for i in range(bullet_count):
            angle = start_angle + i * angle_step
            angle_rad = math.radians(angle)
            
            # 計算子彈的移動方向
            speed_x = math.sin(angle_rad) * 3
            speed_y = math.cos(angle_rad) * 3
            
            bullets.append(BossBullet(center_x - 3, center_y, "spread", 
                                    self.attack_damage, speed_x, speed_y))
        
        return bullets
    
    def _create_circle_attack(self, bullet_count):
        """
        創建圓形彈幕攻擊\n
        \n
        參數:\n
        bullet_count (int): 子彈數量\n
        \n
        回傳:\n
        list: 子彈列表\n
        """
        bullets = []
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        angle_step = 360 / bullet_count
        
        for i in range(bullet_count):
            angle = i * angle_step
            angle_rad = math.radians(angle)
            
            # 計算子彈的移動方向
            speed_x = math.cos(angle_rad) * 2
            speed_y = math.sin(angle_rad) * 2
            
            bullets.append(BossBullet(center_x - 3, center_y - 3, "circle", 
                                    self.attack_damage, speed_x, speed_y))
        
        return bullets
    
    def take_damage(self, damage):
        """
        Boss 受到傷害\n
        \n
        參數:\n
        damage (int): 傷害值\n
        \n
        回傳:\n
        bool: Boss 是否死亡\n
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.boss_config['name']} 被擊敗！")
            return True
        return False
    
    def draw(self, screen):
        """
        繪製 Boss\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 繪製 Boss 主體
        boss_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, boss_rect)
        
        # 繪製邊框
        pygame.draw.rect(screen, WHITE, boss_rect, 2)
        
        # 根據 Boss 等級繪製不同的圖案
        self._draw_boss_pattern(screen)
    
    def _draw_boss_pattern(self, screen):
        """
        繪製 Boss 特殊圖案\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.boss_index <= 2:
            # 前兩個 Boss：簡單圓形
            pygame.draw.circle(screen, WHITE, (center_x, center_y), self.width // 4)
        
        elif self.boss_index <= 4:
            # 中級 Boss：十字圖案
            cross_size = self.width // 3
            pygame.draw.line(screen, WHITE, 
                           (center_x - cross_size, center_y), 
                           (center_x + cross_size, center_y), 3)
            pygame.draw.line(screen, WHITE, 
                           (center_x, center_y - cross_size), 
                           (center_x, center_y + cross_size), 3)
        
        elif self.boss_index <= 6:
            # 高級 Boss：星形圖案
            points = []
            for i in range(8):
                angle = i * 45
                angle_rad = math.radians(angle)
                radius = self.width // 3 if i % 2 == 0 else self.width // 5
                point_x = center_x + math.cos(angle_rad) * radius
                point_y = center_y + math.sin(angle_rad) * radius
                points.append((point_x, point_y))
            
            if len(points) >= 3:
                pygame.draw.polygon(screen, WHITE, points)
        
        else:
            # 最終 Boss：複雜圖案
            # 外圈
            pygame.draw.circle(screen, WHITE, (center_x, center_y), self.width // 3, 3)
            # 內圈
            pygame.draw.circle(screen, WHITE, (center_x, center_y), self.width // 5, 2)
            # 中心點
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), 5)
    
    def draw_health_bar(self, screen):
        """
        繪製 Boss 血量條\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        bar_x = BOSS_FIGHT_UI["boss_health_bar_x"]
        bar_y = BOSS_FIGHT_UI["boss_health_bar_y"]
        bar_width = BOSS_FIGHT_UI["boss_health_bar_width"]
        bar_height = BOSS_FIGHT_UI["boss_health_bar_height"]
        
        # 背景
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # 血量
        health_percentage = max(0, self.health / self.max_health)
        health_width = int(bar_width * health_percentage)
        
        # 根據血量變化顏色
        if health_percentage > 0.6:
            health_color = RED
        elif health_percentage > 0.3:
            health_color = ORANGE
        else:
            health_color = (139, 0, 0)  # 深紅色
        
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # 邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Boss 名稱和血量文字
        boss_font = create_font(BOSS_FIGHT_UI["boss_name_font_size"])
        name_text = boss_font.render(self.boss_config["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y - 30))
        screen.blit(name_text, name_rect)
        
        health_font = create_font(BOSS_FIGHT_UI["progress_font_size"])
        health_text = health_font.render(f"{self.health}/{self.max_health}", True, WHITE)
        health_rect = health_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_height + 15))
        screen.blit(health_text, health_rect)


######################Boss 子彈類別######################
class BossBullet:
    """
    Boss 專用子彈類別\n
    """
    
    def __init__(self, x, y, bullet_type, damage, speed_x=0, speed_y=4):
        """
        初始化 Boss 子彈\n
        \n
        參數:\n
        x (int): 初始 X 座標\n
        y (int): 初始 Y 座標\n
        bullet_type (str): 子彈類型\n
        damage (int): 傷害值\n
        speed_x (float): X 方向速度\n
        speed_y (float): Y 方向速度\n
        """
        self.x = x
        self.y = y
        self.bullet_type = bullet_type
        self.damage = damage
        self.speed_x = speed_x
        self.speed_y = speed_y
        
        # 子彈外觀
        if bullet_type == "normal":
            self.width = 6
            self.height = 12
            self.color = RED
        elif bullet_type == "spread":
            self.width = 5
            self.height = 10
            self.color = ORANGE
        elif bullet_type == "circle":
            self.width = 4
            self.height = 8
            self.color = PURPLE
        else:
            self.width = 6
            self.height = 10
            self.color = YELLOW
    
    def move(self):
        """
        移動子彈\n
        """
        self.x += self.speed_x
        self.y += self.speed_y
    
    def is_off_screen(self):
        """
        檢查子彈是否飛出螢幕\n
        \n
        回傳:\n
        bool: 是否飛出螢幕\n
        """
        return (self.x < -20 or self.x > SCREEN_WIDTH + 20 or 
                self.y < -20 or self.y > SCREEN_HEIGHT + 20)
    
    def draw(self, screen):
        """
        繪製子彈\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        if self.bullet_type == "circle":
            # 圓形子彈
            radius = max(self.width, self.height) // 2
            pygame.draw.circle(screen, self.color, (int(self.x + radius), int(self.y + radius)), radius)
        else:
            # 矩形子彈
            bullet_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
            pygame.draw.rect(screen, self.color, bullet_rect)