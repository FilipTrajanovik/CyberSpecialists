"""
Special Level Types - POLISHED VERSION
"""
# -*- coding: utf-8 -*-
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
    """Level 2: Parkour with obstacles at different heights - EASIER JUMPS"""

    def __init__(self, level_num, difficulty, fonts, lang_manager=None):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager

        self.player = Player(100, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT - 10)
        self.camera = Camera()

        # Quiz setup
        num_questions = QUESTIONS_PER_LEVEL.get(difficulty, 7)
        self.quiz_questions = get_randomized_questions(level_num, num_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
        self.total_questions = len(self.quiz_questions)
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # Coin counter for triggering quizzes (every 2-3 coins)
        self.coins_collected = 0
        self.coins_needed_for_quiz = 2  # Will trigger quiz every 2-3 coins

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

        # Generate parkour obstacles
        self.obstacles = []
        self.coins = []
        self.level_width = 0
        self._generate_parkour_level()

    def _generate_parkour_level(self):
        """Generate parkour obstacles with coins at REACHABLE heights"""
        obstacle_count = self.total_questions
        spacing = 300  # More spacing between platforms

        # Ground platform
        self.level_width = spacing * obstacle_count + 500
        ground = Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, self.level_width)
        self.obstacles.append(ground)

        for i in range(obstacle_count):
            x = 400 + i * spacing

            # EASIER heights - player can jump ~250 pixels
            height_from_ground = random.randint(80, 220)  # Much lower!
            height = SCREEN_HEIGHT - GROUND_HEIGHT - height_from_ground
            width = random.randint(120, 200)  # Wider platforms

            # Create platform obstacle
            platform = Platform(x, height, width)
            self.obstacles.append(platform)

            # Put coin on top of platform
            coin_x = x + width // 2
            coin_y = height - 40
            coin = Coin(coin_x, coin_y)
            self.coins.append(coin)

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
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

        # Update player with collision
        old_y = self.player.y
        self.player.update(self.obstacles)

        # BOUNCE DOWN if hitting obstacle from below
        if self.player.vel_y < 0:  # Moving upward
            for obstacle in self.obstacles:
                if obstacle.rect.colliderect(self.player.get_rect()):
                    # Hit from below - bounce down
                    if old_y + self.player.height <= obstacle.rect.top + 10:
                        self.player.y = obstacle.rect.bottom
                        self.player.vel_y = 5  # Bounce down

        # RIGHT BORDER - stop at level end
        if self.player.x > self.level_width - PLAYER_WIDTH:
            self.player.x = self.level_width - PLAYER_WIDTH
            self.player.vel_x = 0

        self.camera.update(self.player.x)

        # Update coins
        for coin in self.coins:
            coin.update()
            if coin.check_collection(self.player.get_rect()):
                coin.collected = True
                self.player.collect_coin()
                self.level_score += POINTS['coin']
                self.score_display.set_score(self.level_score)

                # Show quiz
                if not coin.quiz_shown and self.current_quiz_index < len(self.quiz_questions):
                    coin.quiz_shown = True
                    self.current_quiz = QuizOverlay(
                        self.quiz_questions[self.current_quiz_index],
                        self.fonts
                    )
                    self.current_quiz_index += 1
                    self.quiz_active = True

        # Check completion
        if self.questions_answered >= self.total_questions:
            self.completed = True
            self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        if self.player.health <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything"""
        draw_gradient_background(surface, GRADIENTS['level2'][0], GRADIENTS['level2'][1])

        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(surface, GREEN, ground_rect)
        pygame.draw.rect(surface, DARK_BLUE, ground_rect, 3)

        # Obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface, self.camera.offset_x)

        # Coins
        for coin in self.coins:
            coin.draw(surface, self.camera.offset_x)

        # Player
        self.player.draw(surface, self.camera.offset_x)

        # UI
        self.player.draw_ui(surface, self.fonts['small'])
        self.timer.draw(surface, self.fonts['medium'])
        self.score_display.draw(surface)

        # Progress

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
                pygame.time.wait(500)
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


class MazeLevel:
    """Level 3: Navigate maze like the image - smaller and simpler"""

    def __init__(self, level_num, difficulty, fonts, lang_manager=None):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager

        self.player = Player(120, SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT - 10)
        self.camera_offset = 0  # No camera - maze fits on screen

        # Quiz setup
        num_questions = QUESTIONS_PER_LEVEL.get(difficulty, 7)
        self.quiz_questions = get_randomized_questions(level_num, num_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
        self.total_questions = len(self.quiz_questions)
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # Coin counter for triggering quizzes (every 2-3 coins)
        self.coins_collected = 0
        self.coins_needed_for_quiz = 2  # Will trigger quiz every 2-3 coins

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

        # Generate maze
        self.walls = []
        self.coins = []
        self.exit_rect = None
        self._generate_maze()

    def _generate_maze(self):
        """Generate simple maze that fits on screen"""
        # Maze dimensions - fits on screen!
        maze_left = 100
        maze_top = 150
        maze_width = 1000
        maze_height = 550

        # Outer walls
        wall_thickness = 15

        # Top wall
        self.walls.append(pygame.Rect(maze_left, maze_top, maze_width, wall_thickness))
        # Bottom wall
        self.walls.append(pygame.Rect(maze_left, maze_top + maze_height - wall_thickness, maze_width, wall_thickness))
        # Left wall (with entrance gap)
        self.walls.append(pygame.Rect(maze_left, maze_top, wall_thickness, 200))
        self.walls.append(pygame.Rect(maze_left, maze_top + 280, wall_thickness, maze_height - 280))
        # Right wall (with exit gap)
        self.walls.append(pygame.Rect(maze_left + maze_width - wall_thickness, maze_top, wall_thickness, 200))
        self.walls.append(
            pygame.Rect(maze_left + maze_width - wall_thickness, maze_top + 280, wall_thickness, maze_height - 280))

        # Internal maze walls - create paths
        # Vertical walls
        for i in range(5):
            x = maze_left + 150 + i * 180
            if i % 2 == 0:
                # Wall from top
                self.walls.append(pygame.Rect(x, maze_top + 100, wall_thickness, 250))
            else:
                # Wall from bottom
                self.walls.append(pygame.Rect(x, maze_top + 350, wall_thickness, 200))

        # Horizontal walls
        for i in range(3):
            y = maze_top + 150 + i * 150
            if i % 2 == 0:
                self.walls.append(pygame.Rect(maze_left + 200, y, 300, wall_thickness))
            else:
                self.walls.append(pygame.Rect(maze_left + 550, y, 300, wall_thickness))

        # Place coins in accessible areas
        coin_positions = [
            (300, 300), (500, 250), (700, 400),
            (400, 500), (800, 300), (600, 550),
            (350, 600)
        ]

        for i in range(min(self.total_questions, len(coin_positions))):
            coin_x, coin_y = coin_positions[i]
            self.coins.append(Coin(coin_x, coin_y))

        # Exit at top right
        self.exit_rect = pygame.Rect(maze_left + maze_width - 100, maze_top + 220, 80, 60)

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
            return

        # Player movement
        keys = pygame.key.get_pressed()
        old_x = self.player.x
        old_y = self.player.y

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += PLAYER_SPEED

        # Wall collision
        player_rect = self.player.get_rect()
        for wall in self.walls:
            if player_rect.colliderect(wall):
                self.player.x = old_x
                self.player.y = old_y
                break

        # Update coins
        for coin in self.coins:
            coin.update()
            if coin.check_collection(self.player.get_rect()):
                coin.collected = True
                self.player.collect_coin()
                self.level_score += POINTS['coin']
                self.score_display.set_score(self.level_score)

                # Show quiz
                if not coin.quiz_shown and self.current_quiz_index < len(self.quiz_questions):
                    coin.quiz_shown = True
                    self.current_quiz = QuizOverlay(
                        self.quiz_questions[self.current_quiz_index],
                        self.fonts
                    )
                    self.current_quiz_index += 1
                    self.quiz_active = True

        # Check completion - all coins collected AND reached exit
        if self.questions_answered >= self.total_questions:
            if self.exit_rect.colliderect(self.player.get_rect()):
                self.completed = True
                self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything"""
        draw_gradient_background(surface, GRADIENTS['level3'][0], GRADIENTS['level3'][1])

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(surface, DARK_GRAY, wall)
            pygame.draw.rect(surface, WHITE, wall, 2)

        # Draw coins
        for coin in self.coins:
            if not coin.collected:
                coin.draw(surface, 0)  # No camera offset

        # Draw exit
        if self.questions_answered >= self.total_questions:
            pygame.draw.rect(surface, GOLD, self.exit_rect, border_radius=10)
            exit_text = self.fonts['large'].render("EXIT", True, BLACK)
            exit_text_rect = exit_text.get_rect(center=self.exit_rect.center)
            surface.blit(exit_text, exit_text_rect)
        else:
            pygame.draw.rect(surface, LIGHT_GRAY, self.exit_rect, border_radius=10)
            lock_text = self.fonts['medium'].render("LOCKED", True, RED)
            lock_rect = lock_text.get_rect(center=self.exit_rect.center)
            surface.blit(lock_text, lock_rect)

        # Draw player
        player_screen_rect = self.player.get_rect()
        pygame.draw.rect(surface, PLAYER_COLOR, player_screen_rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, player_screen_rect, 3, border_radius=8)

        # UI
        self.player.draw_ui(surface, self.fonts['small'])
        self.timer.draw(surface, self.fonts['medium'])
        self.score_display.draw(surface)

        # Progress

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
                pygame.time.wait(500)
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


