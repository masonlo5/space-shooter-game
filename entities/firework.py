######################載入套件######################
import pygame
import random
import math

######################煙火效果類別######################
class Firework:
    """
    煙火效果類別 - Boss 擊敗後的慶祝動畫\n
    \n
    負責處理:\n
    1. 煙火粒子的生成和移動\n
    2. 煙火爆炸效果\n
    3. 粒子的生命週期管理\n
    """
    
    def __init__(self, x, y):
        """
        初始化煙火\n
        \n
        參數:\n
        x (int): 爆炸中心 x 座標\n
        y (int): 爆炸中心 y 座標\n
        """
        self.x = x
        self.y = y
        self.particles = []
        self.life = 60  # 煙火持續時間
        
        # 匯入所需顏色
        from config import RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE
        
        # 生成煙火粒子
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'color': random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]),
                'life': random.randint(30, 60)
            }
            self.particles.append(particle)
    
    def update(self):
        """
        更新煙火狀態\n
        """
        self.life -= 1
        
        # 更新所有粒子
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # 重力效果
            particle['life'] -= 1
            
            # 移除死亡的粒子
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        """
        繪製煙火\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 3)
    
    def is_dead(self):
        """
        檢查煙火是否結束\n
        \n
        回傳:\n
        bool: 如果煙火已結束返回 True\n
        """
        return len(self.particles) == 0 or self.life <= 0