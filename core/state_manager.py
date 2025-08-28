######################載入套件######################
from config import (
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT,
    GAME_STATE_VICTORY, GAME_STATE_GAME_OVER, GAME_STATE_SHIP_BATTLE,
    GAME_STATE_HIDE_SEEK, BOSS_TRIGGER_KILLS
)

######################遊戲狀態管理器######################
class StateManager:
    """
    遊戲狀態管理系統 - 統一管理所有遊戲狀態和全域變數\n
    \n
    負責處理:\n
    1. 遊戲狀態切換管理\n
    2. 全域變數統一存取\n
    3. 狀態驗證和邏輯檢查\n
    4. Boss 戰觸發條件檢查\n
    """
    
    def __init__(self):
        """
        初始化狀態管理器\n
        """
        # 遊戲狀態
        self.game_state = GAME_STATE_MENU
        
        # 全域遊戲變數
        self.score = 0
        self.stars = 0
        self.boss_killed = False
        self.victory_timer = 0
        self.enemies_killed = 0
        
        # 其他狀態
        self.shop_open = False
    
    def reset_game_state(self):
        """
        重置遊戲狀態到初始值\n
        """
        self.score = 0
        self.stars = 0
        self.boss_killed = False
        self.victory_timer = 0
        self.enemies_killed = 0
        self.shop_open = False
    
    def set_game_state(self, new_state):
        """
        設定遊戲狀態\n
        \n
        參數:\n
        new_state (str): 新的遊戲狀態\n
        """
        valid_states = [
            GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT,
            GAME_STATE_VICTORY, GAME_STATE_GAME_OVER, GAME_STATE_SHIP_BATTLE,
            GAME_STATE_HIDE_SEEK
        ]
        
        if new_state in valid_states:
            self.game_state = new_state
            print(f"遊戲狀態切換到: {new_state}")
        else:
            print(f"警告：無效的遊戲狀態: {new_state}")
    
    def get_game_state(self):
        """
        取得當前遊戲狀態\n
        \n
        回傳:\n
        str: 當前遊戲狀態\n
        """
        return self.game_state
    
    def update_score(self, points):
        """
        更新分數\n
        \n
        參數:\n
        points (int): 要增加的分數\n
        """
        self.score += points
    
    def update_stars(self, amount):
        """
        更新星星數量\n
        \n
        參數:\n
        amount (int): 要增加的星星數量\n
        """
        self.stars += amount
        self.stars = max(0, self.stars)  # 確保不會是負數
    
    def spend_stars(self, amount):
        """
        消費星星\n
        \n
        參數:\n
        amount (int): 要消費的星星數量\n
        \n
        回傳:\n
        bool: 是否成功消費\n
        """
        if self.stars >= amount:
            self.stars -= amount
            return True
        return False
    
    def update_enemies_killed(self, count=1):
        """
        更新敵人擊殺數\n
        \n
        參數:\n
        count (int): 擊殺數量，預設為 1\n
        """
        self.enemies_killed += count
    
    def should_trigger_boss(self):
        """
        檢查是否應該觸發 Boss 戰\n
        \n
        回傳:\n
        bool: 是否應該觸發 Boss 戰\n
        """
        return (self.enemies_killed >= BOSS_TRIGGER_KILLS and 
                self.game_state == GAME_STATE_PLAYING)
    
    def trigger_boss_fight(self):
        """
        觸發 Boss 戰\n
        """
        if self.should_trigger_boss():
            self.set_game_state(GAME_STATE_BOSS_FIGHT)
            return True
        return False
    
    def set_boss_killed(self, victory_time=180):
        """
        設定 Boss 被擊敗\n
        \n
        參數:\n
        victory_time (int): 勝利畫面顯示時間（幀數）\n
        """
        self.boss_killed = True
        self.victory_timer = victory_time
    
    def update_victory_timer(self):
        """
        更新勝利計時器\n
        \n
        回傳:\n
        bool: 計時器是否結束\n
        """
        if self.victory_timer > 0:
            self.victory_timer -= 1
            if self.victory_timer <= 0:
                self.set_game_state(GAME_STATE_VICTORY)
                return True
        return False
    
    def toggle_shop(self, force_state=None):
        """
        切換商店開啟狀態\n
        \n
        參數:\n
        force_state (bool): 強制設定狀態，None 表示切換\n
        """
        if force_state is not None:
            self.shop_open = force_state
        else:
            self.shop_open = not self.shop_open
    
    def can_open_shop(self):
        """
        檢查是否可以開啟商店\n
        \n
        回傳:\n
        bool: 是否可以開啟商店\n
        """
        from config import SHOP_UNLOCK_STARS
        return self.stars >= SHOP_UNLOCK_STARS
    
    def get_boss_progress(self):
        """
        取得 Boss 出現進度\n
        \n
        回傳:\n
        dict: 包含進度資訊的字典\n
        """
        remaining = BOSS_TRIGGER_KILLS - self.enemies_killed
        return {
            'killed': self.enemies_killed,
            'required': BOSS_TRIGGER_KILLS,
            'remaining': max(0, remaining),
            'ready': remaining <= 0
        }
    
    def get_state_dict(self):
        """
        取得所有狀態的字典表示\n
        \n
        回傳:\n
        dict: 包含所有狀態的字典\n
        """
        return {
            'game_state': self.game_state,
            'score': self.score,
            'stars': self.stars,
            'boss_killed': self.boss_killed,
            'victory_timer': self.victory_timer,
            'enemies_killed': self.enemies_killed,
            'shop_open': self.shop_open
        }