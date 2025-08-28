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
        self.font = create_font(FONT_SIZES["medium"])
        self.small_font = create_font(FONT_SIZES["normal"])
    
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
        
        # 藥水庫存顯示
        potions_y = 200
        
        # 回血藥水
        health_potion_text = self.small_font.render(f"Health Potions: {player.health_potions} (Press 1)", True, GREEN)
        screen.blit(health_potion_text, (10, potions_y))
        
        # 加速藥水
        speed_potion_text = self.small_font.render(f"Speed Potions: {player.speed_potions} (Press 2)", True, BLUE)
        screen.blit(speed_potion_text, (10, potions_y + 20))
        
        # 防護藥水
        protect_potion_text = self.small_font.render(f"Protect Potions: {player.protect_potions} (Press 3)", True, PURPLE)
        screen.blit(protect_potion_text, (10, potions_y + 40))
        
        # 藥水效果狀態顯示
        effects_y = potions_y + 60
        if player.speed_boost_timer > 0:
            speed_effect_text = self.small_font.render(f"Speed Boost: {player.speed_boost_timer // 60 + 1}s", True, CYAN)
            screen.blit(speed_effect_text, (10, effects_y))
            effects_y += 20
        
        if player.protect_boost_timer > 0:
            protect_effect_text = self.small_font.render(f"Protection: {player.protect_boost_timer // 60 + 1}s", True, YELLOW)
            screen.blit(protect_effect_text, (10, effects_y))
        
        # 操作說明（調整位置以避免與藥水顯示重疊）
        controls_y = SCREEN_HEIGHT - 140
        controls = [
            "Controls:",
            "Arrow Keys / WASD: Move",
            "Ctrl/Shift: Shoot",
            "Space: Change Weapon",
            "C: Change Ship",
            "X: Special Attack",
            "1/2/3: Use Potions"
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
    
    def draw_ship_battle_ui(self, screen, battle_info):
        """
        繪製 Ship Battle 模式的 UI 介面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        battle_info (dict): 戰鬥資訊字典\n
        """
        if not battle_info:
            return
        
        battle_state = battle_info.get("battle_state", "inactive")
        
        if battle_state == "prepare":
            # 準備階段：顯示雙方名稱和倒數計時
            self._draw_prepare_screen(screen, battle_info)
        
        elif battle_state == "fighting":
            # 戰鬥階段：顯示血量條和操作說明
            self._draw_fighting_ui(screen, battle_info)
        
        elif battle_state in ["victory", "defeat"]:
            # 結果階段：顯示勝負結果
            self._draw_result_screen(screen, battle_info)
    
    def _draw_prepare_screen(self, screen, battle_info):
        """
        繪製準備階段畫面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        battle_info (dict): 戰鬥資訊字典\n
        """
        prepare_timer = battle_info.get("prepare_timer", 0)
        player_name = battle_info.get("player_name", "Player")
        robot_name = battle_info.get("robot_name", "RoboWarrior")
        
        # 半透明黑色背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 標題
        title_font = create_font(SHIP_BATTLE_UI["prepare_font_size"])
        title_text = title_font.render("Ship Battle", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # 對戰雙方名稱
        name_font = create_font(SHIP_BATTLE_UI["name_font_size"])
        
        # 玩家名稱（左側）
        player_text = name_font.render(player_name, True, GREEN)
        player_rect = player_text.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        screen.blit(player_text, player_rect)
        
        # VS 文字（中央）
        vs_text = name_font.render("VS", True, YELLOW)
        vs_rect = vs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(vs_text, vs_rect)
        
        # 機器人名稱（右側）
        robot_text = name_font.render(robot_name, True, RED)
        robot_rect = robot_text.get_rect(center=(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2))
        screen.blit(robot_text, robot_rect)
        
        # 倒數計時
        countdown_seconds = (prepare_timer // 60) + 1
        countdown_text = title_font.render(f"戰鬥開始倒數: {countdown_seconds}", True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(countdown_text, countdown_rect)
    
    def _draw_fighting_ui(self, screen, battle_info):
        """
        繪製戰鬥階段 UI\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        battle_info (dict): 戰鬥資訊字典\n
        """
        # 玩家血量條（左上角）
        self._draw_health_bar(
            screen,
            battle_info.get("player_name", "Player"),
            battle_info.get("player_health", 100),
            battle_info.get("player_max_health", 100),
            battle_info.get("player_potions", 0),
            SHIP_BATTLE_UI["player_health_x"],
            SHIP_BATTLE_UI["health_bar_y"],
            GREEN
        )
        
        # 機器人血量條（右上角）
        self._draw_health_bar(
            screen,
            battle_info.get("robot_name", "RoboWarrior"),
            battle_info.get("robot_health", 100),
            battle_info.get("robot_max_health", 100),
            battle_info.get("robot_potions", 0),
            SHIP_BATTLE_UI["robot_health_x"],
            SHIP_BATTLE_UI["health_bar_y"],
            RED
        )
        
        # 操作說明（左下角）
        self._draw_ship_battle_controls(screen)
    
    def _draw_health_bar(self, screen, name, health, max_health, potions, x, y, color):
        """
        繪製血量條\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        name (str): 角色名稱\n
        health (int): 當前血量\n
        max_health (int): 最大血量\n
        potions (int): 血瓶數量\n
        x (int): x 座標\n
        y (int): y 座標\n
        color (tuple): 血條顏色\n
        """
        bar_width = SHIP_BATTLE_UI["health_bar_width"]
        bar_height = SHIP_BATTLE_UI["health_bar_height"]
        
        # 角色名稱
        name_font = create_font(SHIP_BATTLE_UI["name_font_size"])
        name_text = name_font.render(name, True, WHITE)
        screen.blit(name_text, (x, y - 25))
        
        # 血量條背景（深灰色）
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # 血量條前景
        health_percentage = max(0, health / max_health) if max_health > 0 else 0
        current_width = int(bar_width * health_percentage)
        pygame.draw.rect(screen, color, (x, y, current_width, bar_height))
        
        # 血量條邊框
        pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
        
        # 血量數值
        health_text = self.small_font.render(f"{health}/{max_health}", True, WHITE)
        text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(health_text, text_rect)
        
        # 血瓶數量
        potion_text = self.small_font.render(f"血瓶: {potions}", True, CYAN)
        screen.blit(potion_text, (x, y + bar_height + 5))
    
    def _draw_ship_battle_controls(self, screen):
        """
        繪製 Ship Battle 操作說明\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        controls_x = 20
        controls_y = SCREEN_HEIGHT - 140
        
        controls = [
            "操作說明:",
            "WASD/方向鍵: 移動",
            "Shift: 射擊",
            "Space: 特殊攻擊",
            "I: 使用血瓶",
            "Q: 退出戰鬥"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:  # 標題用黃色
                color = YELLOW
            else:
                color = WHITE
            
            control_text = self.small_font.render(control, True, color)
            screen.blit(control_text, (controls_x, controls_y + i * 20))
    
    def _draw_result_screen(self, screen, battle_info):
        """
        繪製戰鬥結果畫面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        battle_info (dict): 戰鬥資訊字典\n
        """
        battle_state = battle_info.get("battle_state")
        result_timer = battle_info.get("result_timer", 0)
        
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 結果文字
        result_font = create_font(SHIP_BATTLE_UI["result_font_size"])
        
        if battle_state == "victory":
            result_text = result_font.render("Victory", True, GREEN)
            subtitle_text = self.font.render("你擊敗了機器人！", True, WHITE)
        else:  # defeat
            result_text = result_font.render("Defeat", True, RED)
            subtitle_text = self.font.render("你被機器人擊敗了！", True, WHITE)
        
        # 主要結果文字
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(result_text, result_rect)
        
        # 副標題
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(subtitle_text, subtitle_rect)
        
        # 倒數計時
        countdown_seconds = (result_timer // 60) + 1
        countdown_text = self.font.render(f"{countdown_seconds} 秒後返回主選單", True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(countdown_text, countdown_rect)