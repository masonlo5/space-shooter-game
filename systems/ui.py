######################載入套件######################
import pygame
from config import *

######################UI系統類別######################
class UISystem:
    """
    UI系統類別 - 負責繪製所有使用者介面元素\n
    \n
    負責處理:\n
    1. 遊戲資訊顯示（生命值、分數、星星等）\n
    2. 操作說明顯示\n
    3. 商店解鎖提示\n
    4. 勝利訊息顯示\n
    """
    
    def __init__(self):
        """
        初始化UI系統\n
        """
        # 初始化字體
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_ui(self, screen, player, score, stars):
        """
        繪製遊戲 UI 介面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        player (Player): 玩家物件\n
        score (int): 目前分數\n
        stars (int): 星星數量\n
        """
        # 繪製生命值條
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 10
        health_bar_y = 10
        
        # 生命值背景（紅色）
        pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # 生命值前景（綠色）
        health_percentage = max(0, player.health / player.max_health)
        current_health_width = int(health_bar_width * health_percentage)
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))
        
        # 生命值邊框
        pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        
        # 生命值文字
        health_text = self.small_font.render(f"Health: {player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (health_bar_x, health_bar_y + health_bar_height + 5))
        
        # 分數顯示
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 60))
        
        # 星星數量顯示
        stars_text = self.font.render(f"Stars: {stars}", True, YELLOW)
        screen.blit(stars_text, (10, 100))
        
        # 當前武器顯示
        weapon_text = self.small_font.render(f"Weapon: {player.current_weapon.title()}", True, WHITE)
        screen.blit(weapon_text, (10, 140))
        
        # 當前太空船顯示
        ship_text = self.small_font.render(f"Ship: {player.spaceship_type.title()}", True, WHITE)
        screen.blit(ship_text, (10, 160))
        
        # 特殊攻擊冷卻顯示
        if player.special_attack_cooldown > 0:
            special_text = self.small_font.render(f"Special Attack: {player.special_attack_cooldown // 60 + 1}s", True, RED)
        else:
            special_text = self.small_font.render("Special Attack: Ready!", True, GREEN)
        screen.blit(special_text, (10, 180))
        
        # 操作說明
        controls_y = SCREEN_HEIGHT - 120
        controls = [
            "Controls:",
            "Arrow Keys / WASD: Move",
            "Ctrl/Shift: Shoot",
            "Space: Change Weapon",
            "C: Change Ship",
            "X: Special Attack"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, WHITE)
            screen.blit(control_text, (10, controls_y + i * 20))
        
        # 解鎖商店提示
        if stars >= SHOP_UNLOCK_STARS:
            unlock_text = self.small_font.render("Press 'S' to open Shop!", True, GREEN)
            screen.blit(unlock_text, (SCREEN_WIDTH - 200, 10))
        else:
            need_stars = SHOP_UNLOCK_STARS - stars
            unlock_text = self.small_font.render(f"Need {need_stars} stars for Shop", True, WHITE)
            screen.blit(unlock_text, (SCREEN_WIDTH - 200, 10))
    
    def draw_victory_message(self, screen, victory_timer):
        """
        繪製勝利訊息\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        victory_timer (int): 勝利計時器\n
        """
        if victory_timer > 0:
            victory_text = self.font.render("SUCCESS!", True, YELLOW)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # 勝利訊息背景
            pygame.draw.rect(screen, BLACK, 
                           (victory_rect.x - 20, victory_rect.y - 10, 
                            victory_rect.width + 40, victory_rect.height + 20))
            pygame.draw.rect(screen, YELLOW, 
                           (victory_rect.x - 20, victory_rect.y - 10, 
                            victory_rect.width + 40, victory_rect.height + 20), 3)
            
            screen.blit(victory_text, victory_rect)