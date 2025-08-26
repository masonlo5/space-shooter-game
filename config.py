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