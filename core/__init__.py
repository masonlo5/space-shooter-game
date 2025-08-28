"""
######################核心系統模組######################

此模組包含重構後的核心遊戲系統：
- event_manager: 事件處理系統
- state_manager: 遊戲狀態管理系統
- renderer: 渲染管理系統
- game_controller: 主遊戲控制器

這些核心系統負責協調整個遊戲的運行，提供清晰的職責分離。
"""

# 延遲導入以避免循環依賴
def get_event_manager():
    from .event_manager import EventManager
    return EventManager

def get_state_manager():
    from .state_manager import StateManager
    return StateManager

def get_renderer():
    from .renderer import Renderer
    return Renderer

def get_game_controller():
    from .game_controller import GameController
    return GameController

__all__ = ['get_event_manager', 'get_state_manager', 'get_renderer', 'get_game_controller']