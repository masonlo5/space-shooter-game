######################載入套件######################
import pygame

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