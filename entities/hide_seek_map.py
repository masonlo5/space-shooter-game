######################載入套件######################
import pygame
import random
import math
from config import *

######################躲貓貓地圖類別######################
class HideSeekMap:
    """
    躲貓貓地圖類別 - 負責生成隨機地圖和障礙物\n
    \n
    負責處理:\n
    1. 隨機地圖佈局生成\n
    2. 障礙物位置計算和碰撞檢測\n
    3. 安全位置尋找（用於玩家傳送）\n
    4. 地圖背景和環境渲染\n
    5. 小地圖資訊提供\n
    """
    
    def __init__(self, seed=None):
        """
        初始化躲貓貓地圖\n
        \n
        參數:\n
        seed (int): 隨機種子，用於生成固定地圖佈局\n
        """
        # 設定隨機種子（如果提供）
        if seed is not None:
            random.seed(seed)
            self.seed = seed
        else:
            self.seed = random.randint(1, 10000)
            random.seed(self.seed)
        
        # 地圖基本屬性
        self.width = HIDE_SEEK_MAP["map_width"]
        self.height = HIDE_SEEK_MAP["map_height"]
        
        # 生成障礙物
        self.obstacles = []
        self._generate_obstacles()
        
        # 生成背景裝飾元素
        self.decorations = []
        self._generate_decorations()
        
        # 生成安全區域（用於玩家傳送）
        self.safe_zones = []
        self._calculate_safe_zones()
        
        print(f"躲貓貓地圖生成完成，種子：{self.seed}，障礙物數量：{len(self.obstacles)}")
    
    def _generate_obstacles(self):
        """
        生成隨機障礙物\n
        """
        obstacle_count = HIDE_SEEK_MAP["obstacle_count"]
        min_size = HIDE_SEEK_MAP["obstacle_min_size"]
        max_size = HIDE_SEEK_MAP["obstacle_max_size"]
        
        # 確保中央區域保持暢通（作為初始出生點）
        spawn_area = HIDE_SEEK_MAP["spawn_area_size"]
        center_x = self.width // 2
        center_y = self.height // 2
        
        attempts = 0
        max_attempts = obstacle_count * 10
        
        while len(self.obstacles) < obstacle_count and attempts < max_attempts:
            attempts += 1
            
            # 隨機生成障礙物尺寸和位置
            width = random.randint(min_size, max_size)
            height = random.randint(min_size, max_size)
            x = random.randint(width // 2, self.width - width // 2)
            y = random.randint(height // 2, self.height - height // 2)
            
            obstacle_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
            
            # 檢查是否與中央出生區域重疊
            spawn_rect = pygame.Rect(center_x - spawn_area // 2, center_y - spawn_area // 2, 
                                   spawn_area, spawn_area)
            if obstacle_rect.colliderect(spawn_rect):
                continue
            
            # 檢查是否與現有障礙物重疊
            collision = False
            for existing_obstacle in self.obstacles:
                if obstacle_rect.colliderect(existing_obstacle):
                    collision = True
                    break
            
            # 檢查是否太靠近地圖邊界
            margin = 30
            if (obstacle_rect.left < margin or obstacle_rect.right > self.width - margin or
                obstacle_rect.top < margin or obstacle_rect.bottom > self.height - margin):
                continue
            
            # 如果沒有碰撞，添加障礙物
            if not collision:
                self.obstacles.append(obstacle_rect)
        
        print(f"成功生成 {len(self.obstacles)} 個障礙物")
    
    def _generate_decorations(self):
        """
        生成背景裝飾元素（星星、小行星等）\n
        """
        # 生成隨機星星作為背景裝飾
        star_count = 150
        for _ in range(star_count):
            star_x = random.randint(0, self.width)
            star_y = random.randint(0, self.height)
            star_size = random.randint(1, 3)
            star_brightness = random.randint(100, 255)
            
            decoration = {
                "type": "star",
                "x": star_x,
                "y": star_y,
                "size": star_size,
                "brightness": star_brightness
            }
            self.decorations.append(decoration)
        
        # 生成小行星裝飾
        asteroid_count = 20
        for _ in range(asteroid_count):
            asteroid_x = random.randint(50, self.width - 50)
            asteroid_y = random.randint(50, self.height - 50)
            asteroid_size = random.randint(8, 20)
            
            # 確保小行星不與障礙物重疊
            asteroid_rect = pygame.Rect(asteroid_x - asteroid_size, asteroid_y - asteroid_size,
                                      asteroid_size * 2, asteroid_size * 2)
            
            collision = False
            for obstacle in self.obstacles:
                if asteroid_rect.colliderect(obstacle):
                    collision = True
                    break
            
            if not collision:
                decoration = {
                    "type": "asteroid",
                    "x": asteroid_x,
                    "y": asteroid_y,
                    "size": asteroid_size,
                    "color": (random.randint(100, 150), random.randint(80, 120), random.randint(60, 100))
                }
                self.decorations.append(decoration)
    
    def _calculate_safe_zones(self):
        """
        計算安全區域（用於玩家傳送）\n
        """
        # 在地圖中尋找遠離障礙物的安全區域
        grid_size = 100
        safe_distance = HIDE_SEEK_MAP["safe_distance"]
        
        for x in range(safe_distance, self.width - safe_distance, grid_size):
            for y in range(safe_distance, self.height - safe_distance, grid_size):
                # 檢查這個位置是否遠離所有障礙物
                safe_rect = pygame.Rect(x - safe_distance // 2, y - safe_distance // 2,
                                      safe_distance, safe_distance)
                
                is_safe = True
                for obstacle in self.obstacles:
                    if safe_rect.colliderect(obstacle):
                        is_safe = False
                        break
                
                if is_safe:
                    self.safe_zones.append((x, y))
        
        print(f"找到 {len(self.safe_zones)} 個安全區域")
    
    def get_random_safe_position(self):
        """
        取得隨機安全位置\n
        \n
        回傳:\n
        tuple: (x, y) 安全座標，如果沒有安全位置則返回地圖中央\n
        """
        if self.safe_zones:
            return random.choice(self.safe_zones)
        else:
            # 如果沒有安全區域，返回地圖中央
            return (self.width // 2, self.height // 2)
    
    def get_spawn_positions(self, player_count):
        """
        取得玩家出生位置\n
        \n
        參數:\n
        player_count (int): 玩家數量\n
        \n
        回傳:\n
        list: [(x, y), ...] 出生位置列表\n
        """
        positions = []
        center_x = self.width // 2
        center_y = self.height // 2
        spawn_radius = HIDE_SEEK_MAP["spawn_area_size"] // 2
        
        # 在中央區域周圍均勻分布玩家
        for i in range(player_count):
            angle = (2 * math.pi * i) / player_count
            x = center_x + spawn_radius * 0.7 * math.cos(angle)
            y = center_y + spawn_radius * 0.7 * math.sin(angle)
            positions.append((int(x), int(y)))
        
        return positions
    
    def get_teleport_positions(self, player_count, existing_positions=None):
        """
        取得傳送位置（確保玩家間保持安全距離）\n
        \n
        參數:\n
        player_count (int): 需要傳送的玩家數量\n
        existing_positions (list): 現有位置列表（用於避免重疊）\n
        \n
        回傳:\n
        list: [(x, y), ...] 傳送位置列表\n
        """
        positions = []
        safe_distance = HIDE_SEEK_MAP["safe_distance"]
        max_attempts = 50
        
        for i in range(player_count):
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                
                # 從安全區域中選擇一個位置
                if self.safe_zones:
                    x, y = random.choice(self.safe_zones)
                else:
                    # 如果沒有安全區域，隨機選擇位置
                    x = random.randint(100, self.width - 100)
                    y = random.randint(100, self.height - 100)
                
                # 檢查與現有位置的距離
                valid_position = True
                
                # 檢查與已選位置的距離
                for existing_x, existing_y in positions:
                    distance = math.sqrt((x - existing_x)**2 + (y - existing_y)**2)
                    if distance < safe_distance:
                        valid_position = False
                        break
                
                # 檢查與傳入的現有位置的距離
                if valid_position and existing_positions:
                    for existing_x, existing_y in existing_positions:
                        distance = math.sqrt((x - existing_x)**2 + (y - existing_y)**2)
                        if distance < safe_distance:
                            valid_position = False
                            break
                
                # 檢查是否與障礙物碰撞
                if valid_position:
                    player_rect = pygame.Rect(x - 20, y - 15, 40, 30)  # 假設玩家大小
                    for obstacle in self.obstacles:
                        if player_rect.colliderect(obstacle):
                            valid_position = False
                            break
                
                if valid_position:
                    positions.append((x, y))
                    break
            
            # 如果找不到有效位置，使用隨機位置
            if len(positions) <= i:
                x = random.randint(100, self.width - 100)
                y = random.randint(100, self.height - 100)
                positions.append((x, y))
        
        return positions
    
    def is_position_safe(self, x, y, radius=25):
        """
        檢查位置是否安全（不與障礙物碰撞）\n
        \n
        參數:\n
        x (int): X座標\n
        y (int): Y座標\n
        radius (int): 檢查半徑\n
        \n
        回傳:\n
        bool: 位置是否安全\n
        """
        check_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        
        for obstacle in self.obstacles:
            if check_rect.colliderect(obstacle):
                return False
        
        return True
    
    def draw_background(self, screen, camera_x, camera_y):
        """
        繪製地圖背景\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        camera_x (int): 相機X偏移\n
        camera_y (int): 相機Y偏移\n
        """
        # 繪製太空背景
        space_color = (5, 5, 20)  # 深藍色太空
        screen.fill(space_color)
        
        # 繪製背景裝飾
        for decoration in self.decorations:
            screen_x = decoration["x"] - camera_x
            screen_y = decoration["y"] - camera_y
            
            # 只繪製在螢幕範圍內的裝飾
            if (-50 <= screen_x <= SCREEN_WIDTH + 50 and 
                -50 <= screen_y <= SCREEN_HEIGHT + 50):
                
                if decoration["type"] == "star":
                    brightness = decoration["brightness"]
                    star_color = (brightness, brightness, brightness)
                    pygame.draw.circle(screen, star_color, 
                                     (screen_x, screen_y), decoration["size"])
                
                elif decoration["type"] == "asteroid":
                    pygame.draw.circle(screen, decoration["color"],
                                     (screen_x, screen_y), decoration["size"])
                    # 添加陰影效果
                    shadow_color = tuple(max(0, c - 30) for c in decoration["color"])
                    pygame.draw.circle(screen, shadow_color,
                                     (screen_x + 2, screen_y + 2), decoration["size"] - 2)
    
    def draw_obstacles(self, screen, camera_x, camera_y):
        """
        繪製地圖障礙物\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        camera_x (int): 相機X偏移\n
        camera_y (int): 相機Y偏移\n
        """
        for obstacle in self.obstacles:
            # 計算螢幕位置
            screen_rect = pygame.Rect(obstacle.x - camera_x, obstacle.y - camera_y,
                                    obstacle.width, obstacle.height)
            
            # 只繪製在螢幕範圍內的障礙物
            if (screen_rect.right >= 0 and screen_rect.left <= SCREEN_WIDTH and
                screen_rect.bottom >= 0 and screen_rect.top <= SCREEN_HEIGHT):
                
                # 繪製障礙物（金屬質感）
                obstacle_color = (80, 80, 90)  # 暗灰色
                highlight_color = (120, 120, 130)  # 高光
                shadow_color = (40, 40, 50)  # 陰影
                
                # 主體
                pygame.draw.rect(screen, obstacle_color, screen_rect)
                
                # 高光（左上角）
                highlight_rect = pygame.Rect(screen_rect.x, screen_rect.y, 
                                           screen_rect.width, 3)
                pygame.draw.rect(screen, highlight_color, highlight_rect)
                highlight_rect = pygame.Rect(screen_rect.x, screen_rect.y, 
                                           3, screen_rect.height)
                pygame.draw.rect(screen, highlight_color, highlight_rect)
                
                # 陰影（右下角）
                shadow_rect = pygame.Rect(screen_rect.right - 3, screen_rect.y, 
                                        3, screen_rect.height)
                pygame.draw.rect(screen, shadow_color, shadow_rect)
                shadow_rect = pygame.Rect(screen_rect.x, screen_rect.bottom - 3, 
                                        screen_rect.width, 3)
                pygame.draw.rect(screen, shadow_color, shadow_rect)
                
                # 邊框
                pygame.draw.rect(screen, (60, 60, 70), screen_rect, 2)
    
    def draw_minimap_data(self):
        """
        提供小地圖繪製所需的資料\n
        \n
        回傳:\n
        dict: 包含地圖資訊的字典\n
        """
        return {
            "width": self.width,
            "height": self.height,
            "obstacles": self.obstacles
        }
    
    def get_obstacles(self):
        """
        取得障礙物列表\n
        \n
        回傳:\n
        list: 障礙物矩形列表\n
        """
        return self.obstacles
    
    def reset_map(self, new_seed=None):
        """
        重置地圖（生成新的地圖佈局）\n
        \n
        參數:\n
        new_seed (int): 新的隨機種子\n
        """
        self.__init__(new_seed)
        print("地圖已重置")