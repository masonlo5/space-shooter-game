# Galaxy Blaster - AI 程式設計助理指南

## 專案架構概覽

這是一個使用 Python + Pygame 開發的太空射擊遊戲，採用物件導向設計，所有代碼集中在 `main.py` 中。遊戲包含完整的戰鬥系統、商店機制、多種太空船和武器類型。

## 核心物件系統

- **Player**: 玩家太空船，負責移動、射擊、武器切換、特殊攻擊
- **Bullet**: 子彈系統，支援 5 種武器類型（basic/laser/plasma/missile/ion_cannon）
- **Enemy**: 敵人系統，包含 3 種類型（basic/fast/boss），每種有不同移動模式
- **PowerUp**: 道具系統，5 種掉落物（star/health_potion/speed_potion/protect_potion/bomb）
- **Firework**: 粒子效果系統，Boss 擊敗後的慶祝動畫

## 程式碼風格約定

### 必須遵循的規範

1. **使用 #todos 工具規劃後才能開始撰寫程式碼**
2. **變數命名**: 統一使用 snake_case（如 `bg_x`, `ball_radius`）
3. **類別命名**: 使用 PascalCase（如 `Player`, `Enemy`）
4. **註解語言**: 統一使用繁體中文
5. **區塊分隔**: 使用 `######################` 標記區塊
6. **文檔字串**: 使用 `"""` 三引號，包含功能描述、參數說明、回傳值

### 註解撰寫原則

- 用白話文解釋複雜邏輯，避免技術術語
- 數值計算用日常用語說明原因：`# 算出球打到底板的哪個位置（-1 是最左邊，1 是最右邊）`
- 條件判斷用「如果...就...」格式：`# 如果圖片檔案壞了或找不到，就畫一個簡單的圓形代替`

## 遊戲機制關鍵點

### 武器升級系統

- 武器透過 `current_weapon` 屬性切換，影響 Bullet 的 `damage` 和外觀
- 商店購買解鎖新武器，存於 `unlocked_weapons` 清單
- 特殊攻擊 `special_attack()` 根據太空船類型產生不同子彈模式

### 星星經濟系統

- 全域變數 `stars` 作為遊戲貨幣
- 擊敗敵人 +1 星星，Boss +20 星星
- 商店需要 40 顆星星才能開啟（`stars >= 40`）

### 碰撞檢測模式

使用 AABB 檢測：`check_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height)`

### 狀態管理

- `shop_open` 布林值控制商店顯示/遊戲暫停
- `boss_killed` + `victory_timer` 處理勝利條件
- 使用 `pygame.key.get_pressed()` 處理持續按鍵（移動、射擊）
- 使用 `pygame.KEYDOWN` 事件處理單次按鍵（切換武器、開啟商店）

## 開發工作流程

### 新增武器類型

1. 在 `Bullet.__init__()` 新增武器配置（damage, color, size）
2. 在 `Bullet.draw()` 新增對應外觀
3. 在 `draw_shop()` 和 `handle_shop_purchase()` 新增商店項目

### 新增敵人類型

1. 在 `Enemy.__init__()` 設定屬性（width, height, health, speed, color）
2. 在 `Enemy.move()` 實作移動模式
3. 在 `Enemy.draw()` 設計外觀
4. 修改主程式的敵人生成邏輯

### 效能考量

- 使用 `list[:]` 切片複製清單進行安全遍歷：`for bullet in bullets[:]:`
- 及時移除離開螢幕的物件避免記憶體累積
- 冷卻時間機制防止子彈發射過於頻繁

## 除錯指引

### 常見問題

- **物件消失**: 檢查 `is_off_screen()` 邊界判斷
- **碰撞失效**: 確認物件座標和尺寸計算正確
- **商店無法開啟**: 檢查 `stars >= 40` 條件

### 測試建議

- 使用 `python main.py` 直接執行測試
- 修改 `stars = 100` 快速測試商店功能
- 調整 `enemy_spawn_delay` 測試敵人生成頻率
