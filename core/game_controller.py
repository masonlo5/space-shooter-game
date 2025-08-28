######################載入套件######################
import pygame
import sys
import random

# 匯入遊戲設定
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK,
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT,
    GAME_STATE_SHIP_BATTLE, GAME_STATE_HIDE_SEEK, GAME_STATE_GAME_OVER,
    ENEMY_SPAWN_DELAY, POWERUP_DROP_CHANCE, STAR_DROP_CHANCE,
    HEALTH_POTION_CHANCE, SPEED_POTION_CHANCE, PROTECT_POTION_CHANCE,
    SHOP_UNLOCK_STARS
)

# 匯入遊戲物件
from entities import Player, Enemy, Boss, Bullet, PowerUp, Firework

# 匯入遊戲系統
from systems import check_collision, UISystem, ShopSystem, MenuSystem, ShipBattleSystem, VisualEffectsSystem, HideSeekSystem

# 匯入核心系統
from .event_manager import EventManager
from .state_manager import StateManager
from .renderer import Renderer

######################重構後的遊戲控制器######################
class GameController:
    """
    重構後的遊戲主控制器 - 負責協調所有核心系統\n
    \n
    負責處理:\n
    1. 系統初始化和協調\n
    2. 主遊戲迴圈管理\n
    3. 遊戲物件生命週期管理\n
    4. 系統間通信協調\n
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
        
        # 初始化核心系統
        self.event_manager = EventManager()
        self.state_manager = StateManager()
        self.renderer = Renderer(self.screen)
        
        # 初始化遊戲系統
        self.systems = {
            'ui': UISystem(),
            'shop': ShopSystem(),
            'menu': MenuSystem(),
            'ship_battle': ShipBattleSystem(),
            'visual_effects': VisualEffectsSystem(),
            'hide_seek': None  # 躲貓貓系統（按需創建）
        }
        
        # 主迴圈控制
        self.running = True
        
        # 初始化遊戲物件
        self.reset_game_objects()
        
        # 其他控制變數
        self.enemy_spawn_timer = 0
    
    def reset_game_objects(self):
        """
        重置所有遊戲物件\n
        """
        self.game_objects = {
            'player': Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80),
            'bullets': [],
            'enemies': [],
            'powerups': [],
            'fireworks': [],
            'boss': None,
            'boss_bullets': []
        }
        
        # 重置計時器
        self.enemy_spawn_timer = 0
    
    def start_ship_battle(self):
        """
        開始 Ship Battle 模式\n
        """
        print("開始 Ship Battle 模式")
        
        # 建立玩家物件
        player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 80)
        player_name = self.systems['menu'].get_player_name()
        
        # 開始戰鬥
        self.systems['ship_battle'].start_battle(player, player_name)
        
        # 切換到 Ship Battle 狀態
        self.state_manager.set_game_state(GAME_STATE_SHIP_BATTLE)
    
    def start_hide_seek(self):
        """
        開始躲貓貓遊戲\n
        """
        print("開始躲貓貓遊戲")
        
        # 創建躲貓貓遊戲系統
        player_name = self.systems['menu'].get_player_name()
        self.systems['hide_seek'] = HideSeekSystem(player_name)
        
        # 切換到躲貓貓狀態
        self.state_manager.set_game_state(GAME_STATE_HIDE_SEEK)
    
    def handle_events(self):
        """
        處理遊戲事件\n
        """
        events_result = self.event_manager.handle_events(
            self.state_manager.get_game_state(),
            self.systems,
            self.game_objects.get('player'),
            self.state_manager.shop_open
        )
        
        # 處理事件結果
        if not events_result['running']:
            self.running = False
        
        if events_result['state_change']:
            self.state_manager.set_game_state(events_result['state_change'])
            
            if events_result['state_change'] == GAME_STATE_SHIP_BATTLE:
                self.start_ship_battle()
            elif events_result['state_change'] == GAME_STATE_HIDE_SEEK:
                self.start_hide_seek()
        
        if events_result['reset_required']:
            self.reset_game_objects()
            self.state_manager.reset_game_state()
        
        if events_result['shop_toggle'] is not None:
            self.state_manager.toggle_shop(events_result['shop_toggle'])
        
        if events_result['shop_request'] and self.state_manager.can_open_shop():
            self.state_manager.toggle_shop(True)
        
        if events_result['purchase_key']:
            old_stars = self.state_manager.stars
            new_stars = self.systems['shop'].handle_purchase(
                events_result['purchase_key'], 
                self.game_objects['player'], 
                old_stars
            )
            self.state_manager.stars = new_stars
        
        if events_result['special_bullets']:
            self.game_objects['bullets'].extend(events_result['special_bullets'])
    
    def update_game_objects(self):
        """
        更新所有遊戲物件的狀態\n
        """
        game_state = self.state_manager.get_game_state()
        
        # Ship Battle 模式的更新邏輯
        if game_state == GAME_STATE_SHIP_BATTLE:
            self._update_ship_battle()
            return
        
        # 躲貓貓模式的更新邏輯
        if game_state == GAME_STATE_HIDE_SEEK:
            self._update_hide_seek()
            return
        
        # 只有在一般遊戲狀態才更新遊戲邏輯
        if game_state not in [GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT]:
            return
        
        # 只有在商店關閉時才更新遊戲邏輯
        if not self.state_manager.shop_open:
            self._update_main_game()
    
    def _update_ship_battle(self):
        """
        更新 Ship Battle 模式\n
        """
        keys = pygame.key.get_pressed()
        battle_result = self.systems['ship_battle'].update(keys)
        
        # 更新視覺效果
        self.systems['visual_effects'].update()
        
        if battle_result == "victory":
            print("Ship Battle 玩家獲勝！")
            self.systems['visual_effects'].start_victory_effect()
        elif battle_result == "defeat":
            print("Ship Battle 玩家失敗！")
            self.systems['visual_effects'].start_defeat_effect()
        elif battle_result in ["end", "quit"]:
            print("Ship Battle 結束，返回主選單")
            self.systems['visual_effects'].stop_effects()
            self.systems['ship_battle'].reset()
            self.state_manager.set_game_state(GAME_STATE_MENU)
    
    def _update_hide_seek(self):
        """
        更新躲貓貓模式\n
        """
        if self.systems.get('hide_seek'):
            keys = pygame.key.get_pressed()
            result = self.systems['hide_seek'].update(keys)
            
            if result == "return_to_menu":
                print("躲貓貓遊戲結束，返回主選單")
                self.systems['hide_seek'] = None
                self.state_manager.set_game_state(GAME_STATE_MENU)
    
    def _update_main_game(self):
        """
        更新主要遊戲邏輯\n
        """
        game_state = self.state_manager.get_game_state()
        
        # 取得按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 更新玩家
        self.game_objects['player'].move(keys)
        self.game_objects['player'].update()
        
        # 射擊控制（按住 Ctrl 或 Shift 鍵射擊）
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] or keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            new_bullet = self.game_objects['player'].shoot()
            if new_bullet:
                self.game_objects['bullets'].append(new_bullet)
        
        # 更新所有子彈
        for bullet in self.game_objects['bullets'][:]:
            bullet.move()
            if bullet.is_off_screen():
                self.game_objects['bullets'].remove(bullet)
        
        # 更新Boss子彈
        for boss_bullet in self.game_objects['boss_bullets'][:]:
            boss_bullet.move()
            if boss_bullet.is_off_screen():
                self.game_objects['boss_bullets'].remove(boss_bullet)
        
        # 根據遊戲狀態更新敵人或Boss
        if game_state == GAME_STATE_PLAYING:
            self._update_enemies()
            # 檢查是否達到Boss戰條件
            if self.state_manager.should_trigger_boss() and not self.game_objects['boss']:
                self._trigger_boss_fight()
        
        elif game_state == GAME_STATE_BOSS_FIGHT:
            self._update_boss()
        
        # 碰撞檢測
        self._handle_collisions()
        
        # 更新道具
        self._update_powerups()
        
        # 更新煙火效果
        self._update_fireworks()
        
        # 勝利條件檢查
        if self.state_manager.boss_killed:
            if self.state_manager.update_victory_timer():
                print(f"Victory! Boss 擊敗！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
    
    def _update_enemies(self):
        """
        更新敵人生成和移動\n
        """
        # 生成敵人
        self.enemy_spawn_timer += 1
        enemy_spawn_delay = ENEMY_SPAWN_DELAY
        
        if self.enemy_spawn_timer >= enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            enemy_type = random.choice(["basic", "basic", "fast"])
            enemy_x = random.randint(0, SCREEN_WIDTH - 30)
            self.game_objects['enemies'].append(Enemy(enemy_x, -30, enemy_type))
            
            # 隨著分數增加，敵人生成速度加快
            if self.state_manager.score > 100:
                enemy_spawn_delay = max(30, 60 - self.state_manager.score // 50)
        
        # 更新敵人位置
        for enemy in self.game_objects['enemies'][:]:
            enemy.move()
            if enemy.is_off_screen():
                self.game_objects['enemies'].remove(enemy)
    
    def _trigger_boss_fight(self):
        """
        觸發Boss戰\n
        """
        print(f"Boss 出現！已擊敗 {self.state_manager.enemies_killed} 個敵人")
        
        # 清除所有現有敵人
        self.game_objects['enemies'].clear()
        
        # 創建Boss
        boss_x = SCREEN_WIDTH // 2 - 40
        boss_y = 50
        self.game_objects['boss'] = Boss(boss_x, boss_y)
        
        # 切換到Boss戰狀態
        self.state_manager.set_game_state(GAME_STATE_BOSS_FIGHT)
    
    def _update_boss(self):
        """
        更新Boss狀態\n
        """
        if self.game_objects['boss']:
            # 移動Boss
            self.game_objects['boss'].move()
            
            # 更新Boss並獲取新產生的子彈
            new_boss_bullets = self.game_objects['boss'].update()
            self.game_objects['boss_bullets'].extend(new_boss_bullets)
    
    def _handle_collisions(self):
        """
        處理所有碰撞檢測\n
        """
        # 這裡包含原有的所有碰撞檢測邏輯
        # 但使用 state_manager 來更新狀態
        self._handle_bullet_enemy_collision()
        self._handle_bullet_boss_collision()
        self._handle_boss_bullet_player_collision()
        self._handle_player_enemy_collision()
        self._handle_player_boss_collision()
        self._handle_player_powerup_collision()
    
    def _handle_bullet_enemy_collision(self):
        """處理子彈打中敵人的碰撞"""
        for bullet in self.game_objects['bullets'][:]:
            for enemy in self.game_objects['enemies'][:]:
                if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                                 enemy.x, enemy.y, enemy.width, enemy.height):
                    if enemy.take_damage(bullet.damage):
                        self._drop_powerups(enemy)
                        self.game_objects['enemies'].remove(enemy)
                        self.state_manager.update_score(enemy.score_value)
                        self.state_manager.update_stars(enemy.star_value)
                        self.state_manager.update_enemies_killed(1)
                    
                    self.game_objects['bullets'].remove(bullet)
                    break
    
    def _handle_bullet_boss_collision(self):
        """處理子彈打中Boss的碰撞"""
        if not self.game_objects['boss']:
            return
            
        for bullet in self.game_objects['bullets'][:]:
            if check_collision(bullet.x, bullet.y, bullet.width, bullet.height,
                             self.game_objects['boss'].x, self.game_objects['boss'].y, 
                             self.game_objects['boss'].width, self.game_objects['boss'].height):
                if self.game_objects['boss'].take_damage(bullet.damage):
                    # Boss被擊敗
                    self.state_manager.set_boss_killed(180)
                    
                    # 生成Boss禮物
                    gift = self.game_objects['boss'].drop_gift()
                    self.game_objects['powerups'].append(gift)
                    
                    # 生成慶祝煙火
                    for _ in range(8):
                        firework_x = random.randint(100, SCREEN_WIDTH - 100)
                        firework_y = random.randint(100, SCREEN_HEIGHT - 100)
                        self.game_objects['fireworks'].append(Firework(firework_x, firework_y))
                    
                    # 獲得分數和星星
                    self.state_manager.update_score(self.game_objects['boss'].score_value)
                    self.state_manager.update_stars(self.game_objects['boss'].star_value)
                    
                    # 移除Boss
                    self.game_objects['boss'] = None
                    self.game_objects['boss_bullets'].clear()
                
                self.game_objects['bullets'].remove(bullet)
                break
    
    def _handle_boss_bullet_player_collision(self):
        """處理Boss子彈打中玩家的碰撞"""
        for boss_bullet in self.game_objects['boss_bullets'][:]:
            if check_collision(boss_bullet.x, boss_bullet.y, boss_bullet.width, boss_bullet.height,
                             self.game_objects['player'].x, self.game_objects['player'].y, 
                             self.game_objects['player'].width, self.game_objects['player'].height):
                self.game_objects['player'].health -= boss_bullet.damage
                self.game_objects['boss_bullets'].remove(boss_bullet)
                
                if self.game_objects['player'].health <= 0:
                    print(f"被Boss擊敗！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
                    self.state_manager.set_game_state(GAME_STATE_GAME_OVER)
    
    def _handle_player_enemy_collision(self):
        """處理玩家撞到敵人的碰撞"""
        for enemy in self.game_objects['enemies'][:]:
            if check_collision(self.game_objects['player'].x, self.game_objects['player'].y, 
                             self.game_objects['player'].width, self.game_objects['player'].height,
                             enemy.x, enemy.y, enemy.width, enemy.height):
                self.game_objects['player'].health -= 20
                self.game_objects['enemies'].remove(enemy)
                
                if self.game_objects['player'].health <= 0:
                    print(f"遊戲結束！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
                    self.state_manager.set_game_state(GAME_STATE_GAME_OVER)
    
    def _handle_player_boss_collision(self):
        """處理玩家撞到Boss的碰撞"""
        if not self.game_objects['boss']:
            return
            
        if check_collision(self.game_objects['player'].x, self.game_objects['player'].y, 
                         self.game_objects['player'].width, self.game_objects['player'].height,
                         self.game_objects['boss'].x, self.game_objects['boss'].y, 
                         self.game_objects['boss'].width, self.game_objects['boss'].height):
            self.game_objects['player'].health -= 50
            
            if self.game_objects['player'].health <= 0:
                print(f"撞到Boss！遊戲結束！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
                self.state_manager.set_game_state(GAME_STATE_GAME_OVER)
    
    def _handle_player_powerup_collision(self):
        """處理玩家撿到道具的碰撞"""
        for powerup in self.game_objects['powerups'][:]:
            if check_collision(self.game_objects['player'].x, self.game_objects['player'].y, 
                             self.game_objects['player'].width, self.game_objects['player'].height,
                             powerup.x, powerup.y, powerup.width, powerup.height):
                is_fatal, stars_gained, should_return_to_menu = powerup.apply_effect(self.game_objects['player'])
                self.state_manager.update_stars(stars_gained)
                
                if is_fatal:
                    print(f"踩到炸彈！遊戲結束！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
                    self.state_manager.set_game_state(GAME_STATE_GAME_OVER)
                elif should_return_to_menu:
                    print(f"獲得Boss禮物！最終分數：{self.state_manager.score}，星星數量：{self.state_manager.stars}")
                    self.state_manager.set_game_state(GAME_STATE_MENU)
                
                self.game_objects['powerups'].remove(powerup)
    
    def _drop_powerups(self, enemy):
        """敵人死亡時掉落道具的邏輯"""
        drop_chance = random.randint(1, 100)
        if drop_chance <= POWERUP_DROP_CHANCE:
            if drop_chance <= STAR_DROP_CHANCE:
                self.game_objects['powerups'].append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "star"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE:
                self.game_objects['powerups'].append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "health_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE:
                self.game_objects['powerups'].append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "speed_potion"))
            elif drop_chance <= STAR_DROP_CHANCE + HEALTH_POTION_CHANCE + SPEED_POTION_CHANCE + PROTECT_POTION_CHANCE:
                self.game_objects['powerups'].append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "protect_potion"))
            else:
                self.game_objects['powerups'].append(PowerUp(enemy.x + enemy.width // 2, enemy.y, "bomb"))
    
    def _update_powerups(self):
        """更新道具狀態"""
        for powerup in self.game_objects['powerups'][:]:
            powerup.move()
            if powerup.is_off_screen():
                self.game_objects['powerups'].remove(powerup)
    
    def _update_fireworks(self):
        """更新煙火效果"""
        for firework in self.game_objects['fireworks'][:]:
            firework.update()
            if firework.is_dead():
                self.game_objects['fireworks'].remove(firework)
    
    def render(self):
        """
        渲染所有遊戲畫面\n
        """
        self.renderer.render_frame(self.state_manager, self.systems, self.game_objects)
    
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