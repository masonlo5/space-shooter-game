######################載入套件######################
import pygame
import random
from config import SCREEN_HEIGHT, GIFT_STATS

######################道具掉落類別######################
class PowerUp:
    """
    道具掉落類別 - 處理各種掉落道具的行為和效果\n
    \n
    負責處理:\n
    1. 道具移動（向下飄落）\n
    2. 不同道具類型的外觀\n
    3. 道具效果的觸發\n
    4. Boss掉落的禮物系統\n
    5. 邊界檢測\n
    \n
    屬性:\n
    x (int): 道具的 x 座標\n
    y (int): 道具的 y 座標\n
    width (int): 道具寬度\n
    height (int): 道具高度\n
    powerup_type (str): 道具類型\n
    speed (int): 掉落速度\n
    """
    
    def __init__(self, x, y, powerup_type="star"):
        """
        初始化道具\n
        \n
        參數:\n
        x (int): 起始 x 座標\n
        y (int): 起始 y 座標\n
        powerup_type (str): 道具類型\n
        """
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.speed = 3
        
        # 根據道具類型設定不同的屬性
        from config import YELLOW, GREEN, BLUE, PURPLE, RED
        
        if powerup_type == "star":
            self.width = 15
            self.height = 15
            self.color = YELLOW
        elif powerup_type == "health_potion":
            self.width = 20
            self.height = 25
            self.color = GREEN
        elif powerup_type == "speed_potion":
            self.width = 20
            self.height = 25
            self.color = BLUE
        elif powerup_type == "protect_potion":
            self.width = 20
            self.height = 25
            self.color = PURPLE
        elif powerup_type == "bomb":
            self.width = 18
            self.height = 18
            self.color = RED
        elif powerup_type == "gift":
            # Boss掉落的禮物
            self.width = GIFT_STATS["width"]
            self.height = GIFT_STATS["height"]
            self.color = GIFT_STATS["color"]
            self.speed = GIFT_STATS["speed"]
    
    def move(self):
        """
        移動道具（向下飄落）\n
        """
        self.y += self.speed
    
    def draw(self, screen):
        """
        在螢幕上繪製道具\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        from config import WHITE, RED, BLACK, YELLOW, CYAN
        
        if self.powerup_type == "star":
            # 星星：五角星形狀
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            # 簡化版：畫一個亮點加上十字
            pygame.draw.circle(screen, self.color, (center_x, center_y), 6)
            pygame.draw.line(screen, WHITE, (center_x - 8, center_y), (center_x + 8, center_y), 2)
            pygame.draw.line(screen, WHITE, (center_x, center_y - 8), (center_x, center_y + 8), 2)
        elif self.powerup_type == "health_potion":
            # 回血藥水：綠色瓶子
            pygame.draw.rect(screen, self.color, (self.x, self.y + 5, self.width, self.height - 5))
            pygame.draw.rect(screen, WHITE, (self.x + 6, self.y, 8, 8))  # 瓶口
            pygame.draw.rect(screen, RED, (self.x + 4, self.y + 10, 4, 4))  # 十字標記
            pygame.draw.rect(screen, RED, (self.x + 2, self.y + 12, 8, 4))
        elif self.powerup_type == "speed_potion":
            # 加速藥水：藍色瓶子
            pygame.draw.rect(screen, self.color, (self.x, self.y + 5, self.width, self.height - 5))
            pygame.draw.rect(screen, WHITE, (self.x + 6, self.y, 8, 8))  # 瓶口
            # 閃電圖案
            points = [(self.x + 8, self.y + 8), (self.x + 12, self.y + 15), (self.x + 10, self.y + 15),
                     (self.x + 14, self.y + 22), (self.x + 10, self.y + 18), (self.x + 12, self.y + 18)]
            pygame.draw.polygon(screen, YELLOW, points)
        elif self.powerup_type == "protect_potion":
            # 防護藥水：紫色瓶子
            pygame.draw.rect(screen, self.color, (self.x, self.y + 5, self.width, self.height - 5))
            pygame.draw.rect(screen, WHITE, (self.x + 6, self.y, 8, 8))  # 瓶口
            # 盾牌圖案
            pygame.draw.circle(screen, CYAN, (self.x + 10, self.y + 15), 6, 2)
        elif self.powerup_type == "bomb":
            # 炸彈：紅色圓形
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.circle(screen, self.color, (center_x, center_y), 8)
            pygame.draw.circle(screen, BLACK, (center_x, center_y), 8, 2)
            # 引線
            pygame.draw.line(screen, BLACK, (center_x - 6, center_y - 6), (center_x - 10, center_y - 10), 2)
        elif self.powerup_type == "gift":
            # Boss掉落的禮物：金色禮物盒
            # 禮物盒主體
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            
            # 禮物盒裝飾：十字緞帶
            ribbon_color = RED
            # 垂直緞帶
            pygame.draw.rect(screen, ribbon_color, (self.x + self.width // 2 - 2, self.y, 4, self.height))
            # 水平緞帶
            pygame.draw.rect(screen, ribbon_color, (self.x, self.y + self.height // 2 - 2, self.width, 4))
            
            # 蝴蝶結
            bow_x = self.x + self.width // 2
            bow_y = self.y + 2
            pygame.draw.circle(screen, ribbon_color, (bow_x - 3, bow_y), 3)
            pygame.draw.circle(screen, ribbon_color, (bow_x + 3, bow_y), 3)
            pygame.draw.circle(screen, (139, 0, 0), (bow_x, bow_y), 2)  # 深紅色中心
            
            # 發光效果（簡單閃爍）
            if random.randint(1, 10) <= 3:  # 30%機率閃爍
                pygame.draw.rect(screen, WHITE, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 1)
    
    def is_off_screen(self):
        """
        檢查道具是否離開螢幕\n
        \n
        回傳:\n
        bool: 如果道具已經離開螢幕返回 True\n
        """
        return self.y > SCREEN_HEIGHT
    
    def apply_effect(self, player):
        """
        對玩家套用道具效果\n
        \n
        參數:\n
        player (Player): 玩家物件\n
        \n
        回傳:\n
        tuple: (is_fatal, stars_gained, should_return_to_menu) - 是否致命、獲得的星星數、是否返回主畫面\n
        """
        if self.powerup_type == "star":
            return False, 1, False  # 不致命，獲得1顆星星，不返回主畫面
        elif self.powerup_type == "health_potion":
            # 將藥水添加到玩家庫存而不是直接使用
            player.add_potion("health_potion")
            return False, 0, False
        elif self.powerup_type == "speed_potion":
            # 將藥水添加到玩家庫存而不是直接使用
            player.add_potion("speed_potion")
            return False, 0, False
        elif self.powerup_type == "protect_potion":
            # 將藥水添加到玩家庫存而不是直接使用
            player.add_potion("protect_potion")
            return False, 0, False
        elif self.powerup_type == "bomb":
            # 碰到炸彈會死亡
            player.health = 0
            return True, 0, False  # 致命，不獲得星星，不返回主畫面
        elif self.powerup_type == "gift":
            # Boss掉落的禮物：給玩家隨機藥水並返回主畫面
            random_potion = self._get_random_potion_effect(player)
            return False, 10, True  # 不致命，獲得10顆星星，返回主畫面
        
        return False, 0, False
    
    def _get_random_potion_effect(self, player):
        """
        獲得隨機藥水效果（內部方法）\n
        \n
        參數:\n
        player (Player): 玩家物件\n
        \n
        回傳:\n
        str: 獲得的藥水類型\n
        """
        # 隨機選擇一種藥水效果
        potion_types = ["health_potion", "speed_potion", "protect_potion"]
        chosen_potion = random.choice(potion_types)
        
        if chosen_potion == "health_potion":
            # 給玩家2個回血藥水作為Boss獎勵
            player.add_potion("health_potion")
            player.add_potion("health_potion")
            print("禮物效果：獲得 2 個強力回血藥水！")
        elif chosen_potion == "speed_potion":
            # 給玩家2個加速藥水作為Boss獎勵
            player.add_potion("speed_potion")
            player.add_potion("speed_potion")
            print("禮物效果：獲得 2 個強力加速藥水！")
        elif chosen_potion == "protect_potion":
            # 給玩家2個防護藥水作為Boss獎勵
            player.add_potion("protect_potion")
            player.add_potion("protect_potion")
            print("禮物效果：獲得 2 個強力防護藥水！")
        
        return chosen_potion