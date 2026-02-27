# -*- coding: utf-8 -*-
"""
Level 1: Mario-style platformer with password typing and enemy quiz
"""

import pygame
import asyncio
import random
import math
from constants import *
from player import Player
from obstacles import Coin, Platform, Enemy, MovingEnemy, Shield, Finish
from ui import Camera, Timer, ScoreDisplay, QuizOverlay, draw_gradient_background
from questions_bank import get_randomized_questions
from main import pause_menu, pause_menu_async


class PasswordTypingOverlay:
    """Password creation mini-game - USER CREATES THEIR OWN PASSWORD"""

    def __init__(self, fonts, lang_manager=None):
        self.fonts = fonts
        self.lang = lang_manager
        self.user_input = ''
        self.completed = False
        self.success = False

    def _calculate_strength(self, password):
        """Calculate password strength percentage"""
        strength = 0
        if len(password) >= 8:
            strength += 25
        if any(c.isupper() for c in password):
            strength += 20
        if any(c.islower() for c in password):
            strength += 20
        if any(c.isdigit() for c in password):
            strength += 20
        if any(c in '!@#$%^&*()_+-=' for c in password):
            strength += 15
        return min(100, strength)

    def _get_strength_text(self, strength):
        """Get strength description"""
        if strength < 40:
            return (self.lang.get('weak') if self.lang else 'Слаба'), RED
        elif strength < 60:
            return (self.lang.get('medium_strength') if self.lang else 'Средна'), ORANGE
        elif strength < 80:
            return (self.lang.get('strong') if self.lang else 'Јака'), GREEN
        else:
            return (self.lang.get('very_strong') if self.lang else 'Многу Јака'), CYAN

    def handle_event(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                strength = self._calculate_strength(self.user_input)
                if strength >= 60:
                    self.completed = True
                    self.success = True
            elif event.key == pygame.K_ESCAPE:
                self.completed = True
                self.success = False
            elif len(event.unicode) == 1 and event.unicode.isprintable():
                if len(self.user_input) < 30:
                    self.user_input += event.unicode

    def draw(self, surface):
        """Draw password creation interface"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        box_width = 900
        box_height = 550
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        shadow_rect = pygame.Rect(box_x + 8, box_y + 8, box_width, box_height)
        pygame.draw.rect(surface, BLACK, shadow_rect, border_radius=30)

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(surface, WHITE, box_rect, border_radius=30)
        pygame.draw.rect(surface, PURPLE, box_rect, 6, border_radius=30)

        title_text = self.lang.get('create_password') if self.lang else "Креирај Силна Лозинка!"
        title = self.fonts['large'].render(title_text, True, PURPLE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, box_y + 50))
        surface.blit(title, title_rect)

        input_box = pygame.Rect(box_x + 100, box_y + 150, box_width - 200, 60)
        pygame.draw.rect(surface, LIGHT_BLUE, input_box, border_radius=15)
        pygame.draw.rect(surface, CYAN, input_box, 4, border_radius=15)

        display_text = '*' * len(self.user_input) if self.user_input else (
            self.lang.get('type_password_here') if self.lang else 'Внеси лозинка...'
        )
        input_surface = self.fonts['medium'].render(display_text, True,
                                                    BLACK if self.user_input else LIGHT_GRAY)
        input_rect = input_surface.get_rect(center=input_box.center)
        surface.blit(input_surface, input_rect)

        if self.user_input:
            strength = self._calculate_strength(self.user_input)
            strength_text, strength_color = self._get_strength_text(strength)

            strength_label_text = self.lang.get('password_strength') if self.lang else "Јакост:"
            strength_label = self.fonts['small'].render(strength_label_text, True, DARK_BLUE)
            strength_label_rect = strength_label.get_rect(center=(SCREEN_WIDTH // 2, box_y + 250))
            surface.blit(strength_label, strength_label_rect)

            bar_width = 600
            bar_height = 40
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = box_y + 290

            bar_bg = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(surface, LIGHT_GRAY, bar_bg, border_radius=20)
            pygame.draw.rect(surface, BLACK, bar_bg, 3, border_radius=20)

            filled_width = int((strength / 100) * bar_width)
            if filled_width > 0:
                filled_bar = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
                pygame.draw.rect(surface, strength_color, filled_bar, border_radius=20)

            strength_percent = self.fonts['medium'].render(f"{strength_text}: {strength}%",
                                                           True, WHITE)
            strength_percent_rect = strength_percent.get_rect(center=(SCREEN_WIDTH // 2, bar_y + 20))
            surface.blit(strength_percent, strength_percent_rect)

        # Instructions at bottom
        instruction_text = self.lang.get('press_enter') if self.lang else "Притисни ENTER кога е точно | ESC за откажи"
        instruction = self.fonts['tiny'].render(instruction_text, True, DARK_GRAY)
        inst_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, box_y + box_height - 30))
        surface.blit(instruction, inst_rect)


class Castle:
    """Castle at finish line"""

    def __init__(self, x):
        self.x = x
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 200
        self.width = 180
        self.height = 200

    def get_blocking_rect(self):
        """Get rect that blocks player movement"""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camera_offset_x):
        """Draw castle"""
        screen_x = int(self.x - camera_offset_x)

        # Main castle body (gray stone)
        castle_body = pygame.Rect(screen_x, self.y + 60, self.width, self.height - 60)
        pygame.draw.rect(surface, (120, 120, 120), castle_body)
        pygame.draw.rect(surface, (80, 80, 80), castle_body, 4)

        # Stone brick pattern
        brick_size = 30
        for row in range(0, self.height - 60, brick_size):
            offset = (row // brick_size) % 2 * (brick_size // 2)
            for col in range(-offset, self.width, brick_size):
                brick_rect = pygame.Rect(screen_x + col, self.y + 60 + row, brick_size - 2, brick_size - 2)
                pygame.draw.rect(surface, (100, 100, 100), brick_rect)

        # Left tower
        left_tower = pygame.Rect(screen_x, self.y, 50, 100)
        pygame.draw.rect(surface, (140, 140, 140), left_tower)
        pygame.draw.rect(surface, (80, 80, 80), left_tower, 3)

        # Left tower top (crenellations)
        for i in range(3):
            cren = pygame.Rect(screen_x + i * 20, self.y - 15, 15, 15)
            pygame.draw.rect(surface, (140, 140, 140), cren)
            pygame.draw.rect(surface, (80, 80, 80), cren, 2)

        # Right tower
        right_tower = pygame.Rect(screen_x + self.width - 50, self.y, 50, 100)
        pygame.draw.rect(surface, (140, 140, 140), right_tower)
        pygame.draw.rect(surface, (80, 80, 80), right_tower, 3)

        # Right tower top (crenellations)
        for i in range(3):
            cren = pygame.Rect(screen_x + self.width - 50 + i * 20, self.y - 15, 15, 15)
            pygame.draw.rect(surface, (140, 140, 140), cren)
            pygame.draw.rect(surface, (80, 80, 80), cren, 2)

        # Door (dark brown)
        door = pygame.Rect(screen_x + 65, self.y + 120, 50, 80)
        pygame.draw.rect(surface, (101, 67, 33), door, border_radius=10)
        pygame.draw.rect(surface, (70, 40, 20), door, 3, border_radius=10)

        # Door handle
        pygame.draw.circle(surface, GOLD, (screen_x + 100, self.y + 160), 5)

        # Windows
        window1 = pygame.Rect(screen_x + 15, self.y + 30, 20, 25)
        pygame.draw.rect(surface, (50, 100, 150), window1, border_radius=5)
        pygame.draw.rect(surface, BLACK, window1, 2, border_radius=5)

        window2 = pygame.Rect(screen_x + self.width - 35, self.y + 30, 20, 25)
        pygame.draw.rect(surface, (50, 100, 150), window2, border_radius=5)
        pygame.draw.rect(surface, BLACK, window2, 2, border_radius=5)

        # Flag on top
        flag_pole_x = screen_x + self.width // 2
        pygame.draw.line(surface, (60, 60, 60), (flag_pole_x, self.y - 15), (flag_pole_x, self.y - 60), 3)

        # Red flag
        flag_points = [
            (flag_pole_x, self.y - 55),
            (flag_pole_x + 35, self.y - 45),
            (flag_pole_x, self.y - 35)
        ]
        pygame.draw.polygon(surface, RED, flag_points)
        pygame.draw.polygon(surface, DARK_BLUE, flag_points, 2)


class GameLevel:
    """Level 1: Mario-style platformer"""

    def __init__(self, level_num, difficulty, fonts, lang_manager=None):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager

        # Load coin collection sound
        try:
            self.coin_sound = pygame.mixer.Sound('coincollect.ogg')
            self.coin_sound.set_volume(0.5)
        except:
            self.coin_sound = None

        # Load player image (Mario)
        try:
            self.player_img = pygame.image.load('creatives/player-fixed-removebg-preview.png')
            self.player_img = pygame.transform.scale(self.player_img, (70, 80))  # Bigger Mario
        except:
            self.player_img = None

        # Load enemy image
        try:
            self.enemy_img = pygame.image.load('creatives/enemies-fixed-removebg-preview.png')
            self.enemy_img = pygame.transform.scale(self.enemy_img, (70, 70))  # Bigger enemy
        except:
            self.enemy_img = None

        # Player
        self.player = Player(100, SCREEN_HEIGHT - 200)
        self.camera = Camera()

        # Calculate questions: 3 passwords = need 7 coins (every 2nd coin triggers)
        # 3 quiz questions = need 6 enemies (every 2nd enemy triggers)
        self.num_password_questions = 3
        self.num_quiz_questions = 3
        self.total_questions = self.num_password_questions + self.num_quiz_questions

        # Get quiz questions
        self.quiz_questions = get_randomized_questions(level_num, self.num_quiz_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # Password typing
        self.password_overlay = None
        self.password_active = False
        self.passwords_typed = 0

        # State
        self.paused = False
        self.completed = False
        self.game_over = False
        self.questions_answered = 0
        self.correct_answers = 0
        self.level_score = 0

        # Timer and UI
        time_limit = LEVEL_TIME_LIMITS.get(difficulty, 480)
        self.timer = Timer(time_limit)
        self.score_display = ScoreDisplay(SCREEN_WIDTH - 220, 20, fonts['small'])

        # Generate Mario-style level
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.shields = []
        self.castle = None
        self.level_width = 0

        # Track coin/enemy counters
        self.coins_collected_count = 0
        self.enemies_defeated_count = 0

        self._generate_mario_level()

    def _generate_mario_level(self):
        """Generate Mario-style level"""
        self.level_width = 4000

        # Ground
        ground = Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, self.level_width)
        self.platforms.append(ground)

        # Generate platforms
        platform_positions = [
            (300, SCREEN_HEIGHT - 200, 200),
            (600, SCREEN_HEIGHT - 250, 150),
            (900, SCREEN_HEIGHT - 300, 180),
            (1200, SCREEN_HEIGHT - 200, 200),
            (1500, SCREEN_HEIGHT - 350, 150),
            (1800, SCREEN_HEIGHT - 250, 200),
            (2100, SCREEN_HEIGHT - 300, 150),
            (2400, SCREEN_HEIGHT - 400, 180),
            (2700, SCREEN_HEIGHT - 300, 200),
            (3000, SCREEN_HEIGHT - 250, 180),
        ]

        for x, y, width in platform_positions:
            platform = Platform(x, y, width)
            self.platforms.append(platform)

        # Generate 7 coins (every 2nd triggers password = 3 passwords + 1 extra)
        for i in range(7):
            x = 300 + i * 450
            y = SCREEN_HEIGHT - GROUND_HEIGHT - 100 - random.randint(0, 100)
            coin = Coin(x, y)
            self.coins.append(coin)

        # Generate 6 enemies (every 2nd triggers quiz = 3 quiz questions)
        enemy_types = ['virus', 'hacker', 'phishing', 'malware']
        for i in range(6):
            x = 500 + i * 550
            y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT - 5
            enemy_type = random.choice(enemy_types)

            if random.random() < 0.4:
                start_x = x
                end_x = x + random.randint(80, 120)
                enemy = MovingEnemy(x, y, enemy_type, start_x, end_x, speed=2)
            else:
                enemy = Enemy(x, y, enemy_type)

            self.enemies.append(enemy)

        # Shields
        for i in range(5):
            x = 700 + i * 600
            y = SCREEN_HEIGHT - GROUND_HEIGHT - 120 - random.randint(0, 80)
            self.shields.append(Shield(x, y))

        # Castle at the end
        castle_x = self.level_width - 300
        self.castle = Castle(castle_x)

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active or self.password_active:
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop_horizontal()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump()

        # Update player
        self.player.update(self.platforms)

        # Block player from going past castle ONLY if questions not answered
        if self.castle and self.questions_answered < self.total_questions:
            castle_rect = self.castle.get_blocking_rect()
            player_rect = self.player.get_rect()

            if player_rect.colliderect(castle_rect):
                # Push player back
                if self.player.vel_x > 0:  # Moving right
                    self.player.x = castle_rect.left - self.player.width
                    self.player.vel_x = 0

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

                    # Every 2nd coin triggers password (coins 2, 4, 6 = 3 passwords)
                    if self.coins_collected_count % 2 == 0 and self.passwords_typed < self.num_password_questions:
                        self.passwords_typed += 1
                        self.password_overlay = PasswordTypingOverlay(self.fonts, self.lang)
                        self.password_active = True

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

            if not enemy.defeated:
                if self.player.get_hitbox().colliderect(enemy.get_hitbox()):
                    # Check if jumping on enemy
                    if self.player.vel_y > 0 and self.player.y + self.player.height - 15 < enemy.y + enemy.height // 2:
                        enemy.defeat()
                        # Play enemy killed sound
                        try:
                            enemy_sound = pygame.mixer.Sound('creatives/enemy-killed.ogg')
                            enemy_sound.play()
                        except:
                            pass
                        self.player.vel_y = -10
                        self.enemies_defeated_count += 1
                        self.level_score += POINTS['enemy_defeat']
                        self.score_display.set_score(self.level_score)

                        # Every 2nd enemy triggers quiz (enemies 2, 4, 6 = 3 quizzes)
                        if self.enemies_defeated_count % 2 == 0 and self.current_quiz_index < len(self.quiz_questions):
                            self.current_quiz = QuizOverlay(
                                self.quiz_questions[self.current_quiz_index],
                                self.fonts
                            )
                            self.current_quiz_index += 1
                            self.quiz_active = True
                    else:
                        if self.player.take_damage():
                            pass

        # Update shields
        for shield in self.shields:
            shield.update()
            if shield.check_collection(self.player.get_rect()):
                if not shield.collected:
                    shield.collected = True
                    self.player.collect_shield()
                    self.level_score += POINTS['shield']
                    self.score_display.set_score(self.level_score)

        # Check completion - player reaches castle after all questions
        if self.questions_answered >= self.total_questions:
            if self.castle:
                castle_rect = self.castle.get_blocking_rect()
                player_rect = self.player.get_rect()
                if player_rect.colliderect(castle_rect):
                    self.completed = True
                    self.level_score += POINTS['level_complete']

        # Timer
        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        if self.player.health <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything"""
        # Sky background
        draw_gradient_background(surface, (135, 206, 250), (200, 230, 255))

        # Clouds
        cloud_positions = [(150, 100), (500, 80), (900, 120), (1300, 90), (1700, 110), (2100, 100)]
        for cx, cy in cloud_positions:
            screen_x = cx - self.camera.offset_x
            if -200 < screen_x < SCREEN_WIDTH + 200:
                pygame.draw.ellipse(surface, WHITE, (screen_x, cy, 120, 50))
                pygame.draw.ellipse(surface, WHITE, (screen_x + 30, cy - 20, 100, 50))
                pygame.draw.ellipse(surface, WHITE, (screen_x + 60, cy - 10, 90, 40))

        # Hills
        hill_positions = [(300, SCREEN_HEIGHT - GROUND_HEIGHT), (1000, SCREEN_HEIGHT - GROUND_HEIGHT),
                          (1700, SCREEN_HEIGHT - GROUND_HEIGHT), (2400, SCREEN_HEIGHT - GROUND_HEIGHT)]
        for hx, hy in hill_positions:
            screen_x = hx - self.camera.offset_x
            if -300 < screen_x < SCREEN_WIDTH + 300:
                pygame.draw.ellipse(surface, (100, 200, 100), (screen_x - 150, hy - 80, 300, 160))

        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(surface, (210, 105, 30), ground_rect)
        pygame.draw.rect(surface, (139, 69, 19), ground_rect, 3)

        # Grass
        for i in range(0, SCREEN_WIDTH, 30):
            pygame.draw.line(surface, GREEN, (i, SCREEN_HEIGHT - GROUND_HEIGHT),
                             (i, SCREEN_HEIGHT - GROUND_HEIGHT + 5), 2)

        # Platforms (brick style)
        for platform in self.platforms[1:]:
            screen_x = platform.rect.x - self.camera.offset_x
            if -300 < screen_x < SCREEN_WIDTH + 300:
                pygame.draw.rect(surface, (200, 100, 50),
                                 (screen_x, platform.rect.y, platform.rect.width, platform.rect.height),
                                 border_radius=5)
                pygame.draw.rect(surface, (150, 75, 25),
                                 (screen_x, platform.rect.y, platform.rect.width, platform.rect.height),
                                 3, border_radius=5)

                # Brick pattern
                brick_width = 40
                brick_height = 20
                for row in range(0, platform.rect.height, brick_height):
                    offset = (row // brick_height) % 2 * (brick_width // 2)
                    for col in range(-offset, platform.rect.width, brick_width):
                        brick_rect = pygame.Rect(screen_x + col, platform.rect.y + row, brick_width - 2,
                                                 brick_height - 2)
                        pygame.draw.rect(surface, (180, 90, 40), brick_rect, border_radius=3)

        # Draw coins
        for coin in self.coins:
            coin.draw(surface, self.camera.offset_x)

        # Draw shields
        for shield in self.shields:
            shield.draw(surface, self.camera.offset_x)

        # Draw enemies
        # Draw enemies (with image)
        for enemy in self.enemies:
            if not enemy.defeated:  # Only draw if not defeated
                if self.enemy_img:
                    # Enemy hitbox is 40x40, image is 70x70 - align bottoms
                    enemy_screen_x = enemy.x - self.camera.offset_x - 15  # Center 70px over 40px
                    enemy_screen_y = enemy.y - 30  # Bottom of 70px image = bottom of 40px hitbox
                    surface.blit(self.enemy_img, (enemy_screen_x, enemy_screen_y))
                else:
                    # Fallback to default drawing
                    enemy.draw(surface, self.camera.offset_x)

        # Draw castle
        if self.castle:
            self.castle.draw(surface, self.camera.offset_x)

        # Draw player (Mario image)
        if self.player_img:
            # Player hitbox is 40x40, starting at player.x, player.y (top-left)
            # Mario image is 70x80 - align bottom of image with bottom of hitbox
            player_screen_x = self.player.x - self.camera.offset_x - 15  # Center 70px over 40px
            player_screen_y = self.player.y - 30  # Lowered by 10px total (was -40, then -35, now -30)
            surface.blit(self.player_img, (player_screen_x, player_screen_y))
        else:
            # Fallback to default drawing
            self.player.draw(surface, self.camera.offset_x)

        # UI
        self.player.draw_ui(surface, self.fonts['small'])
        self.timer.draw(surface, self.fonts['medium'])
        self.score_display.draw(surface)

        # Progress
        progress_text = f"Прашања: {self.questions_answered}/{self.total_questions}"
        progress_surface = self.fonts['small'].render(progress_text, True, WHITE)
        progress_rect = progress_surface.get_rect(center=(SCREEN_WIDTH // 2, 130))

        bg_rect = pygame.Rect(progress_rect.x - 10, progress_rect.y - 5, progress_rect.width + 20,
                              progress_rect.height + 10)
        pygame.draw.rect(surface, DARK_BLUE, bg_rect, border_radius=10)
        surface.blit(progress_surface, progress_rect)

        # Password overlay
        if self.password_active and self.password_overlay:
            self.password_overlay.draw(surface)

        # Quiz overlay
        if self.quiz_active and self.current_quiz:
            self.current_quiz.draw(surface)

    def handle_input(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:

                if not self.quiz_active and not self.password_active:

                    from main import fonts, lang_manager

                    result = pause_menu(pygame.display.get_surface(), pygame.time.Clock(), fonts, lang_manager)

                    if result == 'exit':
                        self.completed = True

                        return

        # Password typing
        if self.password_active and self.password_overlay:
            self.password_overlay.handle_event(event)
            if self.password_overlay.completed:
                if self.password_overlay.success:
                    self.questions_answered += 1
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                pygame.time.wait(500)
                self.password_active = False
                self.password_overlay = None

        # Quiz input
        if self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN:
            result = self.current_quiz.handle_click(event.pos)
            if result is not None:
                self.questions_answered += 1
                if result:
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                pygame.time.wait(500)
                self.quiz_active = False
                self.current_quiz = None

    async def handle_input_async(self, event):
        """Handle input (async)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.quiz_active and not self.password_active:
                    from main import fonts, lang_manager, pause_menu_async
                    result = await pause_menu_async(pygame.display.get_surface(), pygame.time.Clock(), fonts, lang_manager)
                    if result == 'exit':
                        self.completed = True
                        return

        # Password typing
        if self.password_active and self.password_overlay:
            self.password_overlay.handle_event(event)
            if self.password_overlay.completed:
                if self.password_overlay.success:
                    self.questions_answered += 1
                    self.correct_answers += 1
                    self.level_score += POINTS['quiz_correct']
                self.score_display.set_score(self.level_score)
                await asyncio.sleep(0.5)
                self.password_active = False
                self.password_overlay = None

        # Quiz input
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