class SpaceshipLevel:
    """Level 4: Spaceship avoiding projectiles and collecting coins"""

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

        # Load images
        try:
            self.spaceship_img = pygame.image.load('creatives/spaceship-photo-removebg-preview.png')
            self.spaceship_img = pygame.transform.scale(self.spaceship_img, (80, 60))  # Scaled size
        except:
            self.spaceship_img = None

        try:
            self.asteroid_img = pygame.image.load('creatives/asteroid-photo-removebg-preview.png')
            self.asteroid_img = pygame.transform.scale(self.asteroid_img, (50, 50))  # Fixed size for asteroids
        except:
            self.asteroid_img = None

        try:
            self.coin_img = pygame.image.load('creatives/coin-photo-removebg-preview.png')
            self.coin_img = pygame.transform.scale(self.coin_img, (40, 40))  # Coin size
        except:
            self.coin_img = None

        # Spaceship position (moves vertically only)
        self.ship_x = 150
        self.ship_y = SCREEN_HEIGHT // 2
        self.ship_width = 80  # Match scaled image
        self.ship_height = 60  # Match scaled image
        self.ship_vel_y = 0
        self.ship_speed = 8

        # Asteroid size (fixed)
        self.asteroid_size = 35

        # Generate stars for background
        self.stars = []
        for _ in range(150):  # 150 stars
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT)
            star_size = random.choice([1, 2, 2, 3])  # Most stars are small
            self.stars.append({'x': star_x, 'y': star_y, 'size': star_size})

        # Quiz setup
        num_questions = QUESTIONS_PER_LEVEL.get(difficulty, 7)
        self.quiz_questions = get_randomized_questions(level_num, num_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
        self.total_questions = len(self.quiz_questions)
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # Coin counter for triggering quizzes (every 2-3 coins)
        self.coins_collected = 0
        self.coins_needed_for_quiz = 2  # Will trigger quiz every 2-3 coins

        # State
        self.paused = False
        self.completed = False
        self.game_over = False
        self.questions_answered = 0
        self.correct_answers = 0
        self.level_score = 0
        self.health = 3

        # Projectiles and coins
        self.projectiles = []
        self.coins = []
        self.scroll_speed = 5
        self.distance_traveled = 0
        self.spawn_timer = 0

        # Timer and UI
        time_limit = LEVEL_TIME_LIMITS.get(difficulty, 480)
        self.timer = Timer(time_limit)
        self.score_display = ScoreDisplay(SCREEN_WIDTH - 220, 20, fonts['small'])

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
            return

        # Ship movement (vertical only)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.ship_vel_y = -self.ship_speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.ship_vel_y = self.ship_speed
        else:
            self.ship_vel_y = 0

        self.ship_y += self.ship_vel_y

        # Keep ship in bounds
        if self.ship_y < 0:
            self.ship_y = 0
        if self.ship_y > SCREEN_HEIGHT - self.ship_height:
            self.ship_y = SCREEN_HEIGHT - self.ship_height

        # Spawn projectiles and coins
        self.spawn_timer += 1
        if self.spawn_timer > 40:  # Every ~0.7 seconds
            self.spawn_timer = 0

            # Spawn projectile (asteroid)
            proj_y = random.randint(50, SCREEN_HEIGHT - 100)
            self.projectiles.append({
                'x': SCREEN_WIDTH,
                'y': proj_y,
                'size': self.asteroid_size  # Fixed size 50
            })

            # Sometimes spawn coin
            if random.random() < 0.4:
                coin_y = random.randint(50, SCREEN_HEIGHT - 100)
                coin = Coin(SCREEN_WIDTH, coin_y)
                self.coins.append(coin)

        # Update projectiles
        for proj in self.projectiles[:]:
            proj['x'] -= self.scroll_speed

            # Remove off-screen
            if proj['x'] < -50:
                self.projectiles.remove(proj)

            # Check collision with ship
            ship_rect = pygame.Rect(self.ship_x, self.ship_y, self.ship_width, self.ship_height)
            proj_rect = pygame.Rect(proj['x'], proj['y'], proj['size'], proj['size'])
            if ship_rect.colliderect(proj_rect):
                self.health -= 1
                self.projectiles.remove(proj)

        # Update coins
        for coin in self.coins[:]:
            coin.x -= self.scroll_speed
            coin.update()

            # Remove off-screen
            if coin.x < -50:
                self.coins.remove(coin)

            # Check collection
            ship_rect = pygame.Rect(self.ship_x, self.ship_y, self.ship_width, self.ship_height)
            if coin.check_collection(ship_rect):
                coin.collected = True
                self.coins.remove(coin)
                self.level_score += POINTS['coin']
                self.score_display.set_score(self.level_score)
                self.coins_collected += 1
                # Play coin sound
                if self.coin_sound:
                    self.coin_sound.play()

                # Show quiz every 2-3 coins
                if self.coins_collected >= self.coins_needed_for_quiz:
                    if self.current_quiz_index < len(self.quiz_questions):
                        self.current_quiz = QuizOverlay(
                            self.quiz_questions[self.current_quiz_index],
                            self.fonts
                        )
                        self.current_quiz_index += 1
                        self.quiz_active = True
                        self.coins_collected = 0
                        # Randomize next requirement
                        self.coins_needed_for_quiz = random.randint(2, 3)

        # Track distance
        self.distance_traveled += self.scroll_speed

        # Check completion
        if self.questions_answered >= self.total_questions:
            self.completed = True
            self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        if self.health <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything with images and starry space background"""
        # Black space background
        surface.fill(BLACK)

        # Draw stars
        for star in self.stars:
            pygame.draw.circle(surface, WHITE, (int(star['x']), int(star['y'])), star['size'])

        # Draw spaceship (with image or fallback)
        if self.spaceship_img:
            surface.blit(self.spaceship_img, (self.ship_x, self.ship_y))
        else:
            # Fallback drawing
            pygame.draw.rect(surface, CYAN, (self.ship_x, self.ship_y, self.ship_width, self.ship_height),
                             border_radius=8)
            pygame.draw.polygon(surface, WHITE, [
                (self.ship_x + self.ship_width, self.ship_y + self.ship_height // 2),
                (self.ship_x + self.ship_width + 15, self.ship_y + self.ship_height // 2 - 10),
                (self.ship_x + self.ship_width + 15, self.ship_y + self.ship_height // 2 + 10)
            ])

        # Draw projectiles (asteroids with image or fallback)
        for proj in self.projectiles:
            if self.asteroid_img:
                # Center the image on the projectile position
                img_x = int(proj['x'] - self.asteroid_size // 2)
                img_y = int(proj['y'] - self.asteroid_size // 2)
                surface.blit(self.asteroid_img, (img_x, img_y))
            else:
                # Fallback drawing
                pygame.draw.circle(surface, RED, (int(proj['x']), int(proj['y'])), proj['size'] // 2)
                pygame.draw.circle(surface, ORANGE, (int(proj['x']), int(proj['y'])), proj['size'] // 2 - 5)

        # Draw coins (with image or fallback)
        for coin in self.coins:
            if self.coin_img:
                # Draw coin image
                coin_x = int(coin.x - 20)
                coin_y = int(coin.y - 20)
                surface.blit(self.coin_img, (coin_x, coin_y))
            else:
                # Fallback to default coin drawing
                coin.draw(surface, 0)

        # Health (hearts)
        for i in range(self.health):
            heart_x = 20 + i * 40
            heart_y = 20
            pygame.draw.circle(surface, RED, (heart_x, heart_y), 15)
            pygame.draw.circle(surface, RED, (heart_x + 15, heart_y), 15)
            pygame.draw.polygon(surface, RED, [
                (heart_x - 15, heart_y),
                (heart_x + 30, heart_y),
                (heart_x + 7, heart_y + 30)
            ])

        # UI
        self.timer.draw(surface, self.fonts['medium'])
        self.score_display.draw(surface)

        # Progress

        # Distance
        distance_text = f"Distance: {self.distance_traveled // 10}m"
        distance_surface = self.fonts['small'].render(distance_text, True, WHITE)
        surface.blit(distance_surface, (20, 100))

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
                pygame.time.wait(500)
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


class MemoryCardLevel:
    """Level 5: Memory card matching game - Using SHAPES instead of emojis"""

    def __init__(self, level_num, difficulty, fonts, lang_manager=None):
        self.level_num = level_num
        self.difficulty = difficulty
        self.fonts = fonts
        self.lang = lang_manager

        # Load coin/match sound
        try:
            self.coin_sound = pygame.mixer.Sound('coincollect.ogg')
            self.coin_sound.set_volume(0.5)
        except:
            self.coin_sound = None

        # Load card back image
        try:
            self.card_back_img = pygame.image.load('creatives/questions-memory.png')
        except:
            self.card_back_img = None

        # Quiz setup
        num_questions = QUESTIONS_PER_LEVEL.get(difficulty, 7)
        self.quiz_questions = get_randomized_questions(level_num, num_questions,
                                                       self.lang.get_lang_code() if self.lang else "mk")
        self.total_questions = len(self.quiz_questions)
        self.current_quiz_index = 0
        self.current_quiz = None
        self.quiz_active = False

        # Memory cards
        self.cards = []
        self.flipped_cards = []
        self.matched_cards = []
        self._generate_cards()

        # State
        self.paused = False
        self.completed = False
        self.game_over = False
        self.questions_answered = 0
        self.correct_answers = 0
        self.level_score = 0
        self.flip_timer = 0

        # Timer and UI
        time_limit = LEVEL_TIME_LIMITS.get(difficulty, 480)
        self.timer = Timer(time_limit)
        self.score_display = ScoreDisplay(SCREEN_WIDTH - 220, 20, fonts['small'])

    def _generate_cards(self):
        """Generate 18 memory cards (9 pairs) - only 7 pairs trigger questions"""
        # Define shapes - need 9 different shapes
        shapes = [
            'circle', 'square', 'triangle', 'star',
            'diamond', 'hexagon', 'heart', 'cross', 'pentagon'
        ]

        # Create 9 pairs (18 cards total)
        card_values = shapes[:9]
        card_pairs = card_values + card_values
        random.shuffle(card_pairs)

        # Mark which pairs will trigger questions (7 out of 9)
        self.question_pairs = set(random.sample(card_values, self.total_questions))

        # Position cards in grid - 6 columns x 3 rows
        cols = 6
        rows = 3
        card_width = 120  # Bigger
        card_height = 150  # Bigger
        spacing = 20  # More spacing
        start_x = (SCREEN_WIDTH - (cols * (card_width + spacing))) // 2
        start_y = 180  # More centered vertically

        for i, value in enumerate(card_pairs):
            row = i // cols
            col = i % cols
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)

            self.cards.append({
                'value': value,
                'x': x,
                'y': y,
                'width': card_width,
                'height': card_height,
                'flipped': False,
                'matched': False
            })

    def _draw_shape(self, surface, shape, rect, color):
        """Draw different shapes"""
        center_x = rect.centerx
        center_y = rect.centery
        size = 40  # Bigger for 120x150 cards

        if shape == 'circle':
            pygame.draw.circle(surface, color, (center_x, center_y), size)
        elif shape == 'square':
            square_rect = pygame.Rect(center_x - size, center_y - size, size * 2, size * 2)
            pygame.draw.rect(surface, color, square_rect)
        elif shape == 'triangle':
            points = [
                (center_x, center_y - size),
                (center_x - size, center_y + size),
                (center_x + size, center_y + size)
            ]
            pygame.draw.polygon(surface, color, points)
        elif shape == 'star':
            # 5-pointed star
            points = []
            for i in range(10):
                angle = (i * 36 - 90) * 3.14159 / 180
                r = size if i % 2 == 0 else size // 2
                points.append((center_x + r * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
                               center_y + r * pygame.math.Vector2(1, 0).rotate_rad(angle).y))
            pygame.draw.polygon(surface, color, points)
        elif shape == 'diamond':
            points = [
                (center_x, center_y - size),
                (center_x + size, center_y),
                (center_x, center_y + size),
                (center_x - size, center_y)
            ]
            pygame.draw.polygon(surface, color, points)
        elif shape == 'hexagon':
            points = []
            for i in range(6):
                angle = (i * 60 - 30) * 3.14159 / 180
                points.append((center_x + size * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
                               center_y + size * pygame.math.Vector2(1, 0).rotate_rad(angle).y))
            pygame.draw.polygon(surface, color, points)
        elif shape == 'pentagon':
            # 5-sided pentagon
            points = []
            for i in range(5):
                angle = (i * 72 - 90) * 3.14159 / 180
                points.append((center_x + size * pygame.math.Vector2(1, 0).rotate_rad(angle).x,
                               center_y + size * pygame.math.Vector2(1, 0).rotate_rad(angle).y))
            pygame.draw.polygon(surface, color, points)
        elif shape == 'heart':
            pygame.draw.circle(surface, color, (center_x - size // 2, center_y - size // 4), size // 2)
            pygame.draw.circle(surface, color, (center_x + size // 2, center_y - size // 4), size // 2)
            pygame.draw.polygon(surface, color, [
                (center_x - size, center_y - size // 4),
                (center_x + size, center_y - size // 4),
                (center_x, center_y + size)
            ])
        elif shape == 'cross':
            thickness = size // 3
            # Vertical
            pygame.draw.rect(surface, color, (center_x - thickness // 2, center_y - size, thickness, size * 2))
            # Horizontal
            pygame.draw.rect(surface, color, (center_x - size, center_y - thickness // 2, size * 2, thickness))

    def update(self):
        """Update game state"""
        if self.paused or self.quiz_active:
            return

        # Handle flip timer
        if self.flip_timer > 0:
            self.flip_timer -= 1
            if self.flip_timer == 0:
                # Check if match
                if len(self.flipped_cards) == 2:
                    card1, card2 = self.flipped_cards
                    if card1['value'] == card2['value']:
                        # Match!
                        card1['matched'] = True
                        card2['matched'] = True
                        self.matched_cards.extend([card1, card2])
                        self.level_score += POINTS['coin']
                        self.score_display.set_score(self.level_score)
                        # Play match sound
                        if self.coin_sound:
                            self.coin_sound.play()

                        # Show quiz ONLY if this pair triggers a question
                        if (card1['value'] in self.question_pairs and
                                self.current_quiz_index < len(self.quiz_questions)):
                            self.current_quiz = QuizOverlay(
                                self.quiz_questions[self.current_quiz_index],
                                self.fonts
                            )
                            self.current_quiz_index += 1
                            self.quiz_active = True
                    else:
                        # No match - flip back
                        card1['flipped'] = False
                        card2['flipped'] = False

                    self.flipped_cards = []

        # Check completion
        if len(self.matched_cards) == len(self.cards):
            self.completed = True
            self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        self.score_display.update()

    async def update_async(self):
        """Update game state (async)"""
        if self.paused or self.quiz_active:
            return

        # Handle flip timer
        if self.flip_timer > 0:
            self.flip_timer -= 1
            if self.flip_timer == 0:
                # Check if match
                if len(self.flipped_cards) == 2:
                    card1, card2 = self.flipped_cards
                    if card1['value'] == card2['value']:
                        # Match!
                        card1['matched'] = True
                        card2['matched'] = True
                        self.matched_cards.extend([card1, card2])
                        self.level_score += POINTS['coin']
                        self.score_display.set_score(self.level_score)
                        # Play match sound
                        if self.coin_sound:
                            self.coin_sound.play()

                        # Show quiz ONLY if this pair triggers a question
                        if (card1['value'] in self.question_pairs and
                                self.current_quiz_index < len(self.quiz_questions)):
                            self.current_quiz = QuizOverlay(
                                self.quiz_questions[self.current_quiz_index],
                                self.fonts
                            )
                            self.current_quiz_index += 1
                            self.quiz_active = True
                    else:
                        # No match - flip back
                        card1['flipped'] = False
                        card2['flipped'] = False

                    self.flipped_cards = []

        # Check completion
        if len(self.matched_cards) == len(self.cards):
            self.completed = True
            self.level_score += POINTS['level_complete']

        self.timer.update()
        if self.timer.time_left <= 0:
            self.game_over = True

        self.score_display.update()

    def draw(self, surface):
        """Draw everything"""
        draw_gradient_background(surface, GRADIENTS['level5'][0], GRADIENTS['level5'][1])

        # Draw cards
        for card in self.cards:
            card_rect = pygame.Rect(card['x'], card['y'], card['width'], card['height'])

            if card['matched']:
                # Matched - show green
                pygame.draw.rect(surface, GREEN, card_rect, border_radius=10)
                self._draw_shape(surface, card['value'], card_rect, DARK_BLUE)
            elif card['flipped']:
                # Flipped - show shape
                pygame.draw.rect(surface, WHITE, card_rect, border_radius=10)
                self._draw_shape(surface, card['value'], card_rect, PURPLE)
            else:
                # Face down - show image or fallback
                if self.card_back_img:
                    # Scale image SMALLER than card size
                    padding = 10  # Add padding to make image smaller
                    img_width = card['width'] - (padding * 2)
                    img_height = card['height'] - (padding * 2)
                    scaled_img = pygame.transform.scale(self.card_back_img, (img_width, img_height))
                    surface.blit(scaled_img, (card['x'] + padding, card['y'] + padding))
                    # Border
                    pygame.draw.rect(surface, YELLOW, card_rect, 4, border_radius=10)
                else:
                    # Fallback - blue card with ?
                    pygame.draw.rect(surface, BLUE, card_rect, border_radius=10)
                    pygame.draw.rect(surface, YELLOW, card_rect, 4, border_radius=10)
                    question_mark = self.fonts['large'].render('?', True, WHITE)
                    q_rect = question_mark.get_rect(center=card_rect.center)
                    surface.blit(question_mark, q_rect)

        # UI
        self.timer.draw(surface, self.fonts['medium'])
        self.score_display.draw(surface)

        # Progress
        matches = len(self.matched_cards) // 2
        total_pairs = len(self.cards) // 2

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
                pygame.time.wait(500)
                self.quiz_active = False
                self.current_quiz = None

        # Card clicking
        if not self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN and self.flip_timer == 0:
            if len(self.flipped_cards) < 2:
                mouse_pos = pygame.mouse.get_pos()
                for card in self.cards:
                    card_rect = pygame.Rect(card['x'], card['y'], card['width'], card['height'])
                    if card_rect.collidepoint(mouse_pos):
                        if not card['flipped'] and not card['matched']:
                            card['flipped'] = True
                            self.flipped_cards.append(card)

                            if len(self.flipped_cards) == 2:
                                self.flip_timer = 60  # 1 second delay
                            break

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

        # Card clicking
        if not self.quiz_active and event.type == pygame.MOUSEBUTTONDOWN and self.flip_timer == 0:
            if len(self.flipped_cards) < 2:
                mouse_pos = pygame.mouse.get_pos()
                for card in self.cards:
                    card_rect = pygame.Rect(card['x'], card['y'], card['width'], card['height'])
                    if card_rect.collidepoint(mouse_pos):
                        if not card['flipped'] and not card['matched']:
                            card['flipped'] = True
                            self.flipped_cards.append(card)

                            if len(self.flipped_cards) == 2:
                                self.flip_timer = 60  # 1 second delay
                            break

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

            await self.update_async()
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
