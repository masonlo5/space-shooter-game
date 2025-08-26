######################載入套件######################
import pygame
from config import WEAPON_STATS, SCREEN_HEIGHT

######################子彈類別######################
class Bullet:
    """
    子彈類別 - 處理各種武器發射的彈藥\n
    \n
    負責處理:\n
    1. 子彈移動軌跡\n
    2. 不同武器類型的子彈外觀\n
    3. 邊界檢測（超出螢幕即刪除）\n
    4. 傷害數值管理\n
    \n
    屬性:\n
    x (int): 子彈的 x 座標\n
    y (int): 子彈的 y 座標\n
    speed (int): 移動速度\n
    damage (int): 傷害值\n
    bullet_type (str): 武器類型，影響外觀和傷害\n
    """
    
    def __init__(self, x, y, bullet_type="basic"):
        """
        初始化子彈\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        bullet_type (str): 武器類型，預設為 'basic'\n
        """
        self.x = x
        self.y = y
        self.speed = 8
        self.bullet_type = bullet_type
        
        # 從設定檔載入武器屬性
        if bullet_type in WEAPON_STATS:
            weapon_data = WEAPON_STATS[bullet_type]
            self.damage = weapon_data["damage"]
            self.color = weapon_data["color"]
            self.width = weapon_data["width"]
            self.height = weapon_data["height"]
        else:
            # 預設值
            from config import YELLOW
            self.damage = 15
            self.color = YELLOW
            self.width = 4
            self.height = 10
    
    def move(self):
        """
        移動子彈（向上移動）\n
        """
        self.y -= self.speed
    
    def draw(self, screen):
        """
        在螢幕上繪製子彈\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        from config import RED, WHITE
        
        if self.bullet_type == "basic":
            # 基本子彈：簡單矩形
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.bullet_type == "laser":
            # 雷射：更細長的矩形
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.bullet_type == "plasma":
            # 電漿彈：橢圓形
            pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        elif self.bullet_type == "missile":
            # 飛彈：火箭形狀
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # 飛彈尾焰
            pygame.draw.polygon(screen, RED, [
                (self.x + 2, self.y + self.height),
                (self.x + self.width - 2, self.y + self.height),
                (self.x + self.width // 2, self.y + self.height + 8)
            ])
        elif self.bullet_type == "ion_cannon":
            # 離子砲：強力光束
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # 能量核心
            pygame.draw.circle(screen, WHITE, (self.x + self.width // 2, self.y + self.height // 2), 3)
    
    def is_off_screen(self):
        """
        檢查子彈是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果子彈已經離開螢幕返回 True\n
        """
        return self.y < -self.height