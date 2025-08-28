######################載入套件######################
import pygame
import os

######################字體系統設定######################
# 繁體中文字體檔案路徑（依序嘗試）
CHINESE_FONT_FILES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",        # macOS 黑體（推薦）
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # Arial Unicode 
    "/Library/Fonts/Arial Unicode.ttf",                # 備用 Arial Unicode
    "/System/Library/Fonts/STHeiti Light.ttc"          # 備用黑體
]

def get_working_font_path():
    """
    測試並返回第一個可用的中文字體檔案路徑
    
    回傳:
    str 或 None: 可用的字體檔案路徑，或 None 表示使用預設字體
    """
    import os
    import pygame.font
    
    pygame.font.init()
    
    for font_path in CHINESE_FONT_FILES:
        if os.path.exists(font_path):
            try:
                # 測試字體檔案是否可以正常載入
                test_font = pygame.font.Font(font_path, 24)
                # 測試是否能渲染中文字元
                test_surface = test_font.render("測試中文", True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    return font_path
            except:
                continue
    
    # 如果所有字體檔案都不可用，返回 None
    return None

def create_font(size):
    """
    創建支援繁體中文的字體物件 - 使用直接字體檔案路徑
    
    參數:
    size (int): 字體大小
    
    回傳:
    pygame.font.Font: 字體物件
    """
    import pygame.font
    
    pygame.font.init()
    
    # 取得可用的字體檔案路徑
    font_path = get_working_font_path()
    
    if font_path:
        try:
            # 使用字體檔案直接創建字體物件
            return pygame.font.Font(font_path, size)
        except Exception as e:
            print(f"警告：無法載入字體檔案 {font_path}: {e}")
    
    # 如果字體檔案不可用，嘗試系統字體作為最後備援
    try:
        return pygame.font.SysFont("Arial", size)
    except:
        # 最後的備援：pygame 預設字體
        return pygame.font.Font(None, size)

# 字體大小設定
FONT_SIZES = {
    "extra_large": 72,    # 超大字體（標題）
    "large": 48,          # 大字體（副標題）
    "medium": 36,         # 中等字體（按鈕）
    "normal": 24,         # 一般字體（內容）
    "small": 20,          # 小字體（說明）
    "mini": 16            # 極小字體（註解）
}

######################遊戲基本設定######################
# 螢幕尺寸設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

######################顏色定義######################
# 基本顏色（RGB格式）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

######################遊戲平衡參數######################
# 商店系統設定
SHOP_UNLOCK_STARS = 40  # 解鎖商店需要的星星數量

# 敵人生成設定
ENEMY_SPAWN_DELAY = 60  # 每60幀（約1秒）生成一個敵人
BOSS_SPAWN_BASE_CHANCE = 500  # Boss生成基礎機率

# Boss戰系統設定
BOSS_TRIGGER_KILLS = 60  # 擊敗60個敵人後出現Boss
BOSS_GARBAGE_ATTACK_INTERVAL = 120  # Boss垃圾攻擊間隔（2秒）
BOSS_SPECIAL_ATTACK_INTERVAL = 300  # Boss特殊攻擊間隔（5秒）
BOSS_GARBAGE_DAMAGE = 20  # Boss垃圾攻擊傷害
BOSS_SPECIAL_BULLET_COUNT = 7  # Boss扇形散彈數量

# 主畫面系統設定
MENU_TITLE_SIZE = 72  # 主畫面標題字體大小
MENU_BUTTON_SIZE = 36  # 主畫面按鈕字體大小
MENU_BUTTON_WIDTH = 200  # 按鈕寬度
MENU_BUTTON_HEIGHT = 60  # 按鈕高度

# 道具掉落機率
POWERUP_DROP_CHANCE = 30  # 30%機率掉落道具
STAR_DROP_CHANCE = 15     # 15%機率掉星星
HEALTH_POTION_CHANCE = 5  # 5%機率掉回血藥水
SPEED_POTION_CHANCE = 5   # 5%機率掉加速藥水
PROTECT_POTION_CHANCE = 3 # 3%機率掉防護藥水
BOMB_CHANCE = 2           # 2%機率掉炸彈

######################武器系統設定######################
# 武器類型和傷害值
WEAPON_STATS = {
    "basic": {
        "damage": 15,
        "color": YELLOW,
        "width": 4,
        "height": 10,
        "price": 0
    },
    "laser": {
        "damage": 25,
        "color": RED,
        "width": 6,
        "height": 15,
        "price": 15
    },
    "plasma": {
        "damage": 40,
        "color": PURPLE,
        "width": 8,
        "height": 12,
        "price": 25
    },
    "missile": {
        "damage": 60,
        "color": ORANGE,
        "width": 10,
        "height": 20,
        "price": 50
    },
    "ion_cannon": {
        "damage": 80,
        "color": CYAN,
        "width": 12,
        "height": 25,
        "price": 80
    }
}

######################太空船系統設定######################
# 太空船類型和屬性
SPACESHIP_STATS = {
    "explorer": {
        "max_health": 100,
        "speed": 5,
        "width": 50,
        "height": 40,
        "color": CYAN,
        "special_cooldown": 120,
        "price": 0
    },
    "fighter": {
        "max_health": 120,
        "speed": 6,
        "width": 45,
        "height": 35,
        "color": GREEN,
        "special_cooldown": 180,
        "price": 40
    },
    "interceptor": {
        "max_health": 80,
        "speed": 8,
        "width": 40,
        "height": 30,
        "color": YELLOW,
        "special_cooldown": 150,
        "price": 80
    },
    "destroyer": {
        "max_health": 150,
        "speed": 4,
        "width": 60,
        "height": 50,
        "color": PURPLE,
        "special_cooldown": 240,
        "price": 120
    },
    "battleship": {
        "max_health": 200,
        "speed": 3,
        "width": 70,
        "height": 60,
        "color": MAGENTA,
        "special_cooldown": 300,
        "price": 200
    }
}

######################敵人系統設定######################
# 敵人類型和屬性
ENEMY_STATS = {
    "basic": {
        "width": 30,
        "height": 25,
        "health": 30,
        "speed": 2,
        "color": RED,
        "score": 10,
        "stars": 1
    },
    "fast": {
        "width": 25,
        "height": 20,
        "health": 20,
        "speed": 4,
        "color": ORANGE,
        "score": 15,
        "stars": 1
    },
    "boss": {
        "width": 80,
        "height": 60,
        "health": 300,
        "speed": 1,
        "color": PURPLE,
        "score": 100,
        "stars": 20
    }
}

######################Boss攻擊系統設定######################
# Boss子彈類型和屬性
BOSS_BULLET_STATS = {
    "garbage": {
        "width": 8,
        "height": 8,
        "speed": 3,
        "color": (139, 69, 19),  # 棕色垃圾
        "damage": 20
    },
    "spread": {
        "width": 6,
        "height": 12,
        "speed": 4,
        "color": RED,
        "damage": 15
    }
}

######################禮物系統設定######################
# 禮物道具屬性
GIFT_STATS = {
    "width": 25,
    "height": 25,
    "color": (255, 215, 0),  # 金色
    "speed": 2
}

######################商店物品設定######################
# 商店物品列表
SHOP_ITEMS = {
    "potions": {
        "health_potion": {"name": "Health Potion", "price": 5, "key": "1"},
        "speed_boost": {"name": "Speed Boost", "price": 10, "key": "2"}
    },
    "weapons": {
        "laser": {"name": "Laser Weapon", "price": 15, "key": "3"},
        "plasma": {"name": "Plasma Weapon", "price": 25, "key": "4"},
        "missile": {"name": "Missile Launcher", "price": 50, "key": "5"},
        "ion_cannon": {"name": "Ion Cannon", "price": 80, "key": "6"}
    },
    "spaceships": {
        "fighter": {"name": "Fighter Ship", "price": 40, "key": "7"},
        "interceptor": {"name": "Interceptor Ship", "price": 80, "key": "8"},
        "destroyer": {"name": "Destroyer Ship", "price": 120, "key": "9"},
        "battleship": {"name": "Battleship", "price": 200, "key": "0"}
    }
}

######################Ship Battle 模式設定######################
# 機器人對手設定
ROBOT_STATS = {
    "name": "RoboWarrior",
    "initial_health": 100,
    "health_potion_count": 1,
    "health_potion_heal": 50,
    "move_speed": 3,
    "shoot_cooldown": 30,  # 每0.5秒可以射擊一次
    "special_attack_cooldown": 240,  # 每4秒可以使用特殊攻擊
    "health_potion_use_threshold": 30,  # 血量低於30時自動使用血瓶
    "color": RED
}

# Ship Battle 對戰設定
SHIP_BATTLE_STATS = {
    "initial_health": 100,
    "health_potion_count": 1,
    "health_potion_heal": 50,
    "prepare_time": 300,  # 戰鬥開始前等待時間（5秒）
    "screen_boundary_margin": 10,  # 螢幕邊界保留距離
    "victory_display_time": 180,  # 勝利/失敗畫面顯示時間（3秒）
}

# Ship Battle 視覺效果設定
SHIP_BATTLE_EFFECTS = {
    "snowflake": {
        "count": 50,  # 雪花數量
        "fall_speed": 2,  # 雪花下降速度
        "size_min": 2,  # 最小雪花大小
        "size_max": 4,  # 最大雪花大小
        "color": WHITE
    },
    "crow": {
        "count": 3,  # 烏鴉數量
        "fly_speed": 4,  # 烏鴉飛行速度
        "width": 20,  # 烏鴉寬度
        "height": 15,  # 烏鴉高度
        "color": BLACK
    }
}

# Ship Battle UI 設定
SHIP_BATTLE_UI = {
    "health_bar_width": 200,
    "health_bar_height": 20,
    "health_bar_y": 30,
    "player_health_x": 50,
    "robot_health_x": SCREEN_WIDTH - 250,
    "name_font_size": 24,
    "prepare_font_size": 48,
    "result_font_size": 72
}

######################躲貓貓遊戲設定######################
# 躲貓貓遊戲狀態常數
GAME_STATE_HIDE_SEEK = "hide_seek"
GAME_STATE_HIDE_SEEK_LOBBY = "hide_seek_lobby"
GAME_STATE_HIDE_SEEK_TELEPORT = "hide_seek_teleport"
GAME_STATE_HIDE_SEEK_ROLE_REVEAL = "hide_seek_role_reveal"
GAME_STATE_HIDE_SEEK_PLAYING = "hide_seek_playing"
GAME_STATE_HIDE_SEEK_GHOST = "hide_seek_ghost"

# 躲貓貓設定
HIDE_SEEK_SETTINGS = {
    "total_players": 5,               # 總玩家數（1真人+4AI）
    "seekers_count": 2,               # 搜尋者數量
    "hiders_count": 3,                # 躲藏者數量
    "game_duration": 3600,            # 遊戲持續時間（60秒）
    "lobby_duration": 300,            # 大廳階段時間（5秒）
    "teleport_duration": 180,         # 傳送階段時間（3秒）
    "role_reveal_duration": 180,      # 角色顯示階段時間（3秒）
    "fps": 60,                        # 遊戲幀率
}

# 躲貓貓地圖設定
HIDE_SEEK_MAP = {
    "map_width": 1600,        # 地圖實際寬度（比螢幕大）
    "map_height": 1200,       # 地圖實際高度（比螢幕大）
    "obstacle_count": 15,     # 障礙物數量
    "obstacle_min_size": 40,  # 障礙物最小尺寸
    "obstacle_max_size": 120, # 障礙物最大尺寸
    "spawn_area_size": 100,   # 初始出生區域大小
    "safe_distance": 150      # 傳送時玩家間的安全距離
}

# 躲貓貓太空船外觀設定（5種不同外觀）
HIDE_SEEK_SPACESHIP_STYLES = {
    "style_1": {
        "primary_color": CYAN,
        "secondary_color": BLUE,
        "shape": "triangle",
        "size_modifier": 1.0
    },
    "style_2": {
        "primary_color": GREEN,
        "secondary_color": (0, 200, 0),
        "shape": "diamond",
        "size_modifier": 1.1
    },
    "style_3": {
        "primary_color": YELLOW,
        "secondary_color": ORANGE,
        "shape": "arrow",
        "size_modifier": 0.9
    },
    "style_4": {
        "primary_color": PURPLE,
        "secondary_color": MAGENTA,
        "shape": "star",
        "size_modifier": 1.2
    },
    "style_5": {
        "primary_color": RED,
        "secondary_color": (200, 0, 0),
        "shape": "hexagon",
        "size_modifier": 1.0
    }
}

# 躲貓貓道具系統（5種藥水，每種限用3次）
HIDE_SEEK_POTIONS = {
    "speed_boost": {
        "name": "加速藥水",
        "color": GREEN,
        "duration": 300,       # 持續5秒
        "effect_multiplier": 1.5,
        "uses": 3
    },
    "invisibility": {
        "name": "隱形藥水",
        "color": (100, 100, 100),
        "duration": 180,       # 持續3秒
        "effect_multiplier": 0.3,  # 透明度
        "uses": 3
    },
    "shield": {
        "name": "護盾藥水",
        "color": BLUE,
        "duration": 600,       # 持續10秒
        "effect_multiplier": 1.0,
        "uses": 3
    },
    "freeze_immunity": {
        "name": "防凍藥水",
        "color": ORANGE,
        "duration": 900,       # 持續15秒
        "effect_multiplier": 1.0,
        "uses": 3
    },
    "teleport": {
        "name": "瞬移藥水",
        "color": PURPLE,
        "duration": 0,         # 瞬間效果
        "effect_multiplier": 1.0,
        "uses": 3
    }
}

# 躲貓貓戰鬥系統設定
HIDE_SEEK_COMBAT = {
    "special_attack_cooldown": 60,     # 特殊攻擊冷卻時間（1秒）
    "special_attack_range": 80,        # 特殊攻擊範圍
    "freeze_duration": 180,            # 冰凍持續時間（3秒）
    "seeker_attack_damage": 100,       # 搜尋者攻擊傷害（一擊致命）
    "hider_attack_effect": "freeze",   # 躲藏者攻擊效果（冰凍）
    "invulnerable_time": 60           # 受到攻擊後無敵時間（1秒）
}

# 躲貓貓小地圖設定
HIDE_SEEK_MINIMAP = {
    "width": 200,
    "height": 150,
    "x": SCREEN_WIDTH - 220,
    "y": SCREEN_HEIGHT - 170,
    "background_color": (0, 0, 0, 128),
    "border_color": WHITE,
    "player_dot_size": 3,
    "seeker_color": RED,
    "hider_color": GREEN,
    "ghost_color": (100, 100, 100),
    "self_color": YELLOW,
    "scale_factor": 0.125  # 地圖縮放比例
}

# 躲貓貓UI設定
HIDE_SEEK_UI = {
    "timer_font_size": 36,
    "role_font_size": 48,
    "potion_icon_size": 30,
    "potion_counter_font_size": 24,
    "status_font_size": 28,
    "ghost_message_font_size": 32,
    "countdown_font_size": 72
}

# 躲貓貓AI行為設定
######################躲貓貓AI行為設定######################
HIDE_SEEK_AI = {
    "movement_change_interval": 60,    # AI每1秒改變移動方向（更快反應）
    "seek_update_interval": 30,        # 搜尋者AI每0.5秒更新目標（更頻繁）
    "hide_flee_distance": 250,         # 躲藏者發現搜尋者時的逃跑距離
    "patrol_radius": 800,              # 搜尋者巡邏半徑（大幅增加）
    "global_search_radius": 2000,      # 全地圖搜索範圍
    "random_movement_chance": 20,      # 20%機率進行隨機移動（減少隨機性）
    "aggressive_pursuit": True,        # 開啟積極追擊模式
    "potion_use_health_threshold": 50, # AI在血量低於50%時使用道具
    "potion_use_cooldown": 600         # AI使用道具的冷卻時間（10秒）
}

######################Boss Fight 模式設定######################
# Boss Fight 遊戲狀態
GAME_STATE_BOSS_FIGHT_MODE = "boss_fight_mode"

# Boss Fight 模式設定
BOSS_FIGHT_SETTINGS = {
    "total_bosses": 8,                    # 總共8個Boss
    "player_health": 100,                 # 玩家初始生命值
    "health_potion_count": 3,             # 治療藥水初始數量
    "health_potion_heal": 50,             # 每個藥水回復的生命值
    "victory_display_time": 180,          # 勝利畫面顯示時間（3秒）
    "defeat_display_time": 180,           # 失敗畫面顯示時間（3秒）
    "boss_spawn_delay": 120,              # Boss生成延遲時間（2秒）
}

# 8個Boss的詳細配置
BOSS_FIGHT_BOSSES = {
    1: {
        "name": "Asteroid Guardian",
        "health": 200,
        "speed": 1.5,
        "attack_damage": 15,
        "attack_cooldown": 90,
        "special_attack_cooldown": 300,
        "color": (150, 75, 0),
        "width": 60,
        "height": 45,
        "score": 100,
        "description": "第一關Boss - 小行星守護者"
    },
    2: {
        "name": "Plasma Sentinel",
        "health": 250,
        "speed": 2,
        "attack_damage": 20,
        "attack_cooldown": 75,
        "special_attack_cooldown": 270,
        "color": (0, 150, 75),
        "width": 65,
        "height": 50,
        "score": 150,
        "description": "第二關Boss - 等離子哨兵"
    },
    3: {
        "name": "Crystal Destroyer",
        "health": 300,
        "speed": 1.8,
        "attack_damage": 25,
        "attack_cooldown": 60,
        "special_attack_cooldown": 240,
        "color": (75, 0, 150),
        "width": 70,
        "height": 55,
        "score": 200,
        "description": "第三關Boss - 水晶毀滅者"
    },
    4: {
        "name": "Void Stalker",
        "health": 350,
        "speed": 2.5,
        "attack_damage": 30,
        "attack_cooldown": 50,
        "special_attack_cooldown": 210,
        "color": (100, 100, 100),
        "width": 75,
        "height": 60,
        "score": 250,
        "description": "第四關Boss - 虛空追蹤者"
    },
    5: {
        "name": "Nebula Warden",
        "health": 400,
        "speed": 2.2,
        "attack_damage": 35,
        "attack_cooldown": 45,
        "special_attack_cooldown": 180,
        "color": (150, 150, 0),
        "width": 80,
        "height": 65,
        "score": 300,
        "description": "第五關Boss - 星雲守護者"
    },
    6: {
        "name": "Cosmic Behemoth",
        "health": 500,
        "speed": 1.5,
        "attack_damage": 40,
        "attack_cooldown": 40,
        "special_attack_cooldown": 150,
        "color": (150, 0, 0),
        "width": 85,
        "height": 70,
        "score": 400,
        "description": "第六關Boss - 宇宙巨獸"
    },
    7: {
        "name": "Shadow Emperor",
        "health": 600,
        "speed": 3,
        "attack_damage": 45,
        "attack_cooldown": 35,
        "special_attack_cooldown": 120,
        "color": (50, 0, 50),
        "width": 90,
        "height": 75,
        "score": 500,
        "description": "第七關Boss - 暗影皇帝"
    },
    8: {
        "name": "Galaxy Overlord",
        "health": 800,
        "speed": 2.8,
        "attack_damage": 50,
        "attack_cooldown": 30,
        "special_attack_cooldown": 90,
        "color": (255, 0, 255),
        "width": 100,
        "height": 80,
        "score": 1000,
        "description": "最終Boss - 銀河霸主"
    }
}

# Boss Fight 治療藥水設定
BOSS_FIGHT_POTIONS = {
    "heal_amount": 50,                    # 每瓶藥水回復生命值
    "max_potions": 3,                     # 每場戰鬥最多藥水數
    "random_drop_chance": 30,             # 擊敗Boss後30%機率獲得額外藥水
    "potion_color": (0, 255, 0),          # 藥水顏色（綠色）
    "potion_size": 20                     # 藥水圖示大小
}

# Boss Fight UI設定
BOSS_FIGHT_UI = {
    "boss_health_bar_width": 400,
    "boss_health_bar_height": 20,
    "boss_health_bar_x": 200,
    "boss_health_bar_y": 50,
    "player_health_bar_width": 200,
    "player_health_bar_height": 15,
    "player_health_bar_x": 50,
    "player_health_bar_y": SCREEN_HEIGHT - 50,
    "potion_counter_x": 300,
    "potion_counter_y": SCREEN_HEIGHT - 50,
    "boss_name_font_size": 32,
    "progress_font_size": 24
}

######################遊戲狀態常數######################
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_BOSS_FIGHT = "boss_fight"
GAME_STATE_VICTORY = "victory"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_SHIP_BATTLE = "ship_battle"
GAME_STATE_HIDE_SEEK = "hide_seek"