"""
######################遊戲物件模組######################

此模組包含所有遊戲中的物件類別：
- Player: 玩家太空船
- Enemy: 敵人
- Bullet: 子彈
- PowerUp: 道具
- Firework: 煙火效果

所有物件都遵循統一的設計模式，包含移動、繪製、碰撞檢測等基本功能。
"""

from .player import Player
from .enemy import Enemy
from .bullet import Bullet
from .powerup import PowerUp
from .firework import Firework

__all__ = ['Player', 'Enemy', 'Bullet', 'PowerUp', 'Firework']