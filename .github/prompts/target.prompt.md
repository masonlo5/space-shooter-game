---
mode: agent
---

# Space Shooter 遊戲開發專案

## 📋 專案規格

- **開發語言**: Python + Pygame
- **視覺風格**: 幾何圖形（不使用圖片資源）
- **程式碼規範**: 遵循「程式碼開發風格指南」
- **檔案註解**: 除 README.md 外，其他檔案無需註解

## 🎯 開發指引

- 可先嘗試實作功能，完成後移除測試程式碼
- 使用幾何圖形代替圖片素材
- 遵循專案程式碼風格規範

## ---nt

- this is a game project which use python and pygame to create
- 請符合“程式碼開發風格指南”
- this game's name is call "space shooter"
- no need to use the pictures just use the geometry shapes to represent the game objects
- please use the following game design document to create the game
- funtcion can be try and when its done just delete the things that belong to trying the function
- expect README.md other files do not need to have comments

# above is the game's content

## 🎮 遊戲概述

**《Galaxy Blaster》**

### 核心玩法

- 玩家操作太空船在太空中與敵人戰鬥
- 射擊雷射攻擊外星敵人與敵方太空船
- 擊中普通敵人獲得 1 顆星星
- 集滿 **40 顆星星** 可解鎖商店功能：
  - 購買武器或太空船
  - 解鎖新太空船（每 40 顆星星解鎖 1 艘，最多 5 艘）

---

## 🛸 太空船系統

### 基本規格

- **總數**: 5 種不同太空船
- **特色**: 每艘太空船具備獨特功能與特殊攻擊（大招）

### 解鎖條件

- 需通過特定關卡後才能切換太空船

### 特殊攻擊系統

- 每艘太空船都有專屬大招，效果各異
- 支援裝備不同大招（裝備欄設計）

---

## 🔫 武器系統

### 操作方式

- 按下 **空白鍵（Space）** 即可切換武器

### 武器特性

- 每種武器射出不同類型的彈藥
- 武器價格與傷害成正比（越貴越強）
- 所有武器均可在商店購買

---

## 🛍️ 商店系統

### 可購買物品

#### 💰 裝備類

- **武器**: 各種威力不同的射擊武器
- **太空船**: 每 40 顆星星可解鎖新艘

#### 🧪 藥水道具

- **回血藥水 (Health Potion)**: 恢復生命值
- **加速藥水 (Speed Potion)**: 提升移動速度
- **防護藥水 (Protect Potion)**: 增強防禦能力

---

## 👾 敵人與 BOSS

### 普通敵人

- **行為**: 漂浮於太空中的敵對單位
- **獎勵**: 擊殺後獲得 1 顆星星

### Boss 太空船

- **特徵**: 擁有高生命值與強力攻擊能力
- **勝利演出**:
  - 擊敗後播放煙火動畫
  - 畫面顯示「**Success**」文字

---

## 💣 掉落物品與死亡機制

### 掉落物品系統

#### 觸發條件

- 擊殺特定敵人
- 隨機機率掉落
- 通關獎勵

#### 掉落物品類型

- **星星**: 遊戲貨幣
- **藥水**: 各種增益效果
- **升級零件**: 武器強化材料

### 死亡條件

- 被敵人擊敗
- 碰觸隨機掉落的炸彈（Bomb）

---

## 💡 其他功能

### UI 介面顯示

- **資源顯示**: 星星數量統計
- **裝備資訊**: 當前武器 & 太空船狀態
- **生命系統**: 血量條 & 藥水剩餘數量

### 進階功能 (可選)

- **任務系統**: 完成特定條件獲得獎勵
- **難度調整**: 敵人強度與速度隨關卡提升
