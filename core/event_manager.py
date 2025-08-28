######################載入套件######################
import pygame
from config import (
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT,
    GAME_STATE_VICTORY, GAME_STATE_GAME_OVER, GAME_STATE_SHIP_BATTLE,
    GAME_STATE_HIDE_SEEK, SHOP_UNLOCK_STARS
)

######################事件管理器######################
class EventManager:
    """
    事件管理系統 - 負責處理所有遊戲事件\n
    \n
    負責處理:\n
    1. 統一的事件處理入口\n
    2. 不同遊戲狀態的事件分發\n
    3. 鍵盤、滑鼠、文字輸入事件\n
    4. 事件到動作的轉換\n
    """
    
    def __init__(self):
        """
        初始化事件管理器\n
        """
        pass
    
    def handle_events(self, game_state, systems, player=None, shop_open=False):
        """
        處理所有遊戲事件\n
        \n
        參數:\n
        game_state (str): 當前遊戲狀態\n
        systems (dict): 遊戲系統字典\n
        player (Player): 玩家物件（可選）\n
        shop_open (bool): 商店是否開啟\n
        \n
        回傳:\n
        dict: 包含事件處理結果的字典\n
        """
        events_result = {
            'running': True,
            'state_change': None,
            'shop_toggle': None,
            'shop_request': False,
            'purchase_key': None,
            'special_bullets': [],
            'reset_required': False
        }
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events_result['running'] = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event, game_state, systems, events_result)
            
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event, game_state, systems, player, shop_open, events_result)
            
            elif event.type == pygame.TEXTINPUT:
                self._handle_text_input(event, game_state, systems)
        
        return events_result
    
    def _handle_mouse_click(self, event, game_state, systems, events_result):
        """
        處理滑鼠點擊事件\n
        """
        if game_state == GAME_STATE_MENU and event.button == 1:  # 左鍵點擊
            action = systems['menu'].handle_click(event.pos)
            if action == "start_game":
                events_result['state_change'] = GAME_STATE_PLAYING
                events_result['reset_required'] = True
            elif action == "ship_battle":
                events_result['state_change'] = GAME_STATE_SHIP_BATTLE
            elif action == "hide_seek":
                events_result['state_change'] = GAME_STATE_HIDE_SEEK
    
    def _handle_key_press(self, event, game_state, systems, player, shop_open, events_result):
        """
        處理按鍵事件\n
        """
        if game_state == GAME_STATE_MENU:
            self._handle_menu_keys(event, systems, events_result)
        
        elif game_state == GAME_STATE_SHIP_BATTLE:
            # Ship Battle 模式的按鍵由系統內部處理
            pass
        
        elif game_state == GAME_STATE_HIDE_SEEK:
            self._handle_hide_seek_keys(event, systems, events_result)
        
        elif game_state in [GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT]:
            self._handle_game_keys(event, systems, player, shop_open, events_result)
        
        elif game_state in [GAME_STATE_VICTORY, GAME_STATE_GAME_OVER]:
            self._handle_end_game_keys(event, events_result)
    
    def _handle_menu_keys(self, event, systems, events_result):
        """
        處理主畫面按鍵\n
        """
        if systems['menu'].is_editing_name:
            systems['menu'].handle_text_input(event)
        else:
            action = systems['menu'].handle_key_press(event.key)
            if action == "start_game":
                events_result['state_change'] = GAME_STATE_PLAYING
                events_result['reset_required'] = True
            elif action == "ship_battle":
                events_result['state_change'] = GAME_STATE_SHIP_BATTLE
            elif action == "hide_seek":
                events_result['state_change'] = GAME_STATE_HIDE_SEEK
    
    def _handle_hide_seek_keys(self, event, systems, events_result):
        """
        處理躲貓貓模式按鍵\n
        """
        if systems.get('hide_seek'):
            result = systems['hide_seek'].handle_key_press(event.key)
            if result == "return_to_menu":
                events_result['state_change'] = GAME_STATE_MENU
    
    def _handle_game_keys(self, event, systems, player, shop_open, events_result):
        """
        處理遊戲中的按鍵\n
        """
        # 導入 StateManager 來取得 stars，避免直接使用 global
        
        if shop_open:
            # 商店開啟時的按鍵處理
            if event.key == pygame.K_ESCAPE:
                events_result['shop_toggle'] = False
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                             pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                # 商店購買邏輯會由上層處理
                events_result['purchase_key'] = event.key
        else:
            # 遊戲中的按鍵處理
            if event.key == pygame.K_SPACE and player:
                # 按下空白鍵切換武器
                player.change_weapon()
            elif event.key == pygame.K_s:
                # 按下 S 鍵嘗試開啟商店（星星數檢查由上層處理）
                events_result['shop_request'] = True
            elif event.key == pygame.K_c and player:
                # 按下 C 鍵切換太空船
                player.change_spaceship()
            elif event.key == pygame.K_x and player:
                # 按下 X 鍵發動特殊攻擊
                special_bullets = player.special_attack()
                events_result['special_bullets'] = special_bullets
    
    def _handle_end_game_keys(self, event, events_result):
        """
        處理遊戲結束畫面按鍵\n
        """
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            events_result['state_change'] = GAME_STATE_MENU
        elif event.key == pygame.K_r:
            # 按 R 重新開始
            events_result['state_change'] = GAME_STATE_PLAYING
            events_result['reset_required'] = True
    
    def _handle_text_input(self, event, game_state, systems):
        """
        處理文字輸入事件\n
        """
        if game_state == GAME_STATE_MENU:
            systems['menu'].handle_text_input(event)