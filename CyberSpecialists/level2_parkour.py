# -*- coding: utf-8 -*-
"""
Level 2: Horizontal Parkour - FIXED with bigger gaps, void death, restart message
"""

import pygame
import random
import asyncio
from constants import *
from player import Player
from obstacles import Coin, Platform
from ui import Camera, Timer, ScoreDisplay, QuizOverlay, draw_gradient_background
from questions_bank import get_randomized_questions
from main import pause_menu, pause_menu_async


class ParkourLevel:
    """Level 2: Horizontal parkour jumping across platforms - NO GROUND"""

    def __init__(self, level_num, difficulty, fonts, lang_manager):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager
        self.falling = False
        self.fall_timer = 0

        # Load coin collection sound
        try:
            self.coin_sound = pygame.mixer.Sound('coincollect.ogg')
            self.coin_sound.set_volume(0.5)
        except:
            self.coin_sound = None

        self.init_level()

    def init_level(self):
        """Initialize/reset the level"""
        # Start at bottom left on first platform
        self.player = Player(150, SCREEN_HEIGHT - 200)
        self.camera = Camera()
        self.falling = False
        self.fall_timer = 0

        # Quiz setup - 7 questions = need 21 coins (every 3rd triggers)
        self.num_questions = 7
        self.quiz_questions = get_randomized_questions(
            self.level_num,
            self.num_questions,
            self.lang.get_lang_code()
        )
        self.total_questions = len(self.quiz_questions)
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # State
        self.paused = False
        self.completed = False
        self.game_over = False
        self.questions_answered = 0
        self.correct_answers = 0
        self.level_score = 0
        self.coins_collected_count = 0

        # Timer and UI
        time_limit = LEVEL_TIME_LIMITS.get(self.difficulty, 480)
        self.timer = Timer(time_limit)
        self.score_display = ScoreDisplay(SCREEN_WIDTH - 220, 20, self.fonts['small'])

        # Generate parkour
        self.obstacles = []
        self.coins = []
        self.level_width = 0
        self.finish_platform = None
        self._generate_horizontal_parkour()

        # Void death line
        self.void_death_y = SCREEN_HEIGHT + 50

    def _generate_horizontal_parkour(self):
        """Generate horizontal parkour with 21 platforms and BIGGER GAPS"""
        # Starting platform (bottom left) - player spawns here
        start_platform = Platform(50, SCREEN_HEIGHT - 150, 200)
        self.obstacles.append(start_platform)

        # Level width for 21 platforms
        self.level_width = 8000

        # Generate 21 platforms with varied difficulty and BIGGER GAPS
        current_x = 350  # Start after the first platform

        # Height patterns (varied difficulty)
        heights = [
            SCREEN_HEIGHT - 150,  # Low (easy start)
            SCREEN_HEIGHT - 200,  # Medium-low
            SCREEN_HEIGHT - 250,  # Medium
            SCREEN_HEIGHT - 300,  # Medium-high
            SCREEN_HEIGHT - 350,  # High
            SCREEN_HEIGHT - 400,  # Very high
            SCREEN_HEIGHT - 200,  # Drop back down
            SCREEN_HEIGHT - 320,  # Back up
            SCREEN_HEIGHT - 380,  # Very high
            SCREEN_HEIGHT - 180,  # Low
            SCREEN_HEIGHT - 340,  # High
            SCREEN_HEIGHT - 260,  # Medium
            SCREEN_HEIGHT - 420,  # Very high (hardest)
            SCREEN_HEIGHT - 350,  # High
            SCREEN_HEIGHT - 230,  # Medium
            SCREEN_HEIGHT - 390,  # Very high
            SCREEN_HEIGHT - 200,  # Medium-low
            SCREEN_HEIGHT - 330,  # High
            SCREEN_HEIGHT - 280,  # Medium-high
            SCREEN_HEIGHT - 360,  # High
            SCREEN_HEIGHT - 300,  # Medium-high (last)
        ]

        # BIGGER Gap distances (increased from original)
        gap_distances = [
            250, 270, 290, 310, 330,  # Start with moderate gaps
            340, 360, 380, 400, 370,  # Get bigger
            390, 410, 430, 400, 380,  # Peak difficulty
            360, 340, 320, 300, 280,  # Slightly easier at end
            260  # Last one
        ]

        for i in range(21):
            x = current_x
            y = heights[i]

            # Platform width varies (harder = narrower)
            if i < 5:
                width = random.randint(120, 160)  # Easier start (wider)
            elif i < 12:
                width = random.randint(90, 120)  # Medium
            else:
                width = random.randint(80, 110)  # Harder end (narrower)

            # Create platform
            platform = Platform(x, y, width)
            self.obstacles.append(platform)

            # Coin on platform center
            coin_x = x + width // 2
            coin_y = y - 40
            coin = Coin(coin_x, coin_y)
            self.coins.append(coin)

            # Next platform distance (BIGGER GAPS)
            if i < len(gap_distances):
                current_x += gap_distances[i]
            else:
                current_x += 300

        # Finish platform - reachable height
        self.finish_platform = Platform(current_x + 180, SCREEN_HEIGHT - 300, 300)
        self.obstacles.append(self.finish_platform)

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
            return

        # If falling, show message and wait for restart
        if self.falling:
            self.fall_timer += 1
            if self.fall_timer > 60:  # Wait 1 second
                # Check for R key to restart
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.restart_level()
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop_horizontal()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.player.jump()

        # Apply gravity manually (bypass player's update which has ground collision)
        self.player.apply_gravity()

        # Store old position
        old_y = self.player.y

        # Move player
        self.player.x += self.player.vel_x
        self.player.y += self.player.vel_y

        # Platform collision detection (ONLY platforms, NO ground)
        self.player.on_ground = False
        player_rect = self.player.get_rect()

        for platform in self.obstacles:
            platform.update_rect()
            if player_rect.colliderect(platform.rect):
                # Landing on platform from above
                if self.player.vel_y > 0 and old_y + self.player.height <= platform.rect.top + self.player.vel_y:
                    self.player.y = platform.rect.top - self.player.height
                    self.player.vel_y = 0
                    self.player.on_ground = True
                # Hitting platform from below
                elif self.player.vel_y < 0 and old_y >= platform.rect.bottom:
                    self.player.y = platform.rect.bottom
                    self.player.vel_y = 5  # Bounce down
                # Side collision
                elif self.player.vel_x > 0:
                    self.player.x = platform.rect.left - self.player.width
                    self.player.vel_x = 0
                elif self.player.vel_x < 0:
                    self.player.x = platform.rect.right
                    self.player.vel_x = 0

        # Left border
        if self.player.x < 0:
            self.player.x = 0
            self.player.vel_x = 0

        # Right border
        if self.player.x > self.level_width - PLAYER_WIDTH:
            self.player.x = self.level_width - PLAYER_WIDTH
            self.player.vel_x = 0

        # VOID DEATH - if player falls below void line
        if self.player.y > self.void_death_y:
            self.falling = True
            self.fall_timer = 0
            return

        # Update invincibility timer
        if self.player.invincible:
            self.player.invincible_timer -= 1
            if self.player.invincible_timer <= 0:
                self.player.invincible = False

        # Camera follows player
        self.camera.update(self.player.x)

        # Update coins
        for coin in self.coins:
            coin.update()
            if coin.check_collection(self.player.get_rect()):
                if not coin.collected:
                    coin.collected = True
                    self.player.collect_coin()
                    self.coins_collected_count += 1
                    # Play coin sound
                    if self.coin_sound:
                        self.coin_sound.play()
                    self.level_score += POINTS['coin']
                    self.score_display.set_score(self.level_score)

                    # Every 3rd coin triggers quiz (coins 3, 6, 9, 12, 15, 18, 21 = 7 quizzes)
                    if self.coins_collected_count % 3 == 0 and self.current_quiz_index < len(self.quiz_questions):
                        self.current_quiz = QuizOverlay(
                            self.quiz_questions[self.current_quiz_index],
                            self.fonts
                        )
                        self.current_quiz_index += 1
                        self.quiz_active = True

        # Check completion - reached finish platform
        if self.questions_answered >= self.total_questions:
            if self.finish_platform.rect.colliderect(self.player.get_rect()):
                self.completed = True
                self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        self.score_display.update()

    def restart_level(self):
        """Restart the level (after void death)"""
        self.init_level()  # Re-initialize everything

    def draw(self, surface):
        """Draw everything"""
        # Sky gradient background (NO BLACK VOID)
        draw_gradient_background(surface, (135, 206, 250), (255, 220, 200))  # Blue to light sunset

        # Draw sun
        sun_x = 200 - int(self.camera.offset_x * 0.1)  # Parallax effect
        pygame.draw.circle(surface, (255, 220, 100), (sun_x, 120), 60)
        pygame.draw.circle(surface, (255, 200, 80), (sun_x, 120), 55)

        # Draw clouds (parallax)
        cloud_positions = [(150, 150), (400, 100), (650, 180), (900, 120), (1200, 140)]
        for cx, cy in cloud_positions:
            screen_x = int(cx - self.camera.offset_x * 0.3)  # Slower parallax
            if -200 < screen_x < SCREEN_WIDTH + 200:
                pygame.draw.ellipse(surface, WHITE, (screen_x, cy, 120, 60))
                pygame.draw.ellipse(surface, WHITE, (screen_x + 30, cy - 20, 100, 60))
                pygame.draw.ellipse(surface, WHITE, (screen_x + 60, cy - 10, 90, 50))

        # Draw platforms (orange/brown parkour style)
        for obstacle in self.obstacles:
            screen_x = obstacle.rect.x - self.camera.offset_x
            if -300 < screen_x < SCREEN_WIDTH + 300:
                platform_rect = pygame.Rect(screen_x, obstacle.rect.y, obstacle.rect.width, obstacle.rect.height)

                # Orange platform color
                pygame.draw.rect(surface, (230, 126, 34), platform_rect, border_radius=5)
                pygame.draw.rect(surface, (180, 100, 20), platform_rect, 3, border_radius=5)

                # Wood grain effect
                for i in range(3):
                    line_y = obstacle.rect.y + 5 + i * 5
                    if line_y < obstacle.rect.y + obstacle.rect.height - 5:
                        pygame.draw.line(surface, (200, 110, 30),
                                         (screen_x + 5, line_y),
                                         (screen_x + obstacle.rect.width - 5, line_y), 1)

        # Highlight finish platform
        if self.finish_platform and self.questions_answered >= self.total_questions:
            screen_x = self.finish_platform.rect.x - self.camera.offset_x
            finish_rect = pygame.Rect(screen_x, self.finish_platform.rect.y,
                                      self.finish_platform.rect.width, self.finish_platform.rect.height)

            # Animated glow
            glow_size = int(5 + abs(pygame.time.get_ticks() % 1000 - 500) / 50)
            pygame.draw.rect(surface, GOLD, finish_rect, glow_size, border_radius=8)
            pygame.draw.rect(surface, YELLOW, finish_rect, 3, border_radius=8)

            # "КРАЈ!" / "FUND!" text
            finish_text_key = 'finish'
            finish_text = self.fonts['large'].render(self.lang.get(finish_text_key), True, BLACK)
            finish_text_rect = finish_text.get_rect(center=finish_rect.center)
            surface.blit(finish_text, finish_text_rect)

        # Draw coins
        for coin in self.coins:
            coin.draw(surface, self.camera.offset_x)

        # Draw player
        self.player.draw(surface, self.camera.offset_x)

        # UI
        # Timer (top center)
        self.timer.draw(surface, self.fonts['medium'])

        # Score (top right)
        self.score_display.draw(surface)

        # Progress (below timer)
        progress_text = f"{self.lang.get('questions')}: {self.questions_answered}/{self.total_questions}"
        progress_surface = self.fonts['small'].render(progress_text, True, WHITE)
        progress_rect = progress_surface.get_rect(center=(SCREEN_WIDTH // 2, 130))

        # Background for progress
        bg_rect = pygame.Rect(progress_rect.x - 10, progress_rect.y - 5,
                              progress_rect.width + 20, progress_rect.height + 10)
        pygame.draw.rect(surface, DARK_BLUE, bg_rect, border_radius=10)
        surface.blit(progress_surface, progress_rect)

        # Title (top left)
        title = self.fonts['medium'].render(self.lang.get('parkour_challenge'), True, YELLOW)
        title_rect = pygame.Rect(10, 20, title.get_width() + 20, title.get_height() + 10)
        pygame.draw.rect(surface, (50, 50, 100, 200), title_rect, border_radius=10)
        surface.blit(title, (20, 25))

        # Distance (top left, below title)
        distance_text = f"{self.lang.get('distance')}: {int(self.player.x / 10)}m"
        distance_surface = self.fonts['small'].render(distance_text, True, WHITE)
        dist_rect = pygame.Rect(10, 70, distance_surface.get_width() + 20, distance_surface.get_height() + 10)
        pygame.draw.rect(surface, (50, 50, 100, 200), dist_rect, border_radius=10)
        surface.blit(distance_surface, (20, 75))

        # Coins collected indicator (top left, below distance)
        coins_text = f"{self.lang.get('coins')}: {self.coins_collected_count}/21"
        coins_surface = self.fonts['small'].render(coins_text, True, GOLD)
        coins_rect = pygame.Rect(10, 120, coins_surface.get_width() + 20, coins_surface.get_height() + 10)
        pygame.draw.rect(surface, (50, 50, 100, 200), coins_rect, border_radius=10)
        surface.blit(coins_surface, (20, 125))

        # FALLING MESSAGE - Press R to Restart
        if self.falling:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

            # Message box
            if self.lang.get_lang_code() == 'sq':
                fall_text = "Rashë në humnerë!"
                restart_text = "Shtyp R për të rifilluar"
            else:
                fall_text = "Паднавте во празнина!"
                restart_text = "Притисни R за рестарт"

            fall_surface = self.fonts['title'].render(fall_text, True, RED)
            fall_rect = fall_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            surface.blit(fall_surface, fall_rect)

            restart_surface = self.fonts['large'].render(restart_text, True, YELLOW)
            restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(restart_surface, restart_rect)

        # Quiz
        if self.quiz_active and self.current_quiz:
            self.current_quiz.draw(surface)

    def handle_input(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.quiz_active:
                    from main import fonts, lang_manager
                    result = pause_menu(pygame.display.get_surface(), pygame.time.Clock(), fonts, lang_manager)
                    if result == 'exit':
                        self.completed = True
                        return
            if event.key == pygame.K_r and self.falling:  # Restart when falling
                self.restart_level()

        if self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.current_quiz.handle_click(event.pos)
            if result is not None:
                self.questions_answered += 1
                if result:
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                pygame.time.wait(2500)  # 2.5 seconds to see result
                self.quiz_active = False
                self.current_quiz = None

    async def handle_input_async(self, event):
        """Handle input (async)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.quiz_active:
                    from main import fonts, lang_manager, pause_menu_async
                    result = await pause_menu_async(pygame.display.get_surface(), pygame.time.Clock(), fonts, lang_manager)
                    if result == 'exit':
                        self.completed = True
                        return
            if event.key == pygame.K_r and self.falling:  # Restart when falling
                self.restart_level()

        if self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.current_quiz.handle_click(event.pos)
            if result is not None:
                self.questions_answered += 1
                if result:
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                await asyncio.sleep(2.5)  # 2.5 seconds to see result
                self.quiz_active = False
                self.current_quiz = None

    def run(self, screen, clock):
        """Run level"""
        # Start background music
        try:
            pygame.mixer.music.load('creatives/game-level-music.ogg')
            pygame.mixer.music.set_volume(0.3)  # 30% volume
            pygame.mixer.music.play(-1)  # Loop forever
        except:
            pass

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                self.handle_input(event)

            self.update()
            self.draw(screen)

            if self.completed or self.game_over:
                # Play medal sound if level completed successfully
                if self.completed:
                    try:
                        medal_sound = pygame.mixer.Sound('medal-winning.ogg')
                        medal_sound.play()
                    except:
                        pass
                pygame.time.wait(1000)
                # Stop background music
                pygame.mixer.music.stop()

                return {
                    'action': 'menu',
                    'score': self.level_score,
                    'questions_correct': self.correct_answers,
                    'questions_total': self.total_questions,
                    'time_taken': int(self.timer.time_limit - self.timer.time_left)
                }

            pygame.display.flip()
            clock.tick(FPS)

    async def run_async(self, screen, clock):
        """Run level (async)"""
        # Start background music
        try:
            pygame.mixer.music.load('creatives/game-level-music.ogg')
            pygame.mixer.music.set_volume(0.3)  # 30% volume
            pygame.mixer.music.play(-1)  # Loop forever
        except:
            pass

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                await self.handle_input_async(event)

            self.update()
            self.draw(screen)

            if self.completed or self.game_over:
                # Play medal sound if level completed successfully
                if self.completed:
                    try:
                        medal_sound = pygame.mixer.Sound('medal-winning.ogg')
                        medal_sound.play()
                    except:
                        pass
                await asyncio.sleep(1)
                # Stop background music
                pygame.mixer.music.stop()

                return {
                    'action': 'menu',
                    'score': self.level_score,
                    'questions_correct': self.correct_answers,
                    'questions_total': self.total_questions,
                    'time_taken': int(self.timer.time_limit - self.timer.time_left)
                }

            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)
