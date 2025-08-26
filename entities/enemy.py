######################載入套件######################
import pygame
import math
from config import ENEMY_STATS, SCREEN_HEIGHT

######################敵人類別######################
class Enemy:
    """
    敵人類別 - 處理各種敵人的行為和外觀\n
    \n
    負責處理:\n
    1. 敵人移動模式（直線、波浪、追蹤等）\n
    2. 敵人攻擊行為\n
    3. 不同敵人類型的外觀和屬性\n
    4. 生命值和傷害管理\n
    \n
    屬性:\n
    x (int): 敵人的 x 座標\n
    y (int): 敵人的 y 座標\n
    width (int): 敵人寬度\n
    height (int): 敵人高度\n
    health (int): 生命值\n
    speed (int): 移動速度\n
    enemy_type (str): 敵人類型，影響外觀和行為\n
    """
    
    def __init__(self, x, y, enemy_type="basic"):
        """
        初始化敵人\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        enemy_type (str): 敵人類型，預設為 'basic'\n
        """
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.movement_counter = 0  # 用於控制移動模式的計數器
        
        # 從設定檔載入敵人屬性
        if enemy_type in ENEMY_STATS:
            stats = ENEMY_STATS[enemy_type]
            self.width = stats["width"]
            self.height = stats["height"]
            self.health = stats["health"]
            self.speed = stats["speed"]
            self.color = stats["color"]
            self.score_value = stats["score"]
            self.star_value = stats["stars"]
        else:
            # 預設值
            from config import RED
            self.width = 30
            self.height = 25
            self.health = 30
            self.speed = 2
            self.color = RED
            self.score_value = 10
            self.star_value = 1
    
    def move(self):
        """
        移動敵人（根據類型有不同移動模式）\n
        """
        self.movement_counter += 1
        
        if self.enemy_type == "basic":
            # 基本敵人：直線向下移動
            self.y += self.speed
        elif self.enemy_type == "fast":
            # 快速敵人：直線向下移動，但速度較快
            self.y += self.speed
        elif self.enemy_type == "boss":
            # Boss：左右搖擺移動
            self.y += self.speed
            # 用正弦波控制左右移動
            self.x += math.sin(self.movement_counter * 0.1) * 2
    
    def draw(self, screen):
        """
        在螢幕上繪製敵人\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        from config import WHITE, RED, YELLOW
        
        if self.enemy_type == "basic":
            # 基本敵人：簡單矩形
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # 加上小細節（眼睛）
            pygame.draw.circle(screen, WHITE, (int(self.x + 8), int(self.y + 8)), 3)
            pygame.draw.circle(screen, WHITE, (int(self.x + 22), int(self.y + 8)), 3)
        elif self.enemy_type == "fast":
            # 快速敵人：三角形
            points = [
                (self.x + self.width // 2, self.y + self.height),  # 下方尖端
                (self.x, self.y),  # 左上角
                (self.x + self.width, self.y)  # 右上角
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.enemy_type == "boss":
            # Boss：複雜形狀
            # 主體
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # 砲台
            pygame.draw.rect(screen, RED, (self.x + 10, self.y + self.height - 5, 15, 10))
            pygame.draw.rect(screen, RED, (self.x + self.width - 25, self.y + self.height - 5, 15, 10))
            # 核心
            pygame.draw.circle(screen, YELLOW, (int(self.x + self.width // 2), int(self.y + self.height // 2)), 8)
    
    def is_off_screen(self):
        """
        檢查敵人是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果敵人已經離開螢幕返回 True\n
        """
        return self.y > SCREEN_HEIGHT
    
    def take_damage(self, damage):
        """
        受到傷害\n
        \n
        參數:\n
        damage (int): 受到的傷害值\n
        \n
        回傳:\n
        bool: 如果敵人死亡返回 True\n
        """
        self.health -= damage
        return self.health <= 0