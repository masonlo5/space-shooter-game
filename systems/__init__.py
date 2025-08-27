"""
######################遊戲系統模組######################

此模組包含所有遊戲系統功能：
- collision: 碰撞檢測系統
- ui: 使用者介面系統
- shop: 商店系統
- menu: 主畫面系統
- ship_battle: Ship Battle 對戰系統
- visual_effects: 視覺效果系統

這些系統負責處理遊戲邏輯，與遊戲物件分離，提高程式碼的模組化程度。
"""

from .collision import check_collision
from .ui import UISystem
from .shop import ShopSystem
from .menu import MenuSystem
from .ship_battle import ShipBattleSystem
from .visual_effects import VisualEffectsSystem

__all__ = ['check_collision', 'UISystem', 'ShopSystem', 'MenuSystem', 'ShipBattleSystem', 'VisualEffectsSystem']