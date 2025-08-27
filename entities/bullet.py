######################載入套件######################
import pygame
import math
from config import WEAPON_STATS, BOSS_BULLET_STATS, SCREEN_HEIGHT, SCREEN_WIDTH

######################子彈類別######################
class Bullet:
    """
    子彈類別 - 處理各種武器發射的彈藥和Boss攻擊\n
    \n
    負責處理:\n
    1. 子彈移動軌跡（玩家向上，Boss向下）\n
    2. 不同武器類型的子彈外觀\n
    3. Boss攻擊子彈（垃圾和散彈）\n
    4. 邊界檢測（超出螢幕即刪除）\n
    5. 傷害數值管理\n
    \n
    屬性:\n
    x (float): 子彈的 x 座標\n
    y (float): 子彈的 y 座標\n
    velocity_x (float): x方向速度（用於散彈）\n
    velocity_y (float): y方向速度\n
    damage (int): 傷害值\n
    bullet_type (str): 武器類型，影響外觀和傷害\n
    is_boss_bullet (bool): 是否為Boss子彈\n
    """
    
    def __init__(self, x, y, bullet_type="basic", angle=None):
        """
        初始化子彈\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        bullet_type (str): 武器類型，預設為 'basic'\n
        angle (float): 發射角度（用於Boss散彈攻擊）\n
        """
        self.x = float(x)
        self.y = float(y)
        self.bullet_type = bullet_type
        
        # 判斷是否為Boss子彈
        self.is_boss_bullet = bullet_type.startswith("boss_")
        
        if self.is_boss_bullet:
            # Boss子彈設定
            if bullet_type in BOSS_BULLET_STATS:
                bullet_data = BOSS_BULLET_STATS[bullet_type]
                self.damage = bullet_data["damage"]
                self.color = bullet_data["color"]
                self.width = bullet_data["width"]
                self.height = bullet_data["height"]
                base_speed = bullet_data["speed"]
            else:
                # Boss子彈預設值
                from config import RED
                self.damage = 20
                self.color = RED
                self.width = 8
                self.height = 8
                base_speed = 3
            
            # 設定Boss子彈的移動方向
            if bullet_type == "boss_garbage":
                # 垃圾攻擊：直線向下
                self.velocity_x = 0
                self.velocity_y = base_speed
            elif bullet_type == "boss_spread" and angle is not None:
                # 散彈攻擊：根據角度計算速度分量
                angle_rad = math.radians(angle)
                self.velocity_x = base_speed * math.sin(angle_rad)
                self.velocity_y = base_speed * math.cos(angle_rad)
            else:
                # 預設向下移動
                self.velocity_x = 0
                self.velocity_y = base_speed
        else:
            # 玩家子彈設定
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
            
            # 玩家子彈向上移動
            self.velocity_x = 0
            self.velocity_y = -8  # 負值表示向上
    
    def move(self):
        """
        移動子彈（根據速度向量移動）\n
        """
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def draw(self, screen):
        """
        在螢幕上繪製子彈\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        from config import RED, WHITE, ORANGE
        
        # 計算整數座標用於繪製
        draw_x = int(self.x)
        draw_y = int(self.y)
        
        if self.bullet_type == "boss_garbage":
            # Boss垃圾攻擊：不規則形狀
            # 主體（棕色方塊）
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
            # 垃圾細節（小黑點）
            pygame.draw.circle(screen, (0, 0, 0), (draw_x + 2, draw_y + 2), 1)
            pygame.draw.circle(screen, (0, 0, 0), (draw_x + 6, draw_y + 5), 1)
        elif self.bullet_type == "boss_spread":
            # Boss散彈攻擊：紅色菱形
            points = [
                (draw_x + self.width // 2, draw_y),  # 上
                (draw_x + self.width, draw_y + self.height // 2),  # 右
                (draw_x + self.width // 2, draw_y + self.height),  # 下
                (draw_x, draw_y + self.height // 2)  # 左
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.bullet_type == "basic":
            # 基本子彈：簡單矩形
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "laser":
            # 雷射：更細長的矩形
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "plasma":
            # 電漿彈：橢圓形
            pygame.draw.ellipse(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "missile":
            # 飛彈：火箭形狀
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
            # 飛彈尾焰
            pygame.draw.polygon(screen, RED, [
                (draw_x + 2, draw_y + self.height),
                (draw_x + self.width - 2, draw_y + self.height),
                (draw_x + self.width // 2, draw_y + self.height + 8)
            ])
        elif self.bullet_type == "ion_cannon":
            # 離子砲：強力光束
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
            # 能量核心
            pygame.draw.circle(screen, WHITE, (draw_x + self.width // 2, draw_y + self.height // 2), 3)
    
    def is_off_screen(self):
        """
        檢查子彈是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果子彈已經離開螢幕返回 True\n
        """
        # 檢查是否超出螢幕邊界
        if self.x < -self.width or self.x > SCREEN_WIDTH:
            return True
        if self.y < -self.height or self.y > SCREEN_HEIGHT:
            return True
        return False

######################機器人子彈類別######################
class RobotBullet:
    """
    機器人子彈類別 - 處理機器人發射的子彈\n
    \n
    與玩家子彈的差異:\n
    1. 向下移動（機器人在上方）\n
    2. 使用紅色系配色\n
    3. 移動速度和傷害與武器類型相關\n
    \n
    屬性:\n
    x (float): 子彈的 x 座標\n
    y (float): 子彈的 y 座標\n
    velocity_x (float): x方向速度\n
    velocity_y (float): y方向速度\n
    damage (int): 傷害值\n
    bullet_type (str): 武器類型\n
    """
    
    def __init__(self, x, y, bullet_type="basic"):
        """
        初始化機器人子彈\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        bullet_type (str): 武器類型\n
        """
        self.x = float(x)
        self.y = float(y)
        self.bullet_type = bullet_type
        
        # 從武器設定載入屬性
        if bullet_type in WEAPON_STATS:
            weapon_data = WEAPON_STATS[bullet_type]
            self.damage = weapon_data["damage"]
            self.width = weapon_data["width"]
            self.height = weapon_data["height"]
            # 機器人子彈使用較暗的紅色系
            original_color = weapon_data["color"]
            self.color = self._convert_to_robot_color(original_color)
        else:
            # 預設值
            self.damage = 15
            self.width = 4
            self.height = 10
            self.color = (200, 50, 50)  # 暗紅色
        
        # 機器人子彈向下移動
        self.velocity_x = 0
        self.velocity_y = 6  # 正值表示向下移動
    
    def _convert_to_robot_color(self, original_color):
        """
        將原始武器顏色轉換為機器人專用的紅色系\n
        \n
        參數:\n
        original_color (tuple): 原始 RGB 顏色\n
        \n
        回傳:\n
        tuple: 機器人專用的紅色系顏色\n
        """
        from config import RED, ORANGE, PURPLE, CYAN, YELLOW
        
        # 根據原始顏色轉換為對應的紅色系
        if original_color == YELLOW:  # basic
            return (200, 200, 50)  # 暗黃色
        elif original_color == RED:   # laser
            return (255, 50, 50)   # 純紅色
        elif original_color == PURPLE: # plasma
            return (200, 50, 100)  # 紅紫色
        elif original_color == ORANGE: # missile
            return (255, 100, 50)  # 紅橙色
        elif original_color == CYAN:   # ion_cannon
            return (200, 50, 200)  # 紅藍色
        else:
            return (200, 50, 50)   # 預設暗紅色
    
    def move(self):
        """
        移動機器人子彈\n
        """
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def draw(self, screen):
        """
        在螢幕上繪製機器人子彈\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 計算整數座標用於繪製
        draw_x = int(self.x)
        draw_y = int(self.y)
        
        if self.bullet_type == "basic":
            # 基本子彈：簡單矩形
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "laser":
            # 雷射：更細長的矩形
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "plasma":
            # 電漿彈：橢圓形
            pygame.draw.ellipse(screen, self.color, (draw_x, draw_y, self.width, self.height))
        elif self.bullet_type == "missile":
            # 飛彈：火箭形狀（向下）
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
            # 飛彈尾焰（在上方）
            from config import RED
            pygame.draw.polygon(screen, RED, [
                (draw_x + 2, draw_y),
                (draw_x + self.width - 2, draw_y),
                (draw_x + self.width // 2, draw_y - 8)
            ])
        elif self.bullet_type == "ion_cannon":
            # 離子砲：強力光束
            pygame.draw.rect(screen, self.color, (draw_x, draw_y, self.width, self.height))
            # 能量核心
            from config import WHITE
            pygame.draw.circle(screen, WHITE, (draw_x + self.width // 2, draw_y + self.height // 2), 3)
    
    def is_off_screen(self):
        """
        檢查機器人子彈是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果子彈已經離開螢幕返回 True\n
        """
        # 檢查是否超出螢幕邊界
        if self.x < -self.width or self.x > SCREEN_WIDTH:
            return True
        if self.y < -self.height or self.y > SCREEN_HEIGHT:
            return True
        return False