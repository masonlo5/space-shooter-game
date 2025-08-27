######################載入套件######################
import pygame
from config import *

######################幽靈類別######################
class Ghost:
    """
    幽靈類別 - 處理玩家死亡後的幽靈模式\n
    \n
    負責處理:\n
    1. 幽靈自由飛行移動\n
    2. 觀察模式（可看到所有玩家位置）\n
    3. 幽靈外觀渲染（半透明效果）\n
    4. 無法攻擊和使用道具\n
    5. 無法獲得遊戲勝利\n
    """
    
    def __init__(self, original_player):
        """
        從死亡的玩家創建幽靈\n
        \n
        參數:\n
        original_player (HideSeekPlayer): 原始玩家物件\n
        """
        self.player_id = original_player.player_id
        self.name = original_player.name
        self.is_human = original_player.is_human
        
        # 位置屬性
        self.x = original_player.x
        self.y = original_player.y
        self.width = 30
        self.height = 20
        self.speed = 6  # 幽靈移動較快
        
        # 幽靈特有屬性
        self.alive = False  # 幽靈不算活著
        self.is_ghost = True
        self.alpha = 100  # 半透明
        
        # 外觀屬性
        self.color = (150, 150, 150)  # 灰色
        
        # 相機相關（如果是真人玩家）
        if self.is_human:
            self.camera_x = 0
            self.camera_y = 0
            self._update_camera()
        
        print(f"玩家 {self.name} 變成幽靈")
    
    def update(self, keys):
        """
        更新幽靈狀態\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        \n
        回傳:\n
        str: 如果按下T鍵返回 "return_to_menu"，否則返回 None\n
        """
        # 處理移動
        if self.is_human:
            action = self._handle_human_movement(keys)
            if action:
                return action
        else:
            self._handle_ai_movement()
        
        return None
    
    def _handle_human_movement(self, keys):
        """
        處理真人幽靈玩家移動\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        \n
        回傳:\n
        str: 如果按下T鍵返回 "return_to_menu"，否則返回 None\n
        """
        # 檢查返回主畫面按鍵
        if keys[pygame.K_t]:
            print(f"幽靈 {self.name} 選擇返回主畫面")
            return "return_to_menu"
        
        # 幽靈可以自由飛行，不受地圖邊界限制（但有軟限制）
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
        
        # 應用移動（幽靈不受障礙物限制）
        self.x += dx
        self.y += dy
        
        # 軟性邊界限制（可以飛出地圖但不要太遠）
        max_boundary = max(HIDE_SEEK_MAP["map_width"], HIDE_SEEK_MAP["map_height"]) + 200
        self.x = max(-200, min(max_boundary, self.x))
        self.y = max(-200, min(max_boundary, self.y))
        
        # 更新相機
        self._update_camera()
        
        return None
    
    def _handle_ai_movement(self):
        """
        處理AI幽靈移動（簡單的隨機飛行）\n
        """
        import random
        
        # AI幽靈隨機移動
        if random.randint(1, 100) <= 5:  # 5%機率改變方向
            self.x += random.randint(-self.speed, self.speed)
            self.y += random.randint(-self.speed, self.speed)
            
            # 保持在地圖附近
            self.x = max(0, min(HIDE_SEEK_MAP["map_width"], self.x))
            self.y = max(0, min(HIDE_SEEK_MAP["map_height"], self.y))
    
    def _update_camera(self):
        """
        更新相機位置（讓幽靈保持在螢幕中央）\n
        """
        if not self.is_human:
            return
        
        # 計算相機偏移，讓幽靈保持在螢幕中央
        self.camera_x = self.x - SCREEN_WIDTH // 2
        self.camera_y = self.y - SCREEN_HEIGHT // 2
        
        # 幽靈的相機限制較寬鬆
        max_boundary = max(HIDE_SEEK_MAP["map_width"], HIDE_SEEK_MAP["map_height"]) + 200
        self.camera_x = max(-200, min(max_boundary - SCREEN_WIDTH, self.camera_x))
        self.camera_y = max(-200, min(max_boundary - SCREEN_HEIGHT, self.camera_y))
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """
        繪製幽靈\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        camera_x (int): 相機X偏移\n
        camera_y (int): 相機Y偏移\n
        """
        # 計算螢幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 如果超出螢幕範圍就不繪製
        if (screen_x < -self.width or screen_x > SCREEN_WIDTH + self.width or
            screen_y < -self.height or screen_y > SCREEN_HEIGHT + self.height):
            return
        
        # 創建半透明表面
        ghost_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 繪製幽靈形狀（波浪狀的幽靈）
        self._draw_ghost_shape(ghost_surface)
        
        # 將幽靈表面繪製到主螢幕
        screen.blit(ghost_surface, (screen_x - self.width // 2, screen_y - self.height // 2))
        
        # 繪製幽靈名稱
        self._draw_ghost_name(screen, screen_x, screen_y)
    
    def _draw_ghost_shape(self, surface):
        """
        繪製幽靈形狀\n
        \n
        參數:\n
        surface (pygame.Surface): 繪製表面\n
        """
        import math
        
        # 幽靈主體（橢圓形）
        ghost_color = (*self.color, self.alpha)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 繪製幽靈主體
        pygame.draw.ellipse(surface, ghost_color, (5, 5, self.width-10, self.height-10))
        
        # 繪製幽靈的眼睛
        eye_color = (255, 255, 255, self.alpha + 50)
        left_eye_x = center_x - 6
        right_eye_x = center_x + 6
        eye_y = center_y - 3
        
        pygame.draw.circle(surface, eye_color, (left_eye_x, eye_y), 2)
        pygame.draw.circle(surface, eye_color, (right_eye_x, eye_y), 2)
        
        # 繪製波浪狀的下擺
        wave_points = []
        for i in range(0, self.width, 3):
            wave_y = self.height - 5 + int(3 * math.sin(i * 0.5 + pygame.time.get_ticks() * 0.01))
            wave_points.append((i, wave_y))
        
        if len(wave_points) > 2:
            pygame.draw.lines(surface, ghost_color, False, wave_points, 2)
    
    def _draw_ghost_name(self, screen, x, y):
        """
        繪製幽靈名稱\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        x (int): 螢幕X座標\n
        y (int): 螢幕Y座標\n
        """
        font = pygame.font.Font(None, 18)
        name_text = font.render(f"{self.name} (幽靈)", True, self.color)
        name_rect = name_text.get_rect(center=(x, y + self.height // 2 + 12))
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        """
        取得幽靈的碰撞矩形（幽靈不參與碰撞）\n
        \n
        回傳:\n
        pygame.Rect: 空矩形\n
        """
        return pygame.Rect(0, 0, 0, 0)  # 幽靈不參與碰撞