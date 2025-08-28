######################載入套件######################
import pygame
import math
import random
from config import *

######################Boss類別######################
class Boss:
    """
    Boss類別 - 處理Boss敵人的行為和攻擊模式\n
    \n
    負責處理:\n
    1. Boss在螢幕頂部的左右移動\n
    2. 每2秒發射垃圾攻擊\n
    3. 每5秒發射扇形散彈攻擊\n
    4. Boss血量管理和血量條顯示\n
    5. Boss被擊敗後的禮物掉落\n
    \n
    屬性:\n
    x (int): Boss的 x 座標\n
    y (int): Boss的 y 座標\n
    width (int): Boss寬度\n
    height (int): Boss高度\n
    health (int): 當前生命值\n
    max_health (int): 最大生命值\n
    speed (int): 移動速度\n
    direction (int): 移動方向（1右，-1左）\n
    garbage_attack_timer (int): 垃圾攻擊計時器\n
    special_attack_timer (int): 特殊攻擊計時器\n
    """
    
    def __init__(self, x, y):
        """
        初始化Boss\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        """
        self.x = x
        self.y = y
        
        # 從設定檔載入Boss屬性
        boss_stats = ENEMY_STATS["boss"]
        self.width = boss_stats["width"]
        self.height = boss_stats["height"]
        self.health = boss_stats["health"]
        self.max_health = boss_stats["health"]  # 記錄最大生命值
        self.speed = boss_stats["speed"]
        self.color = boss_stats["color"]
        self.score_value = boss_stats["score"]
        self.star_value = boss_stats["stars"]
        
        # 移動控制
        self.direction = 1  # 1表示向右，-1表示向左
        self.movement_counter = 0
        
        # 攻擊計時器
        self.garbage_attack_timer = 0
        self.special_attack_timer = 0
        
        # Boss類型標識
        self.enemy_type = "boss"
    
    def move(self):
        """
        移動Boss - 在螢幕頂部左右移動\n
        """
        self.movement_counter += 1
        
        # 左右移動
        self.x += self.speed * self.direction
        
        # 撞到邊界就改變方向
        if self.x <= 0:
            self.direction = 1
            self.x = 0
        elif self.x >= SCREEN_WIDTH - self.width:
            self.direction = -1
            self.x = SCREEN_WIDTH - self.width
        
        # 輕微的上下浮動效果
        self.y += math.sin(self.movement_counter * 0.05) * 0.5
        
        # 確保Boss不會移動到螢幕外
        self.y = max(10, min(100, self.y))
    
    def update(self, sounds=None):
        """
        更新Boss狀態 - 包含攻擊計時器和攻擊判斷\n
        \n
        參數:\n
        sounds (dict): 音效物件字典\n
        \n
        回傳:\n
        list: 產生的子彈清單\n
        """
        bullets = []
        
        # 更新攻擊計時器
        self.garbage_attack_timer += 1
        self.special_attack_timer += 1
        
        # 垃圾攻擊（每2秒）
        if self.garbage_attack_timer >= BOSS_GARBAGE_ATTACK_INTERVAL:
            self.garbage_attack_timer = 0
            new_bullets = self.garbage_attack()
            bullets.extend(new_bullets)
            # 播放Boss攻擊音效
            if new_bullets and sounds:
                from config import play_sound
                play_sound(sounds, "laser_shoot", volume=0.7)
        
        # 特殊攻擊（每5秒）
        if self.special_attack_timer >= BOSS_SPECIAL_ATTACK_INTERVAL:
            self.special_attack_timer = 0
            new_bullets = self.special_attack()
            bullets.extend(new_bullets)
            # 播放Boss特殊攻擊音效
            if new_bullets and sounds:
                from config import play_sound
                play_sound(sounds, "laser_shoot", volume=0.9)
        
        return bullets
    
    def garbage_attack(self):
        """
        垃圾攻擊 - 向玩家發射垃圾\n
        \n
        回傳:\n
        list: 垃圾子彈清單\n
        """
        from .bullet import Bullet
        
        bullets = []
        
        # 從Boss中心發射一個垃圾
        center_x = self.x + self.width // 2
        center_y = self.y + self.height
        
        # 創建垃圾子彈
        garbage_bullet = Bullet(center_x, center_y, "boss_garbage")
        bullets.append(garbage_bullet)
        
        return bullets
    
    def special_attack(self):
        """
        特殊攻擊 - 發射扇形散彈\n
        \n
        回傳:\n
        list: 散彈子彈清單\n
        """
        from .bullet import Bullet
        
        bullets = []
        
        # 從Boss中心發射扇形散彈
        center_x = self.x + self.width // 2
        center_y = self.y + self.height
        
        # 計算扇形角度範圍（120度扇形）
        start_angle = -60  # 起始角度
        angle_step = 120 / (BOSS_SPECIAL_BULLET_COUNT - 1)  # 角度間隔
        
        for i in range(BOSS_SPECIAL_BULLET_COUNT):
            angle = start_angle + (i * angle_step)
            
            # 創建扇形散彈
            spread_bullet = Bullet(center_x, center_y, "boss_spread", angle)
            bullets.append(spread_bullet)
        
        return bullets
    
    def draw(self, screen):
        """
        在螢幕上繪製Boss\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 主體 - 大型紫色矩形
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # 砲台 - 左右兩個紅色矩形
        cannon_width = 15
        cannon_height = 10
        pygame.draw.rect(screen, RED, 
                        (self.x + 10, self.y + self.height - 5, cannon_width, cannon_height))
        pygame.draw.rect(screen, RED, 
                        (self.x + self.width - cannon_width - 10, self.y + self.height - 5, 
                         cannon_width, cannon_height))
        
        # 核心 - 中央黃色圓形
        core_x = int(self.x + self.width // 2)
        core_y = int(self.y + self.height // 2)
        pygame.draw.circle(screen, YELLOW, (core_x, core_y), 12)
        
        # Boss外框
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # 危險標誌（紅色三角形警告）
        warning_size = 8
        warning_points = [
            (self.x + self.width // 2, self.y - warning_size),
            (self.x + self.width // 2 - warning_size, self.y),
            (self.x + self.width // 2 + warning_size, self.y)
        ]
        pygame.draw.polygon(screen, RED, warning_points)
    
    def draw_health_bar(self, screen):
        """
        在螢幕頂部繪製Boss血量條\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 血量條位置和尺寸
        bar_width = 300
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 10
        
        # 血量條背景（紅色）
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # 血量條前景（根據血量變色）
        health_percentage = max(0, self.health / self.max_health)
        current_health_width = int(bar_width * health_percentage)
        
        # 血量顏色：綠色 -> 黃色 -> 紅色
        if health_percentage > 0.6:
            health_color = GREEN
        elif health_percentage > 0.3:
            health_color = YELLOW
        else:
            health_color = ORANGE
        
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, current_health_width, bar_height))
        
        # 血量條邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Boss名稱和血量文字
        font = create_font(FONT_SIZES["normal"])
        boss_text = font.render(f"BOSS: {self.health}/{self.max_health}", True, WHITE)
        text_rect = boss_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_height + 15))
        screen.blit(boss_text, text_rect)
    
    def is_off_screen(self):
        """
        檢查Boss是否離開螢幕（Boss不會離開螢幕）\n
        \n
        回傳:\n
        bool: 永遠返回 False，因為Boss會留在螢幕內\n
        """
        return False
    
    def take_damage(self, damage):
        """
        受到傷害\n
        \n
        參數:\n
        damage (int): 受到的傷害值\n
        \n
        回傳:\n
        bool: 如果Boss死亡返回 True\n
        """
        self.health -= damage
        # 確保血量不會低於0
        self.health = max(0, self.health)
        return self.health <= 0
    
    def drop_gift(self):
        """
        Boss被擊敗後掉落禮物\n
        \n
        回傳:\n
        PowerUp: 禮物道具物件\n
        """
        from .powerup import PowerUp
        
        # 從Boss中心位置掉落禮物
        gift_x = self.x + self.width // 2
        gift_y = self.y + self.height // 2
        
        return PowerUp(gift_x, gift_y, "gift")