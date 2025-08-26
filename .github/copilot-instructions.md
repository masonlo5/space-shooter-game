# Galaxy Blaster - AI 程式設計助理指南

## 專案架構概覽

這是一個使用 Python + Pygame 開發的太空射擊遊戲，採用**完全模組化**的 MVC 架構設計。核心是 `main.py` 中的 `GameController` 類別，協調 `entities/` 物件和 `systems/` 服務層。

### 關鍵架構決策

- **模組分離**: `entities/` 存放遊戲物件，`systems/` 存放業務邏輯，`config.py` 統一管理遊戲參數
- **配置驅動**: 所有武器、太空船、敵人屬性都由 `config.py` 的字典定義，支援資料驅動的遊戲設計
- **全域狀態管理**: 使用 `main.py` 中的全域變數（`score`, `stars`, `boss_killed`, `victory_timer`）管理遊戲狀態

## 核心物件系統 (`entities/`)

- **Player**: 玩家太空船，支援 5 種可切換太空船類型，每種有獨特的特殊攻擊模式
- **Bullet**: 子彈系統，支援 5 種武器類型，外觀和傷害從 `WEAPON_STATS` 字典載入
- **Enemy**: 敵人系統，包含 3 種類型，屬性從 `ENEMY_STATS` 字典載入
- **PowerUp**: 道具系統，5 種掉落物（包括致命炸彈），支援複雜的效果邏輯
- **Firework**: 粒子系統，使用數學函數實現煙火爆炸效果

## 程式碼風格約定

### 必須遵循的規範

1. **使用 #todos 工具規劃後才能開始撰寫程式碼**
2. **模組化設計**: 新功能優先考慮放入 `systems/` 或新建模組，避免 `main.py` 過度膨脹
3. **配置驅動**: 新增遊戲物件時，優先在 `config.py` 建立參數字典，然後在類別中載入
4. **變數命名**: 統一使用 snake_case（如 `spaceship_type`, `shoot_cooldown`）
5. **類別命名**: 使用 PascalCase（如 `GameController`, `UISystem`）
6. **註解語言**: 統一使用繁體中文，使用白話文解釋邏輯
7. **區塊分隔**: 使用 `######################` 標記區塊
8. **文檔字串**: 使用 `"""` 三引號，包含功能描述、參數說明、回傳值

### 特殊編程約定

- **import 組織**: 按 標準庫 → 外部庫 → 本地模組 順序，使用 `from config import *` 載入常數
- **邊界檢查模式**: 使用 `min(max_value, current + increment)` 模式防止數值溢出
- **安全遍歷**: 遊戲物件列表使用 `for item in items[:]` 切片複製模式，避免修改時出錯
- **冷卻時間機制**: 所有時間控制使用幀計數器而非時間戳（如 `shoot_cooldown = 10`）

## 遊戲機制關鍵點

### 配置驅動設計模式

- **武器系統**: 所有屬性由 `WEAPON_STATS` 字典定義，新增武器只需修改配置
- **太空船系統**: `SPACESHIP_STATS` 定義所有屬性，`update_ship_stats()` 同步更新實例
- **敵人系統**: `ENEMY_STATS` 定義類型，支援動態屬性載入
- **商店系統**: `SHOP_ITEMS` 字典驅動商店界面和購買邏輯

### 全域狀態協調

- **遊戲狀態**: `main.py` 的全域變數（`score`, `stars`, `boss_killed`, `victory_timer`）作為唯一真相來源
- **物件間通信**: 透過 `GameController` 的方法參數傳遞狀態，避免物件間直接依賴
- **狀態切換**: `shop_open` 布林值控制商店/遊戲模式，影響事件處理和渲染邏輯

### 效能優化模式

- **安全列表遍歷**: `for bullet in bullets[:]` 模式處理動態修改的列表
- **邊界管理**: 及時移除螢幕外物件，使用 `is_off_screen()` 統一判斷
- **冷卻時間**: 基於幀計數的冷卻機制避免過度計算

## 開發工作流程

### 新增武器類型

1. 在 `config.py` 的 `WEAPON_STATS` 字典新增配置
2. 在 `entities/bullet.py` 的 `draw()` 方法新增外觀邏輯
3. 在 `systems/shop.py` 新增商店購買項目
4. 更新 `SHOP_ITEMS` 字典以支援商店界面

### 新增太空船類型

1. 在 `config.py` 的 `SPACESHIP_STATS` 新增屬性配置
2. 在 `entities/player.py` 的 `draw()` 和 `special_attack()` 新增實現
3. 在 `systems/shop.py` 新增購買邏輯
4. 確保 `update_ship_stats()` 正確同步屬性

### 新增遊戲系統

1. 在 `systems/` 目錄建立新模組
2. 在 `systems/__init__.py` 註冊新系統
3. 在 `GameController.__init__()` 初始化系統實例
4. 在主迴圈中適當位置調用系統方法

### 效能考量

- 使用配置字典而非硬編碼常數，支援熱重載和動態調整
- 物件池模式：考慮預分配子彈和敵人物件，避免頻繁記憶體分配
- 分離渲染和邏輯更新，`render()` 只負責繪製，`update_game_objects()` 負責邏輯

## 除錯指引

### 常見問題

- **物件消失**: 檢查 `is_off_screen()` 邊界判斷和 `entities/` 中的 `move()` 方法
- **碰撞失效**: 確認 `systems/collision.py` 的 AABB 算法和物件座標計算
- **商店無法開啟**: 檢查 `stars >= SHOP_UNLOCK_STARS` 條件和事件處理邏輯
- **配置不生效**: 確認 `config.py` 的字典結構和物件初始化時的載入邏輯

### 測試建議

- 使用 `python main.py` 直接執行測試
- 修改 `config.py` 中的常數快速測試（如 `SHOP_UNLOCK_STARS = 5`）
- 調整 `ENEMY_SPAWN_DELAY` 測試敵人生成頻率
- 在 `GameController.__init__()` 設定 `stars = 100` 快速測試商店功能

### 模組化除錯

- **遊戲邏輯**: 在 `GameController` 的各個方法中加入 `print()` 語句追蹤狀態變化
- **系統功能**: 分別測試 `UISystem`, `ShopSystem`, `collision` 模組的獨立功能
- **物件行為**: 在 `entities/` 中各類別的關鍵方法加入除錯資訊
