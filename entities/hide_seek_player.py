######################載入套件######################
import pygame
import math
import random
import time
from config import *

######################躲貓貓玩家類別######################
class HideSeekPlayer:
    """
    躲貓貓遊戲玩家類別 - 處理玩家和AI的移動、攻擊、道具使用\n
    \n
    負責處理:\n
    1. 玩家移動和碰撞檢測\n
    2. 太空船外觀渲染（5種不同樣式）\n
    3. 角色身分管理（搜尋者/躲藏者）\n
    4. 道具系統（5種藥水，每種3次）\n
    5. 特殊攻擊系統（空格鍵觸發）\n
    6. AI行為邏輯（機器人玩家）\n
    7. 狀態效果管理（冰凍、隱形、護盾等）\n
    """
    
    def __init__(self, player_id, is_human=False, name="Player", assigned_potion=None):
        """
        初始化躲貓貓玩家\n
        \n
        參數:\n
        player_id (int): 玩家編號（0-4）\n
        is_human (bool): 是否為真人玩家\n
        name (str): 玩家名稱\n
        assigned_potion (str): 預分配的道具類型（如果為None則隨機分配）\n
        """
        self.player_id = player_id
        self.is_human = is_human
        self.name = name
        
        # 基本屬性
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.alive = True
        
        # 角色身分（在遊戲開始時分配）
        self.role = "hider"  # "seeker" 或 "hider"
        
        # 隨機分配太空船樣式 - 每個玩家使用不同的隨機種子
        style_keys = list(HIDE_SEEK_SPACESHIP_STYLES.keys())
        # 為每個玩家建立獨特的隨機種子（玩家ID + 當前時間）
        unique_seed = player_id * 12345 + int(time.time() * 1000) % 100000
        random.seed(unique_seed)
        self.spaceship_style = random.choice(style_keys)
        style_config = HIDE_SEEK_SPACESHIP_STYLES[self.spaceship_style]
        
        print(f"玩家 {player_id} 樣式種子：{unique_seed}，選中樣式：{self.spaceship_style}")
        
        # 根據樣式調整尺寸
        size_mod = style_config["size_modifier"]
        self.width = int(self.width * size_mod)
        self.height = int(self.height * size_mod)
        
        # 顏色設定
        self.primary_color = style_config["primary_color"]
        self.secondary_color = style_config["secondary_color"]
        self.shape = style_config["shape"]
        
        # 道具系統 - 使用預分配的道具或隨機分配
        if assigned_potion:
            self.potion_type = assigned_potion
        else:
            # 如果沒有指定道具，隨機分配
            potion_types = list(HIDE_SEEK_POTIONS.keys())
            # 使用獨特種子確保真正隨機
            potion_seed = player_id * 54321 + int(time.time() * 1000) % 100000
            random.seed(potion_seed)
            self.potion_type = random.choice(potion_types)
            print(f"玩家 {player_id} 道具種子：{potion_seed}，選中道具：{self.potion_type}")
        
        self.potion_uses = HIDE_SEEK_POTIONS[self.potion_type]["uses"]
        
        # 狀態效果
        self.frozen = False
        self.freeze_timer = 0
        self.invisible = False
        self.invisible_timer = 0
        self.shielded = False
        self.shield_timer = 0
        self.speed_boosted = False
        self.speed_boost_timer = 0
        self.freeze_immune = False
        self.freeze_immune_timer = 0
        self.invulnerable = False
        self.invulnerable_timer = 0
        
        # 攻擊系統
        self.special_attack_cooldown = 0
        self.can_attack = True
        
        # AI相關屬性
        if not self.is_human:
            self.ai_direction_x = random.choice([-1, 0, 1])
            self.ai_direction_y = random.choice([-1, 0, 1])
            self.ai_change_timer = 0
            self.ai_target_player = None
            self.ai_last_potion_use = 0
        
        # 相機偏移（只有真人玩家需要）
        self.camera_x = 0
        self.camera_y = 0
        
        print(f"玩家 {self.name} 創建完成，樣式：{self.spaceship_style}，道具：{self.potion_type}")
    
    def assign_role(self, role):
        """
        分配角色身分\n
        \n
        參數:\n
        role (str): "seeker" 或 "hider"\n
        """
        self.role = role
        print(f"玩家 {self.name} 被分配為：{role}")
    
    def teleport_to_position(self, x, y):
        """
        傳送到指定位置\n
        \n
        參數:\n
        x (int): 目標X座標\n
        y (int): 目標Y座標\n
        """
        self.x = x
        self.y = y
        print(f"玩家 {self.name} 傳送到位置：({x}, {y})")
    
    def update(self, keys, other_players, map_obstacles, sounds=None):
        """
        更新玩家狀態\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        other_players (list): 其他玩家列表\n
        map_obstacles (list): 地圖障礙物列表\n
        sounds (dict): 音效物件字典\n
        """
        if not self.alive:
            return
        
        # 更新狀態效果計時器
        self._update_status_effects()
        
        # 更新攻擊冷卻時間
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        # 更新無敵時間
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer == 0:
                self.invulnerable = False
        
        # 如果被冰凍，無法移動
        if self.frozen:
            return
        
        # 處理移動
        if self.is_human:
            self._handle_human_movement(keys, map_obstacles)
        else:
            self._handle_ai_movement(other_players, map_obstacles)
        
        # 處理攻擊
        if self.is_human:
            return self._handle_human_attack(keys, other_players, sounds)
        else:
            return self._handle_ai_attack(other_players, sounds)
    
    def _update_status_effects(self):
        """
        更新所有狀態效果的計時器\n
        """
        # 冰凍效果
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
            if self.freeze_timer == 0:
                self.frozen = False
                print(f"玩家 {self.name} 冰凍效果結束")
        
        # 隱形效果
        if self.invisible_timer > 0:
            self.invisible_timer -= 1
            if self.invisible_timer == 0:
                self.invisible = False
                print(f"玩家 {self.name} 隱形效果結束")
        
        # 護盾效果
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shielded = False
                print(f"玩家 {self.name} 護盾效果結束")
        
        # 加速效果
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed_boosted = False
                print(f"玩家 {self.name} 加速效果結束")
        
        # 防凍效果
        if self.freeze_immune_timer > 0:
            self.freeze_immune_timer -= 1
            if self.freeze_immune_timer == 0:
                self.freeze_immune = False
                print(f"玩家 {self.name} 防凍效果結束")
    
    def _handle_human_movement(self, keys, map_obstacles):
        """
        處理真人玩家移動\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        map_obstacles (list): 地圖障礙物列表\n
        """
        move_speed = self.speed
        if self.speed_boosted:
            move_speed = int(move_speed * HIDE_SEEK_POTIONS["speed_boost"]["effect_multiplier"])
        
        # 計算移動向量
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = move_speed
        
        # 應用移動並檢查碰撞
        self._apply_movement(dx, dy, map_obstacles)
    
    def _handle_ai_movement(self, other_players, map_obstacles):
        """
        處理AI玩家移動\n
        \n
        參數:\n
        other_players (list): 其他玩家列表\n
        map_obstacles (list): 地圖障礙物列表\n
        """
        move_speed = self.speed
        if self.speed_boosted:
            move_speed = int(move_speed * HIDE_SEEK_POTIONS["speed_boost"]["effect_multiplier"])
        
        # 更新AI移動方向（搜尋者更頻繁更新）
        update_interval = HIDE_SEEK_AI["seek_update_interval"] if self.role == "seeker" else HIDE_SEEK_AI["movement_change_interval"]
        self.ai_change_timer += 1
        if self.ai_change_timer >= update_interval:
            self.ai_change_timer = 0
            self._update_ai_direction(other_players)
        
        # 應用AI移動
        dx = self.ai_direction_x * move_speed
        dy = self.ai_direction_y * move_speed
        
        self._apply_movement(dx, dy, map_obstacles)
        
        # AI道具使用邏輯
        self._handle_ai_potion_use()
    
    def _update_ai_direction(self, other_players):
        """
        更新AI移動方向（根據角色身分決定行為）\n
        \n
        參數:\n
        other_players (list): 其他玩家列表\n
        """
        if self.role == "seeker":
            # 搜尋者AI：積極追蹤躲藏者
            closest_hider = None
            closest_distance = float('inf')
            
            # 搜索所有存活的躲藏者
            for player in other_players:
                if player.alive and player.role == "hider" and not player.invisible:
                    distance = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_hider = player
            
            if closest_hider:
                # 總是朝最近的躲藏者移動（無距離限制）
                dx = closest_hider.x - self.x
                dy = closest_hider.y - self.y
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # 使用標準化的方向向量，確保精確移動
                    self.ai_direction_x = dx / length
                    self.ai_direction_y = dy / length
                self.ai_target_player = closest_hider
                # 打印追擊資訊
                print(f"搜尋者 {self.name} 正在追擊躲藏者 {closest_hider.name}，距離：{closest_distance:.1f}")
            else:
                # 如果找不到可見的躲藏者，進行主動巡邏
                self._active_patrol_movement()
        
        else:  # 躲藏者AI
            # 躲藏者AI：遠離搜尋者
            closest_seeker = None
            closest_distance = float('inf')
            
            for player in other_players:
                if player.alive and player.role == "seeker":
                    distance = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_seeker = player
            
            if closest_seeker and closest_distance < HIDE_SEEK_AI["hide_flee_distance"]:
                # 遠離搜尋者
                dx = self.x - closest_seeker.x
                dy = self.y - closest_seeker.y
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    self.ai_direction_x = dx / length
                    self.ai_direction_y = dy / length
            else:
                # 隨機移動
                self._random_ai_movement()
    
    def _random_ai_movement(self):
        """
        AI隨機移動\n
        """
        if random.randint(1, 100) <= HIDE_SEEK_AI["random_movement_chance"]:
            # 使用標準化的隨機方向向量
            angle = random.uniform(0, 2 * math.pi)
            self.ai_direction_x = math.cos(angle)
            self.ai_direction_y = math.sin(angle)
    
    def _active_patrol_movement(self):
        """
        搜尋者主動巡邏移動（當沒有發現躲藏者時）\n
        """
        # 朝地圖中心或邊緣區域移動，主動搜索
        map_center_x = HIDE_SEEK_MAP["map_width"] // 2
        map_center_y = HIDE_SEEK_MAP["map_height"] // 2
        
        # 如果在地圖中心附近，移向邊緣
        distance_to_center = math.sqrt((self.x - map_center_x)**2 + (self.y - map_center_y)**2)
        
        if distance_to_center < 200:
            # 移向隨機邊緣
            angle = random.uniform(0, 2 * math.pi)
            self.ai_direction_x = math.cos(angle)
            self.ai_direction_y = math.sin(angle)
        else:
            # 移向地圖中心
            dx = map_center_x - self.x
            dy = map_center_y - self.y
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                self.ai_direction_x = dx / length
                self.ai_direction_y = dy / length
    
    def _apply_movement(self, dx, dy, map_obstacles):
        """
        應用移動並處理碰撞檢測\n
        \n
        參數:\n
        dx (int): X軸移動量\n
        dy (int): Y軸移動量\n
        map_obstacles (list): 地圖障礙物列表\n
        """
        # 儲存原始位置
        old_x = self.x
        old_y = self.y
        
        # 嘗試移動
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 檢查地圖邊界
        new_x = max(self.width//2, min(HIDE_SEEK_MAP["map_width"] - self.width//2, new_x))
        new_y = max(self.height//2, min(HIDE_SEEK_MAP["map_height"] - self.height//2, new_y))
        
        # 檢查障礙物碰撞
        player_rect = pygame.Rect(new_x - self.width//2, new_y - self.height//2, self.width, self.height)
        
        collision = False
        for obstacle in map_obstacles:
            if player_rect.colliderect(obstacle):
                collision = True
                break
        
        # 如果沒有碰撞，應用移動
        if not collision:
            self.x = new_x
            self.y = new_y
        
        # 更新相機位置（只有真人玩家需要）
        if self.is_human:
            self._update_camera()
    
    def _update_camera(self):
        """
        更新相機位置（讓玩家保持在螢幕中央）\n
        """
        # 計算相機偏移，讓玩家保持在螢幕中央
        self.camera_x = self.x - SCREEN_WIDTH // 2
        self.camera_y = self.y - SCREEN_HEIGHT // 2
        
        # 限制相機不超出地圖邊界
        self.camera_x = max(0, min(HIDE_SEEK_MAP["map_width"] - SCREEN_WIDTH, self.camera_x))
        self.camera_y = max(0, min(HIDE_SEEK_MAP["map_height"] - SCREEN_HEIGHT, self.camera_y))
    
    def _handle_human_attack(self, keys, other_players, sounds=None):
        """
        處理真人玩家攻擊\n
        \n
        參數:\n
        keys (dict): 按鍵狀態\n
        other_players (list): 其他玩家列表\n
        sounds (dict): 音效物件字典\n
        \n
        回傳:\n
        dict: 攻擊結果 {"attacked": bool, "target": HideSeekPlayer}\n
        """
        if keys[pygame.K_SPACE] and self.special_attack_cooldown == 0:
            return self._perform_special_attack(other_players, sounds)
        return {"attacked": False, "target": None}
    
    def _handle_ai_attack(self, other_players, sounds=None):
        """
        處理AI玩家攻擊\n
        \n
        參數:\n
        other_players (list): 其他玩家列表\n
        sounds (dict): 音效物件字典\n
        \n
        回傳:\n
        dict: 攻擊結果 {"attacked": bool, "target": HideSeekPlayer}\n
        """
        if self.special_attack_cooldown > 0:
            return {"attacked": False, "target": None}
        
        # AI攻擊邏輯：如果有目標在攻擊範圍內就攻擊
        for player in other_players:
            if player.alive and player.role != self.role:
                distance = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
                if distance <= HIDE_SEEK_COMBAT["special_attack_range"]:
                    return self._perform_special_attack(other_players, sounds)
        
        return {"attacked": False, "target": None}
    
    def _perform_special_attack(self, other_players, sounds=None):
        """
        執行特殊攻擊\n
        \n
        參數:\n
        other_players (list): 其他玩家列表\n
        sounds (dict): 音效物件字典\n
        \n
        回傳:\n
        dict: 攻擊結果 {"attacked": bool, "target": HideSeekPlayer}\n
        """
        self.special_attack_cooldown = HIDE_SEEK_COMBAT["special_attack_cooldown"]
        
        # 播放攻擊音效
        if sounds:
            from config import play_sound
            play_sound(sounds, "laser_shoot", volume=0.8)
        
        # 尋找攻擊範圍內的目標
        for player in other_players:
            if not player.alive or player.invulnerable:
                continue
            
            distance = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
            if distance <= HIDE_SEEK_COMBAT["special_attack_range"]:
                # 根據角色身分決定攻擊效果
                if self.role == "seeker" and player.role == "hider":
                    # 搜尋者攻擊躲藏者：一擊致命
                    if not player.shielded:
                        player.health = 0
                        player.alive = False
                        print(f"搜尋者 {self.name} 擊殺了躲藏者 {player.name}")
                        return {"attacked": True, "target": player}
                    else:
                        print(f"躲藏者 {player.name} 的護盾擋住了攻擊")
                
                elif self.role == "hider" and player.role == "seeker":
                    # 躲藏者攻擊搜尋者：冰凍效果
                    if not player.freeze_immune:
                        player.frozen = True
                        # 隨機設定凍結時間為 0.5-1 秒（60fps，所以 30-60 幀）- 從原本1-3秒縮短
                        freeze_frames = random.randint(30, 60)  # 30-60幀 = 0.5-1秒
                        player.freeze_timer = freeze_frames
                        freeze_seconds = freeze_frames / 60
                        print(f"躲藏者 {self.name} 冰凍了搜尋者 {player.name}，持續時間：{freeze_seconds:.1f}秒")
                        return {"attacked": True, "target": player}
                    else:
                        print(f"搜尋者 {player.name} 免疫冰凍效果")
        
        print(f"玩家 {self.name} 攻擊落空")
        return {"attacked": False, "target": None}
    
    def use_potion(self):
        """
        使用道具\n
        \n
        回傳:\n
        bool: 是否成功使用道具\n
        """
        if self.potion_uses <= 0:
            return False
        
        potion_config = HIDE_SEEK_POTIONS[self.potion_type]
        self.potion_uses -= 1
        
        if self.potion_type == "speed_boost":
            self.speed_boosted = True
            self.speed_boost_timer = potion_config["duration"]
        
        elif self.potion_type == "invisibility":
            self.invisible = True
            self.invisible_timer = potion_config["duration"]
        
        elif self.potion_type == "shield":
            self.shielded = True
            self.shield_timer = potion_config["duration"]
        
        elif self.potion_type == "freeze_immunity":
            self.freeze_immune = True
            self.freeze_immune_timer = potion_config["duration"]
        
        elif self.potion_type == "teleport":
            # 隨機傳送到地圖上的安全位置
            safe_x = random.randint(50, HIDE_SEEK_MAP["map_width"] - 50)
            safe_y = random.randint(50, HIDE_SEEK_MAP["map_height"] - 50)
            self.teleport_to_position(safe_x, safe_y)
        
        print(f"玩家 {self.name} 使用了 {potion_config['name']}，剩餘 {self.potion_uses} 次")
        return True
    
    def _handle_ai_potion_use(self):
        """
        AI道具使用邏輯\n
        """
        if self.potion_uses <= 0:
            return
        
        # 檢查冷卻時間
        current_time = pygame.time.get_ticks()
        if current_time - self.ai_last_potion_use < HIDE_SEEK_AI["potion_use_cooldown"] * 1000 / 60:
            return
        
        # 根據情況決定是否使用道具
        should_use = False
        
        if self.health < HIDE_SEEK_AI["potion_use_health_threshold"]:
            should_use = True
        elif self.potion_type == "teleport" and self.health < 30:
            should_use = True
        elif self.frozen and self.potion_type == "freeze_immunity":
            should_use = True
        
        if should_use:
            if self.use_potion():
                self.ai_last_potion_use = current_time
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """
        繪製玩家太空船\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        camera_x (int): 相機X偏移\n
        camera_y (int): 相機Y偏移\n
        """
        if not self.alive:
            return
        
        # 計算螢幕位置
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # 如果超出螢幕範圍就不繪製
        if (screen_x < -self.width or screen_x > SCREEN_WIDTH + self.width or
            screen_y < -self.height or screen_y > SCREEN_HEIGHT + self.height):
            return
        
        # 根據隱形狀態調整透明度
        alpha = 255
        if self.invisible:
            alpha = int(255 * HIDE_SEEK_POTIONS["invisibility"]["effect_multiplier"])
        
        # 根據太空船樣式繪製
        self._draw_spaceship_shape(screen, screen_x, screen_y, alpha)
        
        # 繪製狀態效果
        self._draw_status_effects(screen, screen_x, screen_y)
        
        # 繪製玩家名稱
        self._draw_player_name(screen, screen_x, screen_y)
    
    def _draw_spaceship_shape(self, screen, x, y, alpha):
        """
        根據樣式繪製太空船形狀\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        x (int): 螢幕X座標\n
        y (int): 螢幕Y座標\n
        alpha (int): 透明度 (0-255)\n
        """
        # 創建透明表面
        spaceship_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.shape == "triangle":
            points = [
                (self.width // 2, 0),
                (0, self.height),
                (self.width, self.height)
            ]
            pygame.draw.polygon(spaceship_surface, (*self.primary_color, alpha), points)
            pygame.draw.polygon(spaceship_surface, (*self.secondary_color, alpha), points, 2)
        
        elif self.shape == "diamond":
            points = [
                (self.width // 2, 0),
                (self.width, self.height // 2),
                (self.width // 2, self.height),
                (0, self.height // 2)
            ]
            pygame.draw.polygon(spaceship_surface, (*self.primary_color, alpha), points)
            pygame.draw.polygon(spaceship_surface, (*self.secondary_color, alpha), points, 2)
        
        elif self.shape == "arrow":
            points = [
                (self.width // 2, 0),
                (self.width // 4, self.height // 3),
                (self.width * 3 // 4, self.height // 3),
                (self.width * 3 // 4, self.height),
                (self.width // 4, self.height)
            ]
            pygame.draw.polygon(spaceship_surface, (*self.primary_color, alpha), points)
            pygame.draw.polygon(spaceship_surface, (*self.secondary_color, alpha), points, 2)
        
        elif self.shape == "star":
            # 簡化的星形（用多個三角形組成）
            center_x = self.width // 2
            center_y = self.height // 2
            radius = min(self.width, self.height) // 2
            
            # 繪製圓形作為星形的簡化版本
            pygame.draw.circle(spaceship_surface, (*self.primary_color, alpha), (center_x, center_y), radius)
            pygame.draw.circle(spaceship_surface, (*self.secondary_color, alpha), (center_x, center_y), radius, 2)
        
        elif self.shape == "hexagon":
            center_x = self.width // 2
            center_y = self.height // 2
            radius = min(self.width, self.height) // 2
            
            points = []
            for i in range(6):
                angle = i * math.pi / 3
                px = center_x + radius * math.cos(angle)
                py = center_y + radius * math.sin(angle)
                points.append((px, py))
            
            pygame.draw.polygon(spaceship_surface, (*self.primary_color, alpha), points)
            pygame.draw.polygon(spaceship_surface, (*self.secondary_color, alpha), points, 2)
        
        # 將太空船表面繪製到主螢幕
        screen.blit(spaceship_surface, (x - self.width // 2, y - self.height // 2))
    
    def _draw_status_effects(self, screen, x, y):
        """
        繪製狀態效果指示\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        x (int): 螢幕X座標\n
        y (int): 螢幕Y座標\n
        """
        effect_y = y - self.height // 2 - 10
        
        # 冰凍效果
        if self.frozen:
            pygame.draw.circle(screen, CYAN, (x, effect_y), 5)
            effect_y -= 12
        
        # 護盾效果
        if self.shielded:
            pygame.draw.circle(screen, BLUE, (x, effect_y), 8, 2)
            effect_y -= 12
        
        # 加速效果
        if self.speed_boosted:
            pygame.draw.circle(screen, GREEN, (x, effect_y), 4)
            effect_y -= 12
        
        # 防凍效果
        if self.freeze_immune:
            pygame.draw.circle(screen, ORANGE, (x, effect_y), 4)
            effect_y -= 12
    
    def _draw_player_name(self, screen, x, y):
        """
        繪製玩家名稱\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面\n
        x (int): 螢幕X座標\n
        y (int): 螢幕Y座標\n
        """
        font = create_font(FONT_SIZES["small"])
        
        # 根據角色身分選擇顏色
        if self.role == "seeker":
            name_color = RED
        else:
            name_color = GREEN
        
        name_text = font.render(self.name, True, name_color)
        name_rect = name_text.get_rect(center=(x, y + self.height // 2 + 15))
        screen.blit(name_text, name_rect)
    
    def get_rect(self):
        """
        取得玩家的碰撞矩形\n
        \n
        回傳:\n
        pygame.Rect: 碰撞矩形\n
        """
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)