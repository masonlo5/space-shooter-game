######################載入套件######################
import pygame
import math
import random
from config import *

######################盟友太空船類別######################
class AllyShip:
    """
    盟友太空船類別 - Boss Fight 模式中的自動戰鬥盟友\n
    \n
    負責處理:\n
    1. 跟隨玩家移動\n
    2. 自動瞄準和射擊Boss\n
    3. 閃避Boss攻擊\n
    4. 視覺效果和動畫\n
    \n
    屬性:\n
    x (float): 太空船的 x 座標\n
    y (float): 太空船的 y 座標\n
    width (int): 太空船寬度\n
    height (int): 太空船高度\n
    target_x (float): 目標 x 座標\n
    target_y (float): 目標 y 座標\n
    """
    
    def __init__(self, x, y, side="left"):
        """
        初始化盟友太空船\n
        \n
        參數:\n
        x (float): 起始 x 座標\n
        y (float): 起始 y 座標\n
        side (str): 位置標識 ("left" 或 "right")\n
        """
        self.x = x
        self.y = y
        self.position = side  # 為了與 boss_fight.py 兼容
        self.side = side
        
        # 太空船屬性
        self.width = 30
        self.height = 25
        self.speed = 3
        self.max_health = 80
        self.health = self.max_health
        self.damage_flash_timer = 0
        
        # 跟隨玩家的偏移量
        if side == "left":
            self.offset_x = -60  # 左側偏移
            self.offset_y = -10
        else:
            self.offset_x = 60   # 右側偏移
            self.offset_y = -10
        
        # 目標位置
        self.target_x = x
        self.target_y = y
        
        # 射擊相關
        self.shoot_cooldown = 0
        self.shoot_interval = 45  # 每0.75秒射擊一次
        
        # 閃避相關
        self.dodge_timer = 0
        self.dodge_direction = 0
        
        # 動畫效果
        self.engine_flicker = 0
        
        # 顏色設定（左右不同顏色以便區分）
        if side == "left":
            self.primary_color = CYAN
            self.secondary_color = BLUE
        else:
            self.primary_color = GREEN
            self.secondary_color = (0, 200, 0)
    
    def update(self, player, boss, boss_bullets):
        """
        更新盟友太空船狀態\n
        \n
        參數:\n
        player (Player): 玩家物件\n
        boss (BossFightBoss): Boss物件\n
        boss_bullets (list): Boss子彈列表\n
        \n
        回傳:\n
        list: 新產生的子彈列表\n
        """
        new_bullets = []
        
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # 更新閃避計時器
        if self.dodge_timer > 0:
            self.dodge_timer -= 1
        
        # 更新受傷閃爍計時器
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1
        
        # 更新引擎閃爍效果
        self.engine_flicker = (self.engine_flicker + 1) % 10
        
        # 跟隨玩家
        self._follow_player(player)
        
        # 閃避Boss子彈
        self._dodge_bullets(boss_bullets)
        
        # 移動到目標位置
        self._move_to_target()
        
        # 自動射擊Boss
        if boss and self.shoot_cooldown <= 0:
            bullet = self._shoot_at_boss(boss)
            if bullet:
                new_bullets.append(bullet)
                self.shoot_cooldown = self.shoot_interval
        
        return new_bullets
    
    def _follow_player(self, player):
        """
        跟隨玩家移動\n
        \n
        參數:\n
        player (Player): 玩家物件\n
        """
        # 計算跟隨位置
        self.target_x = player.x + self.offset_x
        self.target_y = player.y + self.offset_y
        
        # 確保不超出螢幕邊界
        self.target_x = max(0, min(SCREEN_WIDTH - self.width, self.target_x))
        self.target_y = max(0, min(SCREEN_HEIGHT - self.height, self.target_y))
    
    def _dodge_bullets(self, boss_bullets):
        """
        閃避Boss子彈\n
        \n
        參數:\n
        boss_bullets (list): Boss子彈列表\n
        """
        if self.dodge_timer > 0:
            return  # 正在閃避中
        
        # 檢查附近的危險子彈
        danger_distance = 80
        for bullet in boss_bullets:
            distance = math.sqrt((bullet.x - self.x)**2 + (bullet.y - self.y)**2)
            if distance < danger_distance:
                # 啟動閃避
                self.dodge_timer = 30  # 0.5秒閃避時間
                
                # 隨機選擇閃避方向
                if random.choice([True, False]):
                    self.dodge_direction = random.choice([-1, 1]) * 40
                else:
                    self.dodge_direction = 0
                
                break
    
    def _move_to_target(self):
        """
        移動到目標位置\n
        """
        # 如果正在閃避，應用閃避偏移
        target_x = self.target_x
        if self.dodge_timer > 0:
            target_x += self.dodge_direction
            target_x = max(0, min(SCREEN_WIDTH - self.width, target_x))
        
        # 平滑移動到目標位置
        dx = target_x - self.x
        dy = self.target_y - self.y
        
        # 限制移動速度
        if abs(dx) > self.speed:
            dx = self.speed if dx > 0 else -self.speed
        if abs(dy) > self.speed:
            dy = self.speed if dy > 0 else -self.speed
        
        self.x += dx
        self.y += dy
    
    def _shoot_at_boss(self, boss):
        """
        向Boss射擊\n
        \n
        參數:\n
        boss (BossFightBoss): Boss物件\n
        \n
        回傳:\n
        Bullet or None: 新產生的子彈\n
        """
        # 計算Boss中心位置
        boss_center_x = boss.x + boss.width // 2
        boss_center_y = boss.y + boss.height // 2
        
        # 計算射擊起點
        bullet_x = self.x + self.width // 2
        bullet_y = self.y
        
        # 計算射擊方向
        dx = boss_center_x - bullet_x
        dy = boss_center_y - bullet_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # 創建導向子彈
            from entities.bullet import Bullet
            bullet = Bullet(bullet_x - 2, bullet_y, "plasma")  # 使用等離子武器
            
            # 設定子彈方向（導向Boss）
            bullet.dx = (dx / distance) * 8  # 子彈速度
            bullet.dy = (dy / distance) * 8
            
            return bullet
        
        return None
    
    def draw(self, screen):
        """
        在螢幕上繪製盟友太空船\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 主體船身
        ship_points = [
            (self.x + self.width // 2, self.y),  # 船頭
            (self.x + 5, self.y + self.height),  # 左下角
            (self.x + self.width - 5, self.y + self.height)  # 右下角
        ]
        pygame.draw.polygon(screen, self.primary_color, ship_points)
        
        # 機翼
        pygame.draw.polygon(screen, self.secondary_color, [
            (self.x, self.y + 8), 
            (self.x + 8, self.y + 12), 
            (self.x + 3, self.y + 18)
        ])
        pygame.draw.polygon(screen, self.secondary_color, [
            (self.x + self.width, self.y + 8), 
            (self.x + self.width - 8, self.y + 12), 
            (self.x + self.width - 3, self.y + 18)
        ])
        
        # 引擎噴射效果（閃爍）
        if self.engine_flicker < 5:  # 50%機率顯示引擎火焰
            engine_width = 4
            engine_height = 8
            left_engine_x = self.x + 6
            right_engine_x = self.x + self.width - 10
            engine_y = self.y + self.height
            
            pygame.draw.rect(screen, ORANGE, (left_engine_x, engine_y, engine_width, engine_height))
            pygame.draw.rect(screen, ORANGE, (right_engine_x, engine_y, engine_width, engine_height))
        
        # 如果正在閃避，顯示警告效果
        if self.dodge_timer > 0:
            # 閃爍邊框表示閃避狀態
            if (self.dodge_timer // 5) % 2:
                pygame.draw.rect(screen, YELLOW, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)
        
        # 側邊標識（區分左右盟友）
        if self.side == "left":
            pygame.draw.circle(screen, WHITE, (self.x + 5, self.y + 5), 2)
        else:
            pygame.draw.circle(screen, WHITE, (self.x + self.width - 5, self.y + 5), 2)
        
        # 受傷閃爍效果
        if self.damage_flash_timer > 0 and (self.damage_flash_timer // 3) % 2:
            # 紅色覆蓋層表示受傷
            damage_surface = pygame.Surface((self.width, self.height))
            damage_surface.set_alpha(128)  # 半透明
            damage_surface.fill(RED)
            screen.blit(damage_surface, (self.x, self.y))
    
    def is_off_screen(self):
        """
        檢查太空船是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果太空船已經離開螢幕返回 True\n
        """
        return (self.x < -self.width or self.x > SCREEN_WIDTH or 
                self.y < -self.height or self.y > SCREEN_HEIGHT)
    
    def take_damage(self, damage):
        """
        受到傷害\n
        \n
        參數:\n
        damage (int): 傷害值\n
        """
        self.health = max(0, self.health - damage)
        
        # 受傷閃爍效果
        self.damage_flash_timer = 10
        
        if self.health <= 0:
            print(f"盟友太空船 ({self.side}) 被摧毀！")