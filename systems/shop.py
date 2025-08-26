######################載入套件######################
import pygame
from config import *

######################商店系統類別######################
class ShopSystem:
    """
    商店系統類別 - 負責處理商店的顯示和購買邏輯\n
    \n
    負責處理:\n
    1. 商店介面繪製\n
    2. 商品列表顯示\n
    3. 購買邏輯處理\n
    4. 價格檢查和物品解鎖\n
    """
    
    def __init__(self):
        """
        初始化商店系統\n
        """
        # 初始化字體
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_shop(self, screen, stars):
        """
        繪製商店介面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        stars (int): 目前星星數量\n
        """
        # 商店背景
        pygame.draw.rect(screen, (50, 50, 100), (100, 100, 600, 400))
        pygame.draw.rect(screen, WHITE, (100, 100, 600, 400), 3)
        
        # 商店標題
        title_text = self.font.render("SPACE SHOP", True, WHITE)
        title_rect = title_text.get_rect(center=(400, 130))
        screen.blit(title_text, title_rect)
        
        # 星星數量顯示
        stars_text = self.small_font.render(f"Stars: {stars}", True, YELLOW)
        screen.blit(stars_text, (120, 150))
        
        # 商品項目
        items = [
            {"name": "Health Potion", "price": 5, "key": "1"},
            {"name": "Speed Boost", "price": 10, "key": "2"},
            {"name": "Laser Weapon", "price": 15, "key": "3"},
            {"name": "Plasma Weapon", "price": 25, "key": "4"},
            {"name": "Missile Launcher", "price": 50, "key": "5"},
            {"name": "Ion Cannon", "price": 80, "key": "6"},
            {"name": "Fighter Ship", "price": 40, "key": "7"},
            {"name": "Interceptor Ship", "price": 80, "key": "8"},
            {"name": "Destroyer Ship", "price": 120, "key": "9"},
            {"name": "Battleship", "price": 200, "key": "0"}
        ]
        
        y_offset = 180
        for i, item in enumerate(items):
            # 商品名稱和價格
            item_text = self.small_font.render(f"{item['key']}. {item['name']} - {item['price']} stars", True, WHITE)
            
            # 檢查是否買得起
            if stars >= item['price']:
                color = GREEN
            else:
                color = RED
                
            screen.blit(item_text, (120, y_offset + i * 30))
            
            # 價格顏色標示
            price_text = self.small_font.render(f"{item['price']}", True, color)
            screen.blit(price_text, (350, y_offset + i * 30))
        
        # 操作說明
        instructions = [
            "Press number key to buy item",
            "Press ESC to close shop",
            "Items 7-0 are spaceships"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = self.small_font.render(instruction, True, WHITE)
            screen.blit(instruction_text, (120, 350 + i * 25))
    
    def handle_purchase(self, key, player, stars):
        """
        處理商店購買邏輯\n
        \n
        參數:\n
        key (int): 按下的按鍵（1-0）\n
        player (Player): 玩家物件\n
        stars (int): 目前星星數量\n
        \n
        回傳:\n
        int: 購買後剩餘的星星數量\n
        """
        if key == pygame.K_1 and stars >= 5:  # Health Potion
            player.health = min(player.max_health, player.health + 50)
            return stars - 5
        elif key == pygame.K_2 and stars >= 10:  # Speed Boost
            player.speed = min(10, player.speed + 1)
            return stars - 10
        elif key == pygame.K_3 and stars >= 15:  # Laser Weapon
            if "laser" not in player.unlocked_weapons:
                player.unlocked_weapons.append("laser")
            player.current_weapon = "laser"
            return stars - 15
        elif key == pygame.K_4 and stars >= 25:  # Plasma Weapon
            if "plasma" not in player.unlocked_weapons:
                player.unlocked_weapons.append("plasma")
            player.current_weapon = "plasma"
            return stars - 25
        elif key == pygame.K_5 and stars >= 50:  # Missile Launcher
            if "missile" not in player.unlocked_weapons:
                player.unlocked_weapons.append("missile")
            player.current_weapon = "missile"
            return stars - 50
        elif key == pygame.K_6 and stars >= 80:  # Ion Cannon
            if "ion_cannon" not in player.unlocked_weapons:
                player.unlocked_weapons.append("ion_cannon")
            player.current_weapon = "ion_cannon"
            return stars - 80
        elif key == pygame.K_7 and stars >= 40:  # Fighter Ship
            if "fighter" not in player.unlocked_ships:
                player.unlocked_ships.append("fighter")
            player.spaceship_type = "fighter"
            player.update_ship_stats()
            return stars - 40
        elif key == pygame.K_8 and stars >= 80:  # Interceptor Ship
            if "interceptor" not in player.unlocked_ships:
                player.unlocked_ships.append("interceptor")
            player.spaceship_type = "interceptor"
            player.update_ship_stats()
            return stars - 80
        elif key == pygame.K_9 and stars >= 120:  # Destroyer Ship
            if "destroyer" not in player.unlocked_ships:
                player.unlocked_ships.append("destroyer")
            player.spaceship_type = "destroyer"
            player.update_ship_stats()
            return stars - 120
        elif key == pygame.K_0 and stars >= 200:  # Battleship
            if "battleship" not in player.unlocked_ships:
                player.unlocked_ships.append("battleship")
            player.spaceship_type = "battleship"
            player.update_ship_stats()
            return stars - 200
        
        return stars