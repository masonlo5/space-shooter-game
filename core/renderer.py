######################載入套件######################
import pygame
from config import (
    BLACK, WHITE, RED, GREEN, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_SIZES, create_font, BOSS_TRIGGER_KILLS,
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_BOSS_FIGHT,
    GAME_STATE_VICTORY, GAME_STATE_GAME_OVER, GAME_STATE_SHIP_BATTLE,
    GAME_STATE_HIDE_SEEK
)

######################渲染管理器######################
class Renderer:
    """
    渲染管理系統 - 負責協調所有遊戲畫面的繪製\n
    \n
    負責處理:\n
    1. 不同遊戲狀態的畫面渲染\n
    2. 遊戲物件的統一繪製管理\n
    3. UI 元素的渲染協調\n
    4. 特效和覆蓋層的處理\n
    """
    
    def __init__(self, screen):
        """
        初始化渲染管理器\n
        \n
        參數:\n
        screen (pygame.Surface): 遊戲畫面物件\n
        """
        self.screen = screen
    
    def render_frame(self, state_manager, systems, game_objects):
        """
        渲染一幀畫面\n
        \n
        參數:\n
        state_manager (StateManager): 狀態管理器\n
        systems (dict): 遊戲系統字典\n
        game_objects (dict): 遊戲物件字典\n
        """
        game_state = state_manager.get_game_state()
        
        if game_state == GAME_STATE_MENU:
            self._render_menu(systems)
        
        elif game_state == GAME_STATE_SHIP_BATTLE:
            self._render_ship_battle(systems)
        
        elif game_state == GAME_STATE_HIDE_SEEK:
            self._render_hide_seek(systems)
        
        else:
            self._render_main_game(state_manager, systems, game_objects)
        
        # 更新畫面
        pygame.display.flip()
    
    def _render_menu(self, systems):
        """
        渲染主畫面\n
        """
        systems['menu'].draw_menu(self.screen)
    
    def _render_ship_battle(self, systems):
        """
        渲染 Ship Battle 模式\n
        """
        # 繪製戰鬥物件
        systems['ship_battle'].draw_battle_objects(self.screen)
        
        # 繪製 Ship Battle UI
        battle_info = systems['ship_battle'].get_battle_info()
        systems['ui'].draw_ship_battle_ui(self.screen, battle_info)
        
        # 繪製視覺效果（雪花或烏鴉）
        systems['visual_effects'].draw(self.screen)
    
    def _render_hide_seek(self, systems):
        """
        渲染躲貓貓遊戲\n
        """
        if systems.get('hide_seek'):
            systems['hide_seek'].draw(self.screen)
    
    def _render_main_game(self, state_manager, systems, game_objects):
        """
        渲染主要遊戲畫面\n
        """
        # 清空螢幕（填滿黑色）
        self.screen.fill(BLACK)
        
        game_state = state_manager.get_game_state()
        shop_open = state_manager.shop_open
        
        # 繪製遊戲物件（只有在商店關閉時）
        if not shop_open:
            self._render_game_objects(game_objects)
        
        # 繪製 UI 介面
        state_dict = state_manager.get_state_dict()
        systems['ui'].draw_ui(
            self.screen, 
            game_objects.get('player'), 
            state_dict['score'], 
            state_dict['stars']
        )
        
        # 顯示敵人擊殺計數和Boss觸發進度
        if game_state == GAME_STATE_PLAYING:
            self._render_boss_progress(state_manager)
        
        # 繪製煙火效果
        if game_objects.get('fireworks'):
            for firework in game_objects['fireworks']:
                firework.draw(self.screen)
        
        # 如果 Boss 被擊敗，顯示勝利訊息
        if state_manager.boss_killed and state_manager.victory_timer > 0:
            systems['ui'].draw_victory_message(self.screen, state_manager.victory_timer)
        
        # 如果商店開啟，繪製商店介面
        if shop_open:
            systems['shop'].draw_shop(self.screen, state_manager.stars)
        
        # 遊戲結束畫面
        if game_state == GAME_STATE_GAME_OVER:
            self._draw_game_over_screen(state_manager)
        
        # 勝利畫面
        elif game_state == GAME_STATE_VICTORY:
            self._draw_victory_screen(state_manager)
    
    def _render_game_objects(self, game_objects):
        """
        渲染遊戲物件\n
        """
        # 繪製玩家
        if game_objects.get('player'):
            game_objects['player'].draw(self.screen)
        
        # 繪製所有子彈
        if game_objects.get('bullets'):
            for bullet in game_objects['bullets']:
                bullet.draw(self.screen)
        
        # 繪製Boss子彈
        if game_objects.get('boss_bullets'):
            for boss_bullet in game_objects['boss_bullets']:
                boss_bullet.draw(self.screen)
        
        # 繪製所有敵人
        if game_objects.get('enemies'):
            for enemy in game_objects['enemies']:
                enemy.draw(self.screen)
        
        # 繪製Boss
        if game_objects.get('boss'):
            game_objects['boss'].draw(self.screen)
            # 繪製Boss血量條
            game_objects['boss'].draw_health_bar(self.screen)
        
        # 繪製所有道具
        if game_objects.get('powerups'):
            for powerup in game_objects['powerups']:
                powerup.draw(self.screen)
    
    def _render_boss_progress(self, state_manager):
        """
        渲染 Boss 出現進度\n
        """
        progress_info = state_manager.get_boss_progress()
        progress_font = create_font(FONT_SIZES["normal"])
        
        if progress_info['remaining'] > 0:
            progress_text = progress_font.render(
                f"Boss 出現倒數: {progress_info['remaining']} 敵人", 
                True, YELLOW
            )
            self.screen.blit(progress_text, (SCREEN_WIDTH - 200, 40))
        else:
            boss_ready_text = progress_font.render("Boss 即將出現！", True, RED)
            self.screen.blit(boss_ready_text, (SCREEN_WIDTH - 200, 40))
    
    def _draw_game_over_screen(self, state_manager):
        """
        繪製遊戲結束畫面\n
        """
        # 半透明黑色覆蓋
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 字體
        font_large = create_font(FONT_SIZES["extra_large"])
        font_medium = create_font(FONT_SIZES["medium"])
        font_small = create_font(FONT_SIZES["normal"])
        
        # 遊戲結束文字
        game_over_text = font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最終分數
        score_text = font_medium.render(f"最終分數: {state_manager.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        stars_text = font_medium.render(f"星星數量: {state_manager.stars}", True, YELLOW)
        stars_rect = stars_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(stars_text, stars_rect)
        
        killed_text = font_medium.render(f"擊敗敵人: {state_manager.enemies_killed}", True, GREEN)
        killed_rect = killed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(killed_text, killed_rect)
        
        # 操作提示
        restart_text = font_small.render("按 R 重新開始 | 按 Enter 返回主畫面", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)
    
    def _draw_victory_screen(self, state_manager):
        """
        繪製勝利畫面\n
        """
        # 半透明金色覆蓋
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((40, 40, 0))  # 深金色
        self.screen.blit(overlay, (0, 0))
        
        # 字體
        font_large = create_font(FONT_SIZES["extra_large"])
        font_medium = create_font(FONT_SIZES["medium"])
        font_small = create_font(FONT_SIZES["normal"])
        
        # 勝利文字
        victory_text = font_large.render("VICTORY!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(victory_text, victory_rect)
        
        boss_text = font_medium.render("Boss 已被擊敗！", True, WHITE)
        boss_rect = boss_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(boss_text, boss_rect)
        
        # 最終分數
        score_text = font_medium.render(f"最終分數: {state_manager.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        stars_text = font_medium.render(f"星星數量: {state_manager.stars}", True, YELLOW)
        stars_rect = stars_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(stars_text, stars_rect)
        
        # 操作提示
        continue_text = font_small.render("按 Enter 返回主畫面 | 按 R 重新開始", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(continue_text, continue_rect)