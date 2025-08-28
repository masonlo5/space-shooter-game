######################載入套件######################
import pygame
import random
import math
import time
from config import *
from entities import HideSeekPlayer, Ghost, HideSeekMap

######################躲貓貓遊戲系統類別######################
class HideSeekSystem:
    """
    躲貓貓遊戲系統類別 - 負責管理整個躲貓貓遊戲的邏輯和狀態\n
    \n
    負責處理:\n
    1. 遊戲初始化和玩家創建\n
    2. 角色身分分配（搜尋者/躲藏者）\n
    3. 遊戲階段管理（等待→傳送→角色顯示→遊戲進行）\n
    4. 時間控制和倒數計時\n
    5. 玩家互動和攻擊處理\n
    6. 勝負判定和遊戲結束\n
    7. 幽靈模式管理\n
    8. UI介面協調\n
    """
    
    def __init__(self, human_player_name="Player"):
        """
        初始化躲貓貓遊戲系統\n
        \n
        參數:\n
        human_player_name (str): 真人玩家名稱\n
        """
        self.human_player_name = human_player_name
        
        # 遊戲狀態
        self.game_state = GAME_STATE_HIDE_SEEK_LOBBY
        self.game_timer = 0
        self.phase_timer = 0
        
        # 玩家和物件
        self.players = []
        self.ghosts = []
        self.human_player = None
        self.human_ghost = None
        
        # 地圖
        self.game_map = None
        
        # 角色分配
        self.seekers = []
        self.hiders = []
        
        # 勝負狀態
        self.game_over = False
        self.victory_message = ""
        self.game_over_timer = 0
        
        # 小地圖系統
        self.minimap_system = None
        
        # 初始化遊戲
        self._initialize_game()
        
        print("躲貓貓遊戲系統初始化完成")
    
    def _initialize_game(self):
        """
        初始化遊戲（創建玩家、地圖、分配角色）\n
        """
        # 設定隨機種子，確保每次遊戲都有不同的隨機結果
        random.seed(time.time())
        
        # 創建地圖
        self.game_map = HideSeekMap()
        
        # 創建玩家
        self._create_players()
        
        # 分配角色
        self._assign_roles()
        
        # 設置初始位置
        self._set_initial_positions()
        
        # 初始化小地圖
        self.minimap_system = HideSeekMiniMap(self.game_map)
        
        # 設置初始遊戲狀態
        self.game_state = GAME_STATE_HIDE_SEEK_LOBBY
        self.phase_timer = HIDE_SEEK_SETTINGS["lobby_duration"]
        
        print("躲貓貓遊戲初始化完成")
    
    def _create_players(self):
        """
        創建所有玩家（1個真人 + 4個AI）\n
        """
        total_players = HIDE_SEEK_SETTINGS["total_players"]
        
        # 重新設置隨機種子以確保道具分配的隨機性
        player_seed = int(time.time() * 1000) % 100000
        random.seed(player_seed)
        print(f"道具分配種子：{player_seed}")
        
        # 準備道具分配 - 確保多樣性
        potion_types = list(HIDE_SEEK_POTIONS.keys())
        assigned_potions = self._distribute_potions(potion_types, total_players)
        
        # 創建真人玩家
        human_player = HideSeekPlayer(0, is_human=True, name=self.human_player_name, assigned_potion=assigned_potions[0])
        self.players.append(human_player)
        self.human_player = human_player
        
        # 創建AI玩家
        ai_names = ["機器人Alpha", "機器人Beta", "機器人Gamma", "機器人Delta"]
        for i in range(1, total_players):
            ai_name = ai_names[i-1] if i-1 < len(ai_names) else f"機器人{i}"
            ai_player = HideSeekPlayer(i, is_human=False, name=ai_name, assigned_potion=assigned_potions[i])
            self.players.append(ai_player)
        
        print(f"創建了 {len(self.players)} 名玩家")
    
    def _distribute_potions(self, potion_types, total_players):
        """
        智能分配道具，確保多樣性\n
        
        參數:\n
        potion_types (list): 可用道具類型列表\n
        total_players (int): 玩家總數\n
        
        回傳:\n
        list: 分配給每個玩家的道具類型\n
        """
        assigned_potions = []
        
        # 確保每種道具至少分配一次（如果道具種類 >= 玩家數量）
        if len(potion_types) >= total_players:
            # 隨機選擇不重複的道具
            assigned_potions = random.sample(potion_types, total_players)
        else:
            # 道具種類少於玩家數量，確保盡可能多樣化
            assigned_potions = potion_types.copy()
            while len(assigned_potions) < total_players:
                assigned_potions.append(random.choice(potion_types))
            # 再次隨機打亂，增加隨機性
            random.shuffle(assigned_potions)
        
        # 輸出分配結果以供除錯
        print(f"道具分配結果：{assigned_potions}")
        
        return assigned_potions
    
    def _assign_roles(self):
        """
        隨機分配角色身分\n
        """
        # 重新設置隨機種子以確保角色分配的隨機性
        role_seed = int(time.time() * 1000) % 100000 + 1000  # 避免和道具種子相同
        random.seed(role_seed)
        print(f"角色分配種子：{role_seed}")
        
        # 隨機選擇搜尋者
        seekers_count = HIDE_SEEK_SETTINGS["seekers_count"]
        all_players = self.players.copy()
        
        # 確保隨機性
        random.shuffle(all_players)
        
        # 隨機選擇搜尋者
        self.seekers = random.sample(all_players, seekers_count)
        self.hiders = [player for player in all_players if player not in self.seekers]
        
        # 設置玩家角色
        for player in self.seekers:
            player.assign_role("seeker")
        
        for player in self.hiders:
            player.assign_role("hider")
        
        print(f"角色分配完成：{len(self.seekers)} 名搜尋者，{len(self.hiders)} 名躲藏者")
    
    def _set_initial_positions(self):
        """
        設置玩家初始位置（所有玩家在中央）\n
        """
        spawn_positions = self.game_map.get_spawn_positions(len(self.players))
        
        for i, player in enumerate(self.players):
            if i < len(spawn_positions):
                x, y = spawn_positions[i]
                player.teleport_to_position(x, y)
        
        print("玩家初始位置設置完成")
    
    def update(self, keys):
        """
        更新躲貓貓遊戲狀態\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        \n
        回傳:\n
        str: 遊戲狀態變更或None\n
        """
        # 處理遊戲階段更新
        result = self._update_game_phase(keys)
        if result:
            return result
        
        # 更新玩家
        if self.game_state == GAME_STATE_HIDE_SEEK_PLAYING:
            self._update_players(keys)
            self._check_victory_conditions()
        
        # 更新幽靈
        if self.ghosts:
            ghost_result = self._update_ghosts(keys)
            if ghost_result:
                return ghost_result
        
        # 處理道具使用
        if self.game_state == GAME_STATE_HIDE_SEEK_PLAYING:
            self._handle_potion_usage(keys)
        
        # 更新小地圖
        if self.minimap_system:
            self.minimap_system.update(self.players, self.ghosts)
        
        return None
    
    def _update_game_phase(self, keys):
        """
        更新遊戲階段（等待→傳送→角色顯示→開始）\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        \n
        回傳:\n
        str: 遊戲狀態變更或None\n
        """
        # 檢查退出遊戲
        if keys[pygame.K_q]:
            print("玩家選擇退出躲貓貓遊戲")
            return "return_to_menu"
        
        # 更新階段計時器
        if self.phase_timer > 0:
            self.phase_timer -= 1
        
        # 階段轉換邏輯
        if self.game_state == GAME_STATE_HIDE_SEEK_LOBBY:
            if self.phase_timer == 0:
                self._start_teleport_phase()
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_TELEPORT:
            if self.phase_timer == 0:
                self._start_role_reveal_phase()
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_ROLE_REVEAL:
            if self.phase_timer == 0:
                self._start_playing_phase()
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_PLAYING:
            # 更新遊戲計時器
            self.game_timer += 1
            
            # 檢查遊戲時間限制（可選功能）
            if self.game_timer >= HIDE_SEEK_SETTINGS["game_duration"]:
                self._end_game("時間到！躲藏者獲勝！")
        
        return None
    
    def _start_teleport_phase(self):
        """
        開始傳送階段\n
        """
        print("開始傳送階段")
        self.game_state = GAME_STATE_HIDE_SEEK_TELEPORT
        self.phase_timer = 60  # 1秒傳送時間
        
        # 傳送玩家到隨機位置
        teleport_positions = self.game_map.get_teleport_positions(len(self.players))
        
        for i, player in enumerate(self.players):
            if i < len(teleport_positions):
                x, y = teleport_positions[i]
                player.teleport_to_position(x, y)
    
    def _start_role_reveal_phase(self):
        """
        開始角色身分顯示階段\n
        """
        print("開始角色身分顯示階段")
        self.game_state = GAME_STATE_HIDE_SEEK_ROLE_REVEAL
        self.phase_timer = HIDE_SEEK_SETTINGS["role_reveal_duration"]
    
    def _start_playing_phase(self):
        """
        開始遊戲進行階段\n
        """
        print("躲貓貓遊戲正式開始！")
        self.game_state = GAME_STATE_HIDE_SEEK_PLAYING
        self.game_timer = 0
    
    def _update_players(self, keys):
        """
        更新所有玩家狀態\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        """
        alive_players = [p for p in self.players if p.alive]
        
        for player in alive_players:
            # 更新玩家狀態
            attack_result = player.update(keys if player.is_human else {}, 
                                        alive_players, self.game_map.get_obstacles())
            
            # 處理攻擊結果
            if attack_result and attack_result["attacked"] and attack_result["target"]:
                target = attack_result["target"]
                if not target.alive:
                    # 玩家死亡，創建幽靈
                    ghost = Ghost(target)
                    self.ghosts.append(ghost)
                    
                    if target.is_human:
                        self.human_ghost = ghost
                    
                    print(f"玩家 {target.name} 死亡，變成幽靈")
    
    def _update_ghosts(self, keys):
        """
        更新幽靈狀態\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        \n
        回傳:\n
        str: 如果幽靈選擇返回主畫面則返回相應字串\n
        """
        for ghost in self.ghosts[:]:  # 使用切片避免修改時出錯
            if ghost.is_human:
                result = ghost.update(keys)
                if result == "return_to_menu":
                    return "return_to_menu"
            else:
                ghost.update({})
        
        return None
    
    def _handle_potion_usage(self, keys):
        """
        處理道具使用\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        """
        # 真人玩家使用道具（按E鍵）
        if self.human_player and self.human_player.alive and keys[pygame.K_e]:
            if self.human_player.use_potion():
                print(f"玩家 {self.human_player.name} 使用了道具")
    
    def _check_victory_conditions(self):
        """
        檢查勝負條件\n
        """
        if self.game_over:
            return
        
        alive_seekers = [p for p in self.seekers if p.alive]
        alive_hiders = [p for p in self.hiders if p.alive]
        
        # 勝負判定
        if len(alive_hiders) == 0:
            self._end_game("搜尋者獲勝！所有躲藏者都被找到了！")
        elif len(alive_seekers) == 0:
            self._end_game("躲藏者獲勝！所有搜尋者都被冰凍了！")
    
    def _end_game(self, message):
        """
        結束遊戲\n
        \n
        參數:\n
        message (str): 勝負訊息\n
        """
        self.game_over = True
        self.victory_message = message
        self.game_over_timer = 300  # 5秒顯示時間
        print(f"遊戲結束：{message}")
    
    def draw(self, screen):
        """
        繪製躲貓貓遊戲畫面\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        """
        # 確定相機位置（跟隨真人玩家或幽靈）
        camera_x, camera_y = self._get_camera_position()
        
        # 繪製地圖背景
        self.game_map.draw_background(screen, camera_x, camera_y)
        
        # 繪製地圖障礙物
        self.game_map.draw_obstacles(screen, camera_x, camera_y)
        
        # 繪製玩家
        for player in self.players:
            if player.alive:
                player.draw(screen, camera_x, camera_y)
        
        # 繪製幽靈
        for ghost in self.ghosts:
            ghost.draw(screen, camera_x, camera_y)
        
        # 繪製小地圖
        if self.minimap_system:
            self.minimap_system.draw(screen, self.human_player, self.human_ghost)
        
        # 繪製UI
        self._draw_ui(screen)
    
    def _get_camera_position(self):
        """
        取得相機位置\n
        \n
        回傳:\n
        tuple: (camera_x, camera_y) 相機座標\n
        """
        # 如果真人玩家還活著，跟隨玩家
        if self.human_player and self.human_player.alive:
            return (self.human_player.camera_x, self.human_player.camera_y)
        
        # 如果真人玩家死亡但有幽靈，跟隨幽靈
        elif self.human_ghost:
            return (self.human_ghost.camera_x, self.human_ghost.camera_y)
        
        # 預設相機位置
        return (0, 0)
    
    def _draw_ui(self, screen):
        """
        繪製遊戲UI\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        """
        font_size = HIDE_SEEK_UI["timer_font_size"]
        chinese_font = get_chinese_font()
        font = create_font(font_size)
        
        # 根據遊戲狀態顯示不同UI
        if self.game_state == GAME_STATE_HIDE_SEEK_LOBBY:
            self._draw_lobby_ui(screen, font)
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_TELEPORT:
            self._draw_teleport_ui(screen, font)
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_ROLE_REVEAL:
            self._draw_role_reveal_ui(screen, font)
        
        elif self.game_state == GAME_STATE_HIDE_SEEK_PLAYING:
            self._draw_playing_ui(screen, font)
        
        # 繪製遊戲結束UI
        if self.game_over:
            self._draw_game_over_ui(screen)
        
        # 繪製操作說明
        self._draw_controls_info(screen)
    
    def _draw_lobby_ui(self, screen, font):
        """
        繪製等待階段UI\n
        """
        seconds_left = max(0, self.phase_timer // 60)
        countdown_text = font.render(f"遊戲開始倒數：{seconds_left}", True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(countdown_text, countdown_rect)
        
        # 玩家列表
        y_offset = 100
        for i, player in enumerate(self.players):
            player_info = f"{player.name} ({player.spaceship_style}) - {player.potion_type}"
            chinese_font = get_chinese_font()
            info_text = create_font(FONT_SIZES["normal"])
            info_surface = info_text.render(player_info, True, WHITE)
            screen.blit(info_surface, (50, y_offset + i * 25))
    
    def _draw_teleport_ui(self, screen, font):
        """
        繪製傳送階段UI\n
        """
        teleport_text = font.render("正在傳送玩家...", True, YELLOW)
        teleport_rect = teleport_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(teleport_text, teleport_rect)
    
    def _draw_role_reveal_ui(self, screen, font):
        """
        繪製角色身分顯示UI\n
        """
        # 顯示玩家角色
        if self.human_player:
            role_text = "你是搜尋者！" if self.human_player.role == "seeker" else "你是躲藏者！"
            role_color = RED if self.human_player.role == "seeker" else GREEN
            
            chinese_font = get_chinese_font()
            role_font = create_font(HIDE_SEEK_UI["role_font_size"])
            role_surface = role_font.render(role_text, True, role_color)
            role_rect = role_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(role_surface, role_rect)
        
        # 倒數
        seconds_left = max(0, self.phase_timer // 60)
        countdown_text = font.render(f"遊戲開始：{seconds_left}", True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(countdown_text, countdown_rect)
    
    def _draw_playing_ui(self, screen, font):
        """
        繪製遊戲進行中UI\n
        """
        # 玩家角色資訊
        if self.human_player and self.human_player.alive:
            role_text = "搜尋者" if self.human_player.role == "seeker" else "躲藏者"
            role_color = RED if self.human_player.role == "seeker" else GREEN
            
            role_surface = font.render(f"身分：{role_text}", True, role_color)
            screen.blit(role_surface, (10, 10))
            
            # 道具資訊
            potion_name = HIDE_SEEK_POTIONS[self.human_player.potion_type]["name"]
            potion_text = f"道具：{potion_name} ({self.human_player.potion_uses}次)"
            potion_surface = create_font(FONT_SIZES["normal"]).render(potion_text, True, WHITE)
            screen.blit(potion_surface, (10, 40))
            
            # 攻擊冷卻
            if self.human_player.special_attack_cooldown > 0:
                cooldown_seconds = self.human_player.special_attack_cooldown // 60 + 1
                cooldown_text = f"攻擊冷卻：{cooldown_seconds}秒"
                cooldown_surface = create_font(FONT_SIZES["normal"]).render(cooldown_text, True, YELLOW)
                screen.blit(cooldown_surface, (10, 70))
        
        # 存活玩家統計
        alive_seekers = len([p for p in self.seekers if p.alive])
        alive_hiders = len([p for p in self.hiders if p.alive])
        
        stats_text = f"搜尋者：{alive_seekers}  躲藏者：{alive_hiders}"
        stats_surface = create_font(28).render(stats_text, True, WHITE)
        stats_rect = stats_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(stats_surface, stats_rect)
        
        # 幽靈模式提示
        if self.human_ghost:
            ghost_font = create_font(HIDE_SEEK_UI["ghost_message_font_size"])
            ghost_text = ghost_font.render("你已死亡 - 幽靈模式", True, (150, 150, 150))
            ghost_rect = ghost_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(ghost_text, ghost_rect)
            
            choice_text = create_font(FONT_SIZES["normal"]).render("按 E 繼續觀戰，按 T 返回主畫面", True, WHITE)
            choice_rect = choice_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            screen.blit(choice_text, choice_rect)
    
    def _draw_game_over_ui(self, screen):
        """
        繪製遊戲結束UI\n
        """
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 勝負訊息
        result_font = create_font(HIDE_SEEK_UI["countdown_font_size"])
        result_text = result_font.render(self.victory_message, True, YELLOW)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(result_text, result_rect)
        
        # 返回提示
        if self.game_over_timer <= 0:
            return_text = create_font(FONT_SIZES["medium"]).render("按任意鍵返回主畫面", True, WHITE)
            return_rect = return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(return_text, return_rect)
        else:
            self.game_over_timer -= 1
    
    def _draw_controls_info(self, screen):
        """
        繪製操作說明\n
        """
        controls_font = create_font(FONT_SIZES["small"])
        controls = ["WASD/方向鍵: 移動", "空格: 特殊攻擊", "E: 使用道具", "Q: 退出遊戲"]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (180, 180, 180))
            screen.blit(control_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100 + i * 20))
    
    def handle_key_press(self, key):
        """
        處理按鍵事件\n
        \n
        參數:\n
        key (int): 按鍵代碼\n
        \n
        回傳:\n
        str: 遊戲狀態變更或None\n
        """
        # 遊戲結束後按任意鍵返回主畫面
        if self.game_over and self.game_over_timer <= 0:
            return "return_to_menu"
        
        # 幽靈模式選擇
        if self.human_ghost and not self.human_player.alive:
            if key == pygame.K_e:
                # 繼續幽靈模式（什麼都不做）
                pass
            elif key == pygame.K_t:
                return "return_to_menu"
        
        return None


######################躲貓貓小地圖系統類別######################
class HideSeekMiniMap:
    """
    躲貓貓小地圖系統類別 - 負責顯示小地圖和玩家位置\n
    """
    
    def __init__(self, game_map):
        """
        初始化小地圖系統\n
        \n
        參數:\n
        game_map (HideSeekMap): 遊戲地圖物件\n
        """
        self.game_map = game_map
        self.map_data = game_map.draw_minimap_data()
        
        # 小地圖設定
        self.config = HIDE_SEEK_MINIMAP
        
        # 創建小地圖表面
        self.minimap_surface = pygame.Surface((self.config["width"], self.config["height"]), pygame.SRCALPHA)
        
        # 預繪製地圖背景
        self._render_map_background()
    
    def _render_map_background(self):
        """
        預繪製小地圖背景和障礙物\n
        """
        self.minimap_surface.fill(self.config["background_color"])
        
        # 繪製障礙物
        scale = self.config["scale_factor"]
        
        for obstacle in self.map_data["obstacles"]:
            minimap_x = int(obstacle.x * scale)
            minimap_y = int(obstacle.y * scale)
            minimap_width = max(2, int(obstacle.width * scale))
            minimap_height = max(2, int(obstacle.height * scale))
            
            minimap_rect = pygame.Rect(minimap_x, minimap_y, minimap_width, minimap_height)
            pygame.draw.rect(self.minimap_surface, (100, 100, 100), minimap_rect)
        
        # 繪製邊框
        pygame.draw.rect(self.minimap_surface, self.config["border_color"], 
                        (0, 0, self.config["width"], self.config["height"]), 2)
    
    def update(self, players, ghosts):
        """
        更新小地圖（重新繪製玩家位置）\n
        \n
        參數:\n
        players (list): 玩家列表\n
        ghosts (list): 幽靈列表\n
        """
        # 重置到背景狀態
        temp_surface = self.minimap_surface.copy()
        
        # 繪製活著的玩家
        for player in players:
            if player.alive:
                self._draw_player_dot(temp_surface, player)
        
        # 繪製幽靈（只有幽靈能看到所有位置）
        for ghost in ghosts:
            if ghost.is_human:
                # 如果是真人幽靈，顯示所有玩家位置
                for player in players:
                    if player.alive:
                        self._draw_player_dot(temp_surface, player, is_ghost_view=True)
        
        self.minimap_surface = temp_surface
    
    def _draw_player_dot(self, surface, player, is_ghost_view=False):
        """
        在小地圖上繪製玩家點\n
        \n
        參數:\n
        surface (pygame.Surface): 繪製表面\n
        player (HideSeekPlayer): 玩家物件\n
        is_ghost_view (bool): 是否為幽靈視角\n
        """
        scale = self.config["scale_factor"]
        dot_size = self.config["player_dot_size"]
        
        # 計算小地圖位置
        minimap_x = int(player.x * scale)
        minimap_y = int(player.y * scale)
        
        # 確保點在小地圖範圍內
        if 0 <= minimap_x < self.config["width"] and 0 <= minimap_y < self.config["height"]:
            # 選擇顏色
            if player.is_human:
                color = self.config["self_color"]  # 自己用黃色
            elif player.role == "seeker":
                color = self.config["seeker_color"]  # 搜尋者用紅色
            else:
                color = self.config["hider_color"]   # 躲藏者用綠色
            
            # 如果玩家隱形且不是幽靈視角，不顯示
            if player.invisible and not is_ghost_view:
                return
            
            # 繪製玩家點
            pygame.draw.circle(surface, color, (minimap_x, minimap_y), dot_size)
            
            # 繪製邊框
            pygame.draw.circle(surface, WHITE, (minimap_x, minimap_y), dot_size + 1, 1)
    
    def draw(self, screen, human_player, human_ghost):
        """
        繪製小地圖到螢幕上\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        human_player (HideSeekPlayer): 真人玩家\n
        human_ghost (Ghost): 真人幽靈\n
        """
        # 繪製小地圖
        map_x = self.config["x"]
        map_y = self.config["y"]
        
        screen.blit(self.minimap_surface, (map_x, map_y))
        
        # 繪製小地圖標題
        font = create_font(FONT_SIZES["small"])
        title_text = font.render("地圖", True, WHITE)
        screen.blit(title_text, (map_x, map_y - 25))
        
        # 如果是幽靈模式，顯示特殊提示
        if human_ghost:
            ghost_text = font.render("(幽靈視角)", True, (150, 150, 150))
            screen.blit(ghost_text, (map_x + 50, map_y - 25))