######################載入套件######################
import pygame
from config import *

######################主畫面系統類別######################
class MenuSystem:
    """
    主畫面系統類別 - 負責處理遊戲主畫面的顯示和互動\n
    \n
    負責處理:\n
    1. 主畫面的繪製和佈局\n
    2. 遊戲標題「Galaxy Blaster」的顯示\n
    3. 開始遊戲按鈕的顯示和點擊檢測\n
    4. 玩家命名功能\n
    5. Ship Battle 模式的啟動\n
    6. 主畫面與遊戲模式的切換\n
    \n
    屬性:\n
    title_font (pygame.font.Font): 標題字體\n
    button_font (pygame.font.Font): 按鈕字體\n
    start_button_rect (pygame.Rect): 開始按鈕的矩形區域\n
    player_name (str): 玩家名稱\n
    is_editing_name (bool): 是否正在編輯名稱\n
    """
    
    def __init__(self):
        """
        初始化主畫面系統\n
        """
        # 初始化字體
        pygame.font.init()
        self.title_font = create_font(MENU_TITLE_SIZE)
        self.button_font = create_font(MENU_BUTTON_SIZE)
        self.small_font = create_font(FONT_SIZES["small"])
        
        # 計算開始按鈕位置（螢幕中央偏下）
        button_x = (SCREEN_WIDTH - MENU_BUTTON_WIDTH) // 2
        button_y = SCREEN_HEIGHT // 2 + 50
        self.start_button_rect = pygame.Rect(button_x, button_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        
        # 玩家名稱相關
        self.player_name = "Player"
        self.is_editing_name = False
        self.name_input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 30)
        
        print("主畫面系統初始化完成")
    
    def handle_text_input(self, event):
        """
        處理文字輸入事件（用於玩家命名）\n
        \n
        參數:\n
        event (pygame.event): pygame 事件物件\n
        """
        if not self.is_editing_name:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                # 按 Enter 或 Esc 結束編輯
                self.is_editing_name = False
                if len(self.player_name.strip()) == 0:
                    self.player_name = "Player"  # 空名稱時使用預設值
                print(f"玩家名稱設定為：{self.player_name}")
            
            elif event.key == pygame.K_BACKSPACE:
                # 刪除字元
                self.player_name = self.player_name[:-1]
                print(f"刪除字元，目前名稱：'{self.player_name}'")
        
        elif event.type == pygame.TEXTINPUT:
            # 處理文字輸入（只有在編輯模式時）
            if len(self.player_name) < 15:  # 最多15個字元
                char = event.text
                if char.isprintable() and char not in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
                    self.player_name += char
                    print(f"新增字元：'{char}'，目前名稱：'{self.player_name}'")
    
    def handle_key_press(self, key):
        """
        處理按鍵事件\n
        \n
        參數:\n
        key (int): 按鍵代碼\n
        \n
        回傳:\n
        str: 遊戲狀態變更 ("start_game", "ship_battle", "hide_seek", None)\n
        """
        if self.is_editing_name:
            return None
        
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            # 開始一般遊戲
            print("開始一般遊戲模式")
            return "start_game"
        
        elif key == pygame.K_m:
            # 開始 Ship Battle 模式
            print(f"玩家 {self.player_name} 開始 Ship Battle 模式")
            return "ship_battle"
        
        elif key == pygame.K_l:
            # 開始躲貓貓遊戲
            print(f"玩家 {self.player_name} 開始躲貓貓遊戲")
            return "hide_seek"
        
        elif key == pygame.K_n:
            # 編輯玩家名稱
            print("開始編輯玩家名稱")
            self.is_editing_name = True
            self.player_name = ""  # 清空名稱重新輸入
        
        return None
    
    def draw_menu(self, screen):
        """
        繪製主畫面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 清空螢幕（深藍色太空背景）
        space_blue = (10, 10, 40)
        screen.fill(space_blue)
        
        # 繪製星空背景
        self._draw_stars_background(screen)
        
        # 繪製遊戲標題
        self._draw_title(screen)
        
        # 繪製玩家名稱區域
        self._draw_player_name_section(screen)
        
        # 繪製遊戲模式選擇
        self._draw_game_mode_buttons(screen)
        
        # 繪製操作說明
        self._draw_instructions(screen)
        
        # 繪製版權資訊
        self._draw_credits(screen)
    
    def _draw_stars_background(self, screen):
        """
        繪製星空背景\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        import random
        
        # 在固定位置繪製星星（避免每幀都隨機產生）
        random.seed(42)  # 使用固定種子確保星星位置一致
        
        for _ in range(100):  # 繪製100顆星星
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT)
            star_size = random.randint(1, 3)
            
            # 不同大小的星星用不同亮度
            if star_size == 1:
                star_color = (100, 100, 100)  # 暗灰色小星星
            elif star_size == 2:
                star_color = (150, 150, 150)  # 中等亮度星星
            else:
                star_color = WHITE  # 明亮大星星
            
            pygame.draw.circle(screen, star_color, (star_x, star_y), star_size)
    
    def _draw_title(self, screen):
        """
        繪製遊戲標題\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 主標題文字
        title_text = self.title_font.render("Galaxy Blaster", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        
        # 標題發光效果（多層繪製）
        glow_colors = [(CYAN, 4), (BLUE, 2), (WHITE, 0)]
        for color, offset in glow_colors:
            glow_text = self.title_font.render("Galaxy Blaster", True, color)
            glow_rect = glow_text.get_rect(center=(title_rect.centerx + offset, title_rect.centery + offset))
            screen.blit(glow_text, glow_rect)
        
        # 副標題
        subtitle_font = create_font(28)
        subtitle_text = subtitle_font.render("Space Shooter Game", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, title_rect.bottom + 20))
        screen.blit(subtitle_text, subtitle_rect)
    
    def _draw_player_name_section(self, screen):
        """
        繪製玩家名稱區域\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 玩家名稱標籤
        name_label = self.button_font.render("玩家名稱:", True, WHITE)
        name_label_rect = name_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(name_label, name_label_rect)
        
        # 名稱輸入框背景
        if self.is_editing_name:
            input_color = (100, 100, 100)  # 編輯中時較亮
            border_color = GREEN
        else:
            input_color = (50, 50, 50)     # 非編輯時較暗
            border_color = WHITE
        
        pygame.draw.rect(screen, input_color, self.name_input_rect)
        pygame.draw.rect(screen, border_color, self.name_input_rect, 2)
        
        # 玩家名稱文字
        display_name = self.player_name
        if self.is_editing_name:
            # 編輯中時顯示游標
            display_name += "|" if (pygame.time.get_ticks() // 500) % 2 else ""
        
        name_text = self.button_font.render(display_name, True, WHITE)
        name_text_rect = name_text.get_rect(center=self.name_input_rect.center)
        screen.blit(name_text, name_text_rect)
        
        # 編輯提示
        if not self.is_editing_name:
            edit_hint = self.small_font.render("按 'N' 鍵修改名稱", True, CYAN)
            edit_hint_rect = edit_hint.get_rect(center=(SCREEN_WIDTH // 2, self.name_input_rect.bottom + 15))
            screen.blit(edit_hint, edit_hint_rect)
    
    def _draw_game_mode_buttons(self, screen):
        """
        繪製遊戲模式按鈕\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        # 一般遊戲模式按鈕
        normal_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, 90, 40)
        pygame.draw.rect(screen, (50, 50, 50), normal_button_rect)
        pygame.draw.rect(screen, GREEN, normal_button_rect, 2)
        
        normal_text = self.small_font.render("一般模式", True, WHITE)
        normal_text_rect = normal_text.get_rect(center=normal_button_rect.center)
        screen.blit(normal_text, normal_text_rect)
        
        # Ship Battle 模式按鈕
        battle_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 + 30, 90, 40)
        pygame.draw.rect(screen, (50, 50, 50), battle_button_rect)
        pygame.draw.rect(screen, RED, battle_button_rect, 2)
        
        battle_text = self.small_font.render("Ship Battle", True, WHITE)
        battle_text_rect = battle_text.get_rect(center=battle_button_rect.center)
        screen.blit(battle_text, battle_text_rect)
        
        # 躲貓貓模式按鈕
        hide_seek_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 2 + 30, 90, 40)
        pygame.draw.rect(screen, (50, 50, 50), hide_seek_button_rect)
        pygame.draw.rect(screen, PURPLE, hide_seek_button_rect, 2)
        
        hide_seek_text = self.small_font.render("躲貓貓", True, WHITE)
        hide_seek_text_rect = hide_seek_text.get_rect(center=hide_seek_button_rect.center)
        screen.blit(hide_seek_text, hide_seek_text_rect)
    
    def _draw_instructions(self, screen):
        """
        繪製操作說明\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        instructions_y = SCREEN_HEIGHT // 2 + 100
        
        instructions = [
            "遊戲模式選擇:",
            "Enter/Space: 開始一般遊戲",
            "M: 開始 Ship Battle 模式",
            "L: 開始躲貓貓遊戲",
            "N: 修改玩家名稱"
        ]
        
        for i, instruction in enumerate(instructions):
            if i == 0:  # 標題用黃色
                color = YELLOW
            else:
                color = WHITE
            
            instruction_text = self.small_font.render(instruction, True, color)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, instructions_y + i * 25))
            screen.blit(instruction_text, instruction_rect)
    
    def _draw_credits(self, screen):
        """
        繪製版權和操作說明\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        credit_font = create_font(FONT_SIZES["mini"])
        
        # 版權資訊
        credits = [
            "使用 Python + Pygame 開發",
            "",
            "一般模式操作:",
            "方向鍵/WASD：移動太空船",
            "Ctrl/Shift：發射子彈",
            "空白鍵：切換武器",
            "C鍵：切換太空船",
            "X鍵：特殊攻擊",
            "",
            "Ship Battle 模式操作:",
            "WASD/方向鍵：移動",
            "Shift：射擊",
            "Space：特殊攻擊",
            "I：使用血瓶",
            "Q：退出戰鬥"
        ]
        
        start_y = SCREEN_HEIGHT - len(credits) * 18 - 10
        
        for i, credit in enumerate(credits):
            if credit in ["一般模式操作:", "Ship Battle 模式操作:"]:
                color = CYAN
            elif credit == "":
                continue
            else:
                color = (180, 180, 180)  # 淺灰色
            
            credit_text = credit_font.render(credit, True, color)
            credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 18))
            screen.blit(credit_text, credit_rect)
    
    def handle_click(self, mouse_pos):
        """
        處理滑鼠點擊事件\n
        \n
        參數:\n
        mouse_pos (tuple): 滑鼠點擊位置 (x, y)\n
        \n
        回傳:\n
        str: 遊戲狀態變更 ("start_game", "ship_battle", "hide_seek", "edit_name", None)\n
        """
        # 檢查是否點擊名稱輸入框
        if self.name_input_rect.collidepoint(mouse_pos):
            print("開始編輯玩家名稱")
            self.is_editing_name = True
            self.player_name = ""  # 清空名稱重新輸入
            return "edit_name"
        
        # 檢查遊戲模式按鈕
        normal_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, 90, 40)
        if normal_button_rect.collidepoint(mouse_pos):
            print("點擊開始一般遊戲")
            return "start_game"
        
        battle_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 + 30, 90, 40)
        if battle_button_rect.collidepoint(mouse_pos):
            print(f"玩家 {self.player_name} 點擊開始 Ship Battle 模式")
            return "ship_battle"
        
        hide_seek_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 2 + 30, 90, 40)
        if hide_seek_button_rect.collidepoint(mouse_pos):
            print(f"玩家 {self.player_name} 點擊開始躲貓貓遊戲")
            return "hide_seek"
        
        return None
    
    def get_player_name(self):
        """
        取得玩家名稱\n
        \n
        回傳:\n
        str: 玩家名稱\n
        """
        return self.player_name.strip() if self.player_name.strip() else "Player"
    
    def is_hovering_button(self, mouse_pos):
        """
        檢查滑鼠是否懸停在按鈕上\n
        \n
        參數:\n
        mouse_pos (tuple): 滑鼠位置 (x, y)\n
        \n
        回傳:\n
        bool: 如果滑鼠懸停在任何按鈕上返回 True\n
        """
        normal_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, 90, 40)
        battle_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 + 30, 90, 40)
        hide_seek_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 2 + 30, 90, 40)
        
        return (normal_button_rect.collidepoint(mouse_pos) or 
                battle_button_rect.collidepoint(mouse_pos) or
                hide_seek_button_rect.collidepoint(mouse_pos) or
                self.name_input_rect.collidepoint(mouse_pos))