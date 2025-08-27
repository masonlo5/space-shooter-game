######################載入套件######################
import pygame
import random
import math
from config import *

######################雪花粒子類別######################
class Snowflake:
    """
    雪花粒子類別 - 用於勝利時的雪花效果\n
    \n
    負責處理:\n
    1. 雪花的生成和移動\n
    2. 雪花的外觀繪製\n
    3. 雪花的生命週期管理\n
    \n
    屬性:\n
    x (float): 雪花的 x 座標\n
    y (float): 雪花的 y 座標\n
    size (int): 雪花大小\n
    fall_speed (float): 下降速度\n
    drift_speed (float): 水平漂移速度\n
    """
    
    def __init__(self, x=None, y=None):
        """
        初始化雪花\n
        \n
        參數:\n
        x (int): 起始 x 座標，None 時隨機生成\n
        y (int): 起始 y 座標，None 時隨機生成\n
        """
        # 位置設定
        if x is None:
            self.x = random.randint(0, SCREEN_WIDTH)
        else:
            self.x = float(x)
        
        if y is None:
            self.y = random.randint(-50, 0)  # 從螢幕上方開始落下
        else:
            self.y = float(y)
        
        # 雪花屬性
        snowflake_config = SHIP_BATTLE_EFFECTS["snowflake"]
        self.size = random.randint(snowflake_config["size_min"], snowflake_config["size_max"])
        self.fall_speed = random.uniform(1, snowflake_config["fall_speed"])
        self.drift_speed = random.uniform(-0.5, 0.5)  # 左右漂移
        
        # 視覺效果
        self.alpha = random.randint(150, 255)  # 透明度
        self.rotation = random.uniform(0, 360)  # 旋轉角度
        self.rotation_speed = random.uniform(-2, 2)  # 旋轉速度
    
    def update(self):
        """
        更新雪花狀態\n
        """
        # 下降移動
        self.y += self.fall_speed
        self.x += self.drift_speed
        
        # 旋轉
        self.rotation += self.rotation_speed
        
        # 邊界處理：雪花從左右邊緣重新進入
        if self.x < -10:
            self.x = SCREEN_WIDTH + 10
        elif self.x > SCREEN_WIDTH + 10:
            self.x = -10
    
    def draw(self, screen):
        """
        繪製雪花\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 創建帶透明度的表面
        snowflake_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # 繪製六角雪花
        center = (self.size, self.size)
        
        # 雪花的六個分支
        for i in range(6):
            angle = math.radians(self.rotation + i * 60)
            end_x = center[0] + self.size * math.cos(angle)
            end_y = center[1] + self.size * math.sin(angle)
            
            # 主要分支
            pygame.draw.line(snowflake_surface, (*WHITE, self.alpha), 
                           center, (end_x, end_y), 1)
            
            # 小分支
            if self.size > 2:
                branch_x = center[0] + (self.size * 0.6) * math.cos(angle)
                branch_y = center[1] + (self.size * 0.6) * math.sin(angle)
                
                # 左小分支
                small_angle = angle - math.radians(30)
                small_end_x = branch_x + (self.size * 0.3) * math.cos(small_angle)
                small_end_y = branch_y + (self.size * 0.3) * math.sin(small_angle)
                pygame.draw.line(snowflake_surface, (*WHITE, self.alpha), 
                               (branch_x, branch_y), (small_end_x, small_end_y), 1)
                
                # 右小分支
                small_angle = angle + math.radians(30)
                small_end_x = branch_x + (self.size * 0.3) * math.cos(small_angle)
                small_end_y = branch_y + (self.size * 0.3) * math.sin(small_angle)
                pygame.draw.line(snowflake_surface, (*WHITE, self.alpha), 
                               (branch_x, branch_y), (small_end_x, small_end_y), 1)
        
        # 將雪花繪製到主畫面
        screen.blit(snowflake_surface, (self.x - self.size, self.y - self.size))
    
    def is_off_screen(self):
        """
        檢查雪花是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果雪花已經離開螢幕底部返回 True\n
        """
        return self.y > SCREEN_HEIGHT + 10

######################烏鴉粒子類別######################
class Crow:
    """
    烏鴉粒子類別 - 用於失敗時的烏鴉效果\n
    \n
    負責處理:\n
    1. 烏鴉的飛行軌跡\n
    2. 烏鴉的外觀繪製\n
    3. 烏鴉的生命週期管理\n
    \n
    屬性:\n
    x (float): 烏鴉的 x 座標\n
    y (float): 烏鴉的 y 座標\n
    width (int): 烏鴉寬度\n
    height (int): 烏鴉高度\n
    fly_speed (float): 飛行速度\n
    wing_flap (float): 翅膀拍動狀態\n
    """
    
    def __init__(self, x=None, y=None):
        """
        初始化烏鴉\n
        \n
        參數:\n
        x (int): 起始 x 座標，None 時從左側開始\n
        y (int): 起始 y 座標，None 時隨機高度\n
        """
        # 位置設定
        if x is None:
            self.x = -50  # 從螢幕左側開始
        else:
            self.x = float(x)
        
        if y is None:
            self.y = random.randint(50, SCREEN_HEIGHT // 2)  # 在螢幕上半部飛行
        else:
            self.y = float(y)
        
        # 烏鴉屬性
        crow_config = SHIP_BATTLE_EFFECTS["crow"]
        self.width = crow_config["width"]
        self.height = crow_config["height"]
        self.fly_speed = random.uniform(crow_config["fly_speed"] * 0.8, crow_config["fly_speed"] * 1.2)
        
        # 飛行效果
        self.wing_flap = 0  # 翅膀拍動週期
        self.wing_flap_speed = random.uniform(0.2, 0.4)
        self.vertical_offset = random.uniform(-1, 1)  # 垂直移動偏移
    
    def update(self):
        """
        更新烏鴉狀態\n
        """
        # 水平飛行
        self.x += self.fly_speed
        
        # 輕微的垂直波動（模擬真實飛行）
        self.y += math.sin(self.wing_flap) * self.vertical_offset
        
        # 翅膀拍動
        self.wing_flap += self.wing_flap_speed
    
    def draw(self, screen):
        """
        繪製烏鴉\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 烏鴉身體（橢圓形）
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.ellipse(screen, BLACK, body_rect)
        
        # 翅膀（根據拍動週期變化）
        wing_flap_factor = math.sin(self.wing_flap)
        wing_height = self.height // 3
        
        # 左翅膀
        left_wing_points = [
            (self.x, self.y + self.height // 3),
            (self.x - self.width // 2, self.y + wing_height + wing_flap_factor * 3),
            (self.x + self.width // 4, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, BLACK, left_wing_points)
        
        # 右翅膀
        right_wing_points = [
            (self.x + self.width, self.y + self.height // 3),
            (self.x + self.width + self.width // 2, self.y + wing_height + wing_flap_factor * 3),
            (self.x + self.width - self.width // 4, self.y + self.height // 2)
        ]
        pygame.draw.polygon(screen, BLACK, right_wing_points)
        
        # 烏鴉頭部（小圓圈）
        head_radius = self.height // 4
        head_x = self.x + self.width + head_radius
        head_y = self.y + self.height // 3
        pygame.draw.circle(screen, BLACK, (int(head_x), int(head_y)), head_radius)
        
        # 烏鴉嘴巴（小三角形）
        beak_points = [
            (head_x + head_radius, head_y),
            (head_x + head_radius + 8, head_y - 2),
            (head_x + head_radius + 8, head_y + 2)
        ]
        pygame.draw.polygon(screen, (50, 50, 50), beak_points)
    
    def is_off_screen(self):
        """
        檢查烏鴉是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果烏鴉已經飛出螢幕右側返回 True\n
        """
        return self.x > SCREEN_WIDTH + 50

######################視覺效果系統類別######################
class VisualEffectsSystem:
    """
    視覺效果系統類別 - 管理 Ship Battle 模式的視覺效果\n
    \n
    負責處理:\n
    1. 勝利時的雪花效果\n
    2. 失敗時的烏鴉效果\n
    3. 粒子系統的更新和渲染\n
    \n
    屬性:\n
    snowflakes (list): 雪花粒子列表\n
    crows (list): 烏鴉粒子列表\n
    effect_type (str): 當前效果類型\n
    """
    
    def __init__(self):
        """
        初始化視覺效果系統\n
        """
        self.snowflakes = []
        self.crows = []
        self.effect_type = None  # "victory", "defeat", None
        self.effect_timer = 0
        
        print("視覺效果系統初始化完成")
    
    def start_victory_effect(self):
        """
        開始勝利效果（雪花）\n
        """
        print("開始播放勝利效果 - 雪花飛舞")
        self.effect_type = "victory"
        self.effect_timer = 0
        self.snowflakes.clear()
        self.crows.clear()
        
        # 創建初始雪花
        snowflake_count = SHIP_BATTLE_EFFECTS["snowflake"]["count"]
        for _ in range(snowflake_count):
            self.snowflakes.append(Snowflake())
    
    def start_defeat_effect(self):
        """
        開始失敗效果（烏鴉飛過）\n
        """
        print("開始播放失敗效果 - 烏鴉飛過")
        self.effect_type = "defeat"
        self.effect_timer = 0
        self.snowflakes.clear()
        self.crows.clear()
        
        # 創建烏鴉群（延遲出現）
        crow_count = SHIP_BATTLE_EFFECTS["crow"]["count"]
        for i in range(crow_count):
            delay_x = -50 - (i * 40)  # 每隻烏鴉間隔40像素
            crow_y = random.randint(80, SCREEN_HEIGHT // 2)
            crow = Crow(delay_x, crow_y)
            self.crows.append(crow)
    
    def update(self):
        """
        更新視覺效果\n
        """
        if self.effect_type is None:
            return
        
        self.effect_timer += 1
        
        if self.effect_type == "victory":
            # 更新雪花效果
            self._update_snowflakes()
        elif self.effect_type == "defeat":
            # 更新烏鴉效果
            self._update_crows()
    
    def _update_snowflakes(self):
        """
        更新雪花效果\n
        """
        # 更新現有雪花
        for snowflake in self.snowflakes[:]:
            snowflake.update()
            if snowflake.is_off_screen():
                self.snowflakes.remove(snowflake)
        
        # 持續生成新雪花（每5幀生成一片）
        if self.effect_timer % 5 == 0:
            self.snowflakes.append(Snowflake())
        
        # 限制雪花數量，避免效能問題
        max_snowflakes = SHIP_BATTLE_EFFECTS["snowflake"]["count"] * 2
        if len(self.snowflakes) > max_snowflakes:
            self.snowflakes = self.snowflakes[-max_snowflakes:]
    
    def _update_crows(self):
        """
        更新烏鴉效果\n
        """
        # 更新現有烏鴉
        for crow in self.crows[:]:
            crow.update()
            if crow.is_off_screen():
                self.crows.remove(crow)
    
    def draw(self, screen):
        """
        繪製視覺效果\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        if self.effect_type == "victory":
            # 繪製雪花
            for snowflake in self.snowflakes:
                snowflake.draw(screen)
        elif self.effect_type == "defeat":
            # 繪製烏鴉
            for crow in self.crows:
                crow.draw(screen)
    
    def is_effect_active(self):
        """
        檢查是否有效果正在播放\n
        \n
        回傳:\n
        bool: 如果有效果正在播放返回 True\n
        """
        return self.effect_type is not None and (self.snowflakes or self.crows)
    
    def stop_effects(self):
        """
        停止所有效果\n
        """
        self.effect_type = None
        self.effect_timer = 0
        self.snowflakes.clear()
        self.crows.clear()
        print("視覺效果已停止")