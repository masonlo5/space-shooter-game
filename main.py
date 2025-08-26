######################載入套件######################
import pygame
import sys
import random

# 匯入遊戲設定
from config import *

# 匯入遊戲物件
from entities import Player, Enemy, Bullet, PowerUp, Firework

# 匯入遊戲系統
from systems import check_collision, UISystem, ShopSystem

######################全域變數######################
score = 0
stars = 0
boss_killed = False
victory_timer = 0

######################遊戲主控制類別######################
class GameController:
    """
    遊戲主控制器 - 負責管理整個遊戲的流程和狀態\n
    \n
    負責處理:\n
    1. 遊戲初始化\n
    2. 主遊戲迴圈\n
    3. 事件處理\n
    4. 遊戲物件管理\n
    5. 碰撞檢測協調\n
    """
    
    def __init__(self):
        """
        初始化遊戲控制器\n
        """
        # 初始化 Pygame
        pygame.init()
        
        # 建立遊戲視窗
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Galaxy Blaster - Space Shooter")
        
        # 設定遊戲時鐘
        self.clock = pygame.time.Clock()
        
        # 初始化遊戲系統
        self.ui_system = UISystem()
        self.shop_system = ShopSystem()
        
        # 初始化遊戲物件
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.fireworks = []
        
        # 遊戲狀態
        self.shop_open = False
        self.enemy_spawn_timer = 0
        self.running = True
        
        # 全域變數
        global score, stars, boss_killed, victory_timer
        score = 0
        stars = 0
        boss_killed = False
        victory_timer = 0
    
    def handle_events(self):
        """
        處理遊戲事件\n
        """
        global stars
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.shop_open:
                    # 商店開啟時的按鍵處理
                    if event.key == pygame.K_ESCAPE:
                        self.shop_open = False
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                     pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                        stars = self.shop_system.handle_purchase(event.key, self.player, stars)
                else:
                    # 遊戲中的按鍵處理
                    if event.key == pygame.K_SPACE:
                        # 按下空白鍵切換武器
                        self.player.change_weapon()
                    elif event.key == pygame.K_s and stars >= SHOP_UNLOCK_STARS:
                        # 按下 S 鍵開啟商店（需要 40 顆星星）
                        self.shop_open = True
                    elif event.key == pygame.K_c:
                        # 按下 C 鍵切換太空船
                        self.player.change_spaceship()
                    elif event.key == pygame.K_x:
                        # 按下 X 鍵發動特殊攻擊
                        special_bullets = self.player.special_attack()
                        self.bullets.extend(special_bullets)
    
    def update_game_objects(self):
        """
        更新所有遊戲物件的狀態\n
        """
        global score, stars, boss_killed, victory_timer
        
        # 取得按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 只有在商店關閉時才更新遊戲邏輯
        if not self.shop_open:
            # 更新玩家
            self.player.move(keys)
            self.player.update()
            
            # 射擊控制（按住 Ctrl 或 Shift 鍵射擊）
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                new_bullet = self.player.shoot()
                if new_bullet:
                    self.bullets.append(new_bullet)
            
            # 更新所有子彈
            for bullet in self.bullets[:]:  # 用切片複製清單，避免修改時出錯
                bullet.move()
                # 移除飛出螢幕的子彈
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)
            
            # 敵人生成邏輯
            self.spawn_enemies()
            
            # 更新所有敵人
            for enemy in self.enemies[:]:
                enemy.move()
                # 移除離開螢幕的敵人
                if enemy.is_off_screen():
                    self.enemies.remove(enemy)
            
            # 碰撞檢測
            self.handle_collisions()
            
            # 更新所有道具
            for powerup in self.powerups[:]:
                powerup.move()
                # 移除離開螢幕的道具
                if powerup.is_off_screen():
                    self.powerups.remove(powerup)
            
            # 碰撞檢測：玩家撿到道具
            for powerup in self.powerups[:]:
                if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                                 powerup.x, powerup.y, powerup.width, powerup.height):
                    # 套用道具效果
                    is_fatal, stars_gained = powerup.apply_effect(self.player)
                    stars += stars_gained
                    if is_fatal:
                        print(f"踩到炸彈！遊戲結束！最終分數：{score}，星星數量：{stars}")
                        self.running = False
                    self.powerups.remove(powerup)
        
        # 更新煙火效果
        for firework in self.fireworks[:]:
            firework.update()
            if firework.is_dead():
                self.fireworks.remove(firework)
        
        # 勝利條件檢查
        if boss_killed:
            victory_timer -= 1
            if victory_timer <= 0:
                print(f"Victory! Boss 擊敗！最終分數：{score}，星星數量：{stars}")
                self.running = False
    
    def spawn_enemies(self):
        """
        生成敵人的邏輯\n
        """
        global score
        
        self.enemy_spawn_timer += 1
        enemy_spawn_delay = ENEMY_SPAWN_DELAY
        
        if self.enemy_spawn_timer >= enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            # 隨機選擇敵人類型和位置
            enemy_type = random.choice(["basic", "basic", "fast"])  # 增加基本敵人的比例
            enemy_x = random.randint(0, SCREEN_WIDTH - 30)
            self.enemies.append(Enemy(enemy_x, -30, enemy_type))
            
            # 隨著分數增加，敵人生成速度加快
            if score > 100:
                enemy_spawn_delay = max(30, 60 - score // 50)  # 最快每 0.5 秒生成一個
        
        # 隨機生成 Boss（機率較低，但隨分數提高）
        boss_chance = BOSS_SPAWN_BASE_CHANCE - (score // 10)  # 分數越高，Boss 出現機率越大
        if random.randint(1, max(300, boss_chance)) == 1:
            boss_x = random.randint(0, SCREEN_WIDTH - 80)
            self.enemies.append(Enemy(boss_x, -60, "boss"))
    
    def handle_collisions(self):
        """
        處理所有碰撞檢測\n
        """
        global score, stars, boss_killed, victory_timer
        
        # 碰撞檢測：子彈打中敵人
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 enemy.x, enemy.y, enemy.width, enemy.height):
                    # 子彈打中敵人
                    if enemy.take_damage(bullet.damage):
                        # 檢查是否為 Boss
                        if enemy.enemy_type == "boss":
                            # Boss 被擊敗，觸發勝利條件
                            boss_killed = True
                            victory_timer = 180  # 3 秒勝利畫面
                            
                            # 生成慶祝煙火
                            for _ in range(5):
                                firework_x = random.randint(100, SCREEN_WIDTH - 100)
                                firework_y = random.randint(100, SCREEN_HEIGHT - 100)
                                self.fireworks.append(Firework(firework_x, firework_y))
                        
                        # 敵人死亡，隨機掉落道具
                        self.drop_powerups(enemy)
                        
                        self.enemies.remove(enemy)
                        score += enemy.score_value
                        stars += enemy.star_value
                    self.bullets.remove(bullet)
                    break  # 子彈打中一個敵人後就消失
        
        # 碰撞檢測：玩家撞到敵人
        for enemy in self.enemies[:]:
            if check_collision(self.player.x, self.player.y, self.player.width, self.player.height,
                             enemy.x, enemy.y, enemy.width, enemy.height):
                # 玩家撞到敵人，減少生命值
                self.player.health -= 20
                self.enemies.remove(enemy)
                
                # 檢查遊戲是否結束
                if self.player.health <= 0:
                    print(f"遊戲結束！最終分數：{score}，星星數量：{stars}")
                    self.running = False
    
    def drop_powerups(self, enemy):
        """
        敵人死亡時掉落道具的邏輯\n
        \n
        參數:\n
        enemy (Enemy): 死亡的敵人物件\n
        """
        drop_chance = random.randint(1, 100)
        if drop_chance <= POWERUP_DROP_CHANCE:  # 30% 機率掉落道具
            if drop_chance <= STAR_DROP_CHANCE:  # 15% 機率掉星星
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "star"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE:  # 5% 機率掉回血藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "health_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE:  # 5% 機率掉加速藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "speed_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE + PROTECT_POTION_CHANCE:  # 3% 機率掉防護藥水
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "protect_potion"))
            else:  # 2% 機率掉炸彈
                self.powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "bomb"))
    
    def render(self):
        """
        繪製所有遊戲畫面\n
        """
        global victory_timer
        
        # 清空螢幕（填滿黑色）
        self.screen.fill(BLACK)
        
        # 繪製遊戲物件（只有在商店關閉時）
        if not self.shop_open:
            self.player.draw(self.screen)
            
            # 繪製所有子彈
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            # 繪製所有敵人
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # 繪製所有道具
            for powerup in self.powerups:
                powerup.draw(self.screen)
        
        # 繪製 UI 介面
        self.ui_system.draw_ui(self.screen, self.player, score, stars)
        
        # 繪製煙火效果
        for firework in self.fireworks:
            firework.draw(self.screen)
        
        # 如果 Boss 被擊敗，顯示勝利訊息
        if boss_killed:
            self.ui_system.draw_victory_message(self.screen, victory_timer)
        
        # 如果商店開啟，繪製商店介面
        if self.shop_open:
            self.shop_system.draw_shop(self.screen, stars)
        
        # 更新畫面
        pygame.display.flip()
    
    def run(self):
        """
        執行主遊戲迴圈\n
        """
        while self.running:
            # 處理事件
            self.handle_events()
            
            # 更新遊戲狀態
            self.update_game_objects()
            
            # 繪製畫面
            self.render()
            
            # 控制遊戲幀率
            self.clock.tick(FPS)
        
        # 關閉遊戲
        pygame.quit()
        sys.exit()

######################主程式函數######################
def main():
    """
    遊戲主程式 - 建立並執行遊戲控制器\n
    """
    game = GameController()
    game.run()

# 啟動遊戲
if __name__ == "__main__":
    main()