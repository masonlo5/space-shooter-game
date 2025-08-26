"""
######################遊戲系統模組######################

此模組包含所有遊戲系統功能：
- collision: 碰撞檢測系統
- ui: 使用者介面系統
- shop: 商店系統

這些系統負責處理遊戲邏輯，與遊戲物件分離，提高程式碼的模組化程度。
"""

from .collision import check_collision
from .ui import UISystem
from .shop import ShopSystem

__all__ = ['check_collision', 'UISystem', 'ShopSystem']