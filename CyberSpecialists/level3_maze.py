# -*- coding: utf-8 -*-
"""
Level 3: Maze - With Macedonian text and better layout
"""

import pygame
import asyncio
from constants import *
from obstacles import Coin
from ui import Timer, ScoreDisplay, QuizOverlay, draw_gradient_background
from questions_bank import get_randomized_questions
from main import pause_menu, pause_menu_async


class MazeLevel:
    """Level 3: Maze matching the image"""

    def __init__(self, level_num, difficulty, fonts, lang_manager=None):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager

        # Load Jerry image as player
        try:
            self.jerry_img = pygame.image.load('creatives/jerry-removebg-preview.png')
            # Scale Jerry to appropriate size for maze (smaller)
            self.jerry_img = pygame.transform.scale(self.jerry_img, (40, 40))
        except:
            self.jerry_img = None

        # Load coin image
        try:
            self.coin_img = pygame.image.load('creatives/coin-photo-removebg-preview.png')
            self.coin_img = pygame.transform.scale(self.coin_img, (40, 40))
        except:
            self.coin_img = None

        # Load cheese image for exit
        try:
            self.cheese_img = pygame.image.load('creatives/cheese-removebg-preview.png')
            self.cheese_img = pygame.transform.scale(self.cheese_img, (60, 60))
        except:
            self.cheese_img = None

        # Load coin collection sound
        try:
            self.coin_sound = pygame.mixer.Sound('coincollect.ogg')
            self.coin_sound.set_volume(0.5)
        except:
            self.coin_sound = None

        # Smaller player for maze
        self.player_size = 40  # Visual size (matches Jerry image)
        self.player_hitbox_size = 20  # Small hitbox for tight corridors
        self.player_x = 230  # Inside maze at START (top center)
        self.player_y = 180  # Just below top wall

        # Quiz setup - FIXED: 7 coins = 7 questions
        num_questions = 7
        self.quiz_questions = get_randomized_questions(level_num, num_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
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
        self.coins_collected = 0
        self.health = 3

        # Timer and UI
        time_limit = LEVEL_TIME_LIMITS.get(difficulty, 480)
        self.timer = Timer(time_limit)
        self.score_display = ScoreDisplay(SCREEN_WIDTH - 220, 20, fonts['small'])

        # Generate maze
        self.walls = []
        self.coins = []
        self.exit_rect = None
        self._generate_exact_maze()

    def _generate_exact_maze(self):
        """Generate MUCH HARDER maze with many walls"""
        # Maze settings - centered
        maze_left = 200
        maze_top = 150
        cell_size = 60
        wall_thick = 10

        # Total size: 12x10 cells
        maze_width = cell_size * 12
        maze_height = cell_size * 10

        # Helper function to add wall
        def add_wall(col, row, horizontal, length):
            if horizontal:
                x = maze_left + col * cell_size
                y = maze_top + row * cell_size
                w = cell_size * length
                h = wall_thick
            else:
                x = maze_left + col * cell_size
                y = maze_top + row * cell_size
                w = wall_thick
                h = cell_size * length
            self.walls.append(pygame.Rect(x, y, w, h))

        # Outer walls
        add_wall(0, 0, True, 12)
        add_wall(0, 10, True, 12)
        add_wall(0, 0, False, 10)
        add_wall(12, 0, False, 10)

        # MANY internal walls for complex maze
        # Row 1 area - dense walls
        add_wall(1, 1, True, 1)
        add_wall(2, 1, False, 2)
        add_wall(3, 1, True, 2)
        add_wall(5, 1, False, 1)
        add_wall(6, 1, True, 1)
        add_wall(7, 1, False, 2)
        add_wall(8, 1, True, 2)
        add_wall(10, 1, False, 1)
        add_wall(11, 1, False, 2)

        # Row 2 area
        add_wall(1, 2, True, 2)
        add_wall(4, 2, True, 1)
        add_wall(5, 2, False, 2)
        add_wall(6, 2, True, 2)
        add_wall(9, 2, True, 1)
        add_wall(10, 2, False, 2)

        # Row 3 area - very dense
        add_wall(1, 3, False, 1)
        add_wall(2, 3, True, 1)
        add_wall(3, 3, False, 2)
        add_wall(4, 3, True, 2)
        add_wall(6, 3, False, 1)
        add_wall(7, 3, True, 2)
        add_wall(9, 3, False, 2)
        add_wall(10, 3, True, 1)

        # Row 4 area - REMOVED BLOCKING WALL
        add_wall(1, 4, True, 2)
        add_wall(3, 4, False, 2)
        add_wall(4, 4, True, 1)
        add_wall(5, 4, False, 1)
        # REMOVED: add_wall(6, 4, True, 3)  # This was blocking access to coins
        add_wall(9, 4, False, 1)
        add_wall(10, 4, True, 1)
        add_wall(11, 4, False, 2)

        # Row 5 area - center complexity
        add_wall(1, 5, False, 2)
        add_wall(2, 5, True, 2)
        add_wall(4, 5, False, 1)
        add_wall(5, 5, True, 1)
        add_wall(6, 5, False, 2)
        add_wall(7, 5, True, 2)
        add_wall(9, 5, True, 1)
        add_wall(10, 5, False, 1)

        # Row 6 area
        add_wall(1, 6, True, 1)
        add_wall(2, 6, False, 2)
        add_wall(3, 6, True, 2)
        add_wall(5, 6, False, 2)
        add_wall(6, 6, True, 1)
        add_wall(8, 6, True, 2)
        add_wall(10, 6, False, 2)
        add_wall(11, 6, True, 1)

        # Row 7 area
        add_wall(1, 7, False, 1)
        add_wall(2, 7, True, 1)
        add_wall(4, 7, True, 2)
        add_wall(6, 7, False, 2)
        add_wall(7, 7, True, 1)
        add_wall(8, 7, False, 1)
        add_wall(9, 7, True, 2)
        add_wall(11, 7, False, 1)

        # Row 8 area - bottom complexity
        add_wall(1, 8, True, 2)
        add_wall(3, 8, False, 2)
        add_wall(4, 8, True, 1)
        add_wall(5, 8, False, 1)
        add_wall(6, 8, True, 2)
        add_wall(8, 8, False, 2)
        add_wall(9, 8, True, 1)
        add_wall(10, 8, False, 1)

        # Row 9 area - near bottom
        add_wall(1, 9, False, 1)
        add_wall(2, 9, True, 2)
        add_wall(4, 9, False, 1)
        add_wall(5, 9, True, 2)
        add_wall(7, 9, False, 1)
        add_wall(8, 9, True, 2)
        add_wall(10, 9, True, 1)
        add_wall(11, 9, False, 1)

        # Place 7 coins (one per question) in accessible spots
        coin_positions = [
            (1.5, 1.5),  # Top left
            (6.5, 1.5),  # Top center
            (10.5, 2.5),  # Top right
            (2.5, 4.5),  # Mid left
            (7.5, 5.5),  # Center
            (3.5, 7.5),  # Bottom left
            (10.5, 8.5),  # Bottom right
        ]

        for col, row in coin_positions:
            coin_x = maze_left + int(col * cell_size)
            coin_y = maze_top + int(row * cell_size)
            self.coins.append(Coin(coin_x, coin_y))

        # Exit at bottom right - MOVED SLIGHTLY RIGHT
        exit_x = maze_left + maze_width - cell_size + 10  # Changed from -20 to +10
        exit_y = maze_top + maze_height - cell_size + 10
        self.exit_rect = pygame.Rect(exit_x, exit_y, 60, 60)

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
            return

        # Player movement
        keys = pygame.key.get_pressed()
        old_x = self.player_x
        old_y = self.player_y

        move_speed = 4

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += move_speed

        # Wall collision
        # Use smaller hitbox for collision detection (easier navigation)
        player_rect = pygame.Rect(self.player_x - self.player_hitbox_size // 2,
                                  self.player_y - self.player_hitbox_size // 2,
                                  self.player_hitbox_size, self.player_hitbox_size)
        for wall in self.walls:
            if player_rect.colliderect(wall):
                self.player_x = old_x
                self.player_y = old_y
                break

        # Update coins - TRIGGER QUIZ AFTER EACH COIN (1 coin = 1 quiz)
        for coin in self.coins:
            coin.update()
            if not coin.collected:
                coin_rect = pygame.Rect(coin.x - 20, coin.y - 20, 40, 40)
                if player_rect.colliderect(coin_rect):
                    coin.collected = True
                    self.coins_collected += 1
                    # Play coin sound
                    if self.coin_sound:
                        self.coin_sound.play()
                    self.level_score += POINTS['coin']
                    self.score_display.set_score(self.level_score)

                    # TRIGGER QUIZ IMMEDIATELY (1 quiz per coin = 7 total)
                    if self.current_quiz_index < len(self.quiz_questions):
                        self.current_quiz = QuizOverlay(
                            self.quiz_questions[self.current_quiz_index],
                            self.fonts
                        )
                        self.current_quiz_index += 1
                        self.quiz_active = True

        # Check completion
        if self.questions_answered >= self.total_questions:
            if self.exit_rect.colliderect(player_rect):
                self.completed = True
                self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything"""
        # Blue sky background
        surface.fill((135, 206, 250))  # Sky blue

        # Timer in center
        self.timer.draw(surface, self.fonts['medium'])

        # Draw walls - GREEN like the image
        for wall in self.walls:
            pygame.draw.rect(surface, (0, 150, 80), wall)
            pygame.draw.rect(surface, (0, 100, 50), wall, 2)

        # Draw coins with image
        for coin in self.coins:
            if not coin.collected:
                if self.coin_img:
                    coin_x = int(coin.x - 20)  # Center the 40x40 image
                    coin_y = int(coin.y - 20)
                    surface.blit(self.coin_img, (coin_x, coin_y))
                else:
                    # Fallback to circles
                    pygame.draw.circle(surface, GOLD, (int(coin.x), int(coin.y)), 18)
                    pygame.draw.circle(surface, YELLOW, (int(coin.x), int(coin.y)), 14)
                    pygame.draw.circle(surface, GOLD, (int(coin.x), int(coin.y)), 8)

        # Draw exit (cheese)
        if self.questions_answered >= self.total_questions:
            # Draw cheese image when exit is unlocked
            if self.cheese_img:
                cheese_x = self.exit_rect.centerx - 30
                cheese_y = self.exit_rect.centery - 30
                surface.blit(self.cheese_img, (cheese_x, cheese_y))
            else:
                pygame.draw.rect(surface, GOLD, self.exit_rect, border_radius=10)
                pygame.draw.rect(surface, YELLOW, self.exit_rect, 4, border_radius=10)
                exit_text = self.fonts['small'].render("EXIT", True, BLACK)
                exit_text_rect = exit_text.get_rect(center=self.exit_rect.center)
                surface.blit(exit_text, exit_text_rect)
        else:
            # Locked - show grayed cheese
            if self.cheese_img:
                cheese_x = self.exit_rect.centerx - 30
                cheese_y = self.exit_rect.centery - 30
                # Create a grayed version
                gray_cheese = self.cheese_img.copy()
                gray_cheese.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
                surface.blit(gray_cheese, (cheese_x, cheese_y))

                # Draw lock symbol on top
                lock_text = self.fonts['medium'].render("🔒", True, RED)
                lock_rect = lock_text.get_rect(center=self.exit_rect.center)
                surface.blit(lock_text, lock_rect)
            else:
                pygame.draw.rect(surface, LIGHT_GRAY, self.exit_rect, border_radius=10)
                pygame.draw.rect(surface, DARK_GRAY, self.exit_rect, 3, border_radius=10)
                lock_text = self.fonts['tiny'].render("LOCKED", True, RED)
                lock_rect = lock_text.get_rect(center=self.exit_rect.center)
                surface.blit(lock_text, lock_rect)

        # Draw player - JERRY THE MOUSE
        if self.jerry_img:
            # Draw Jerry image centered on player position
            jerry_x = self.player_x - self.player_size // 2
            jerry_y = self.player_y - self.player_size // 2
            surface.blit(self.jerry_img, (jerry_x, jerry_y))
        else:
            # Fallback to red square if image not found
            player_rect_visual = pygame.Rect(self.player_x - self.player_size // 2,
                                             self.player_y - self.player_size // 2,
                                             self.player_size, self.player_size)
            pygame.draw.rect(surface, RED, player_rect_visual, border_radius=5)
            pygame.draw.rect(surface, WHITE, player_rect_visual, 2, border_radius=5)

        # Progress indicator (top left)
        progress_text = f"{self.lang.get('questions') if self.lang else 'Прашања'}: {self.questions_answered}/{self.total_questions}"
        progress_surface = self.fonts['small'].render(progress_text, True, WHITE)

        # Background box for progress
        progress_bg = pygame.Rect(15, 15, progress_surface.get_width() + 20, progress_surface.get_height() + 10)
        pygame.draw.rect(surface, DARK_BLUE, progress_bg, border_radius=10)
        pygame.draw.rect(surface, GOLD, progress_bg, 3, border_radius=10)

        surface.blit(progress_surface, (25, 20))

        # Coins collected (top left, below progress)
        coins_text = f"Монети: {self.coins_collected}/7"
        coins_surface = self.fonts['small'].render(coins_text, True, GOLD)

        # Background box for coins
        coins_bg = pygame.Rect(15, 70, coins_surface.get_width() + 20, coins_surface.get_height() + 10)
        pygame.draw.rect(surface, DARK_BLUE, coins_bg, border_radius=10)
        pygame.draw.rect(surface, GOLD, coins_bg, 3, border_radius=10)

        surface.blit(coins_surface, (25, 75))

        # Score display (top right)
        self.score_display.draw(surface)

        # YOU WON message when completed
        if self.completed:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

            # Congratulations message
            congrats_text = self.lang.get('congratulations') if self.lang else 'Честитки!'
            congrats_surface = self.fonts['title'].render(congrats_text, True, GOLD)
            congrats_rect = congrats_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            surface.blit(congrats_surface, congrats_rect)

            # You won message
            won_text = self.lang.get('you_won') if self.lang else 'Ти победи!'
            won_surface = self.fonts['large'].render(won_text, True, YELLOW)
            won_rect = won_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(won_surface, won_rect)

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

        if self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.current_quiz.handle_click(event.pos)
            if result is not None:
                self.questions_answered += 1
                if result:
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                pygame.time.wait(500)  # 2.5 seconds to see result
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

        if self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.current_quiz.handle_click(event.pos)
            if result is not None:
                self.questions_answered += 1
                if result:
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                await asyncio.sleep(0.5)
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
                pygame.time.wait(500)  # Wait 2 seconds to see win message
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
                await asyncio.sleep(0.5)
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
