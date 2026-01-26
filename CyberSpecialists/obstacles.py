"""
Obstacles, platforms, and collectibles - FIXED HITBOXES
"""

import pygame
import random
import math
from constants import *


class Platform:
    """Platform - exact hitbox matching visual"""

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.rect = pygame.Rect(int(x), int(y), int(width), int(self.height))
        self.color = PLATFORM_COLOR

    def update_rect(self):
        """Update rect to match position"""
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.rect.width = int(self.width)
        self.rect.height = int(self.height)

    def draw(self, surface, camera_offset_x):
        """Draw platform"""
        screen_x = int(self.x - camera_offset_x)

        # Shadow
        shadow_rect = pygame.Rect(screen_x + 3, self.rect.y + 3, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=10)

        # Main platform - draw at exact hitbox position
        draw_rect = pygame.Rect(screen_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, draw_rect, 3, border_radius=10)

        # Details
        for i in range(3):
            line_y = self.rect.y + 5 + i * 5
            if line_y < self.rect.y + self.rect.height - 5:
                pygame.draw.line(surface, LIGHT_GREEN,
                                 (screen_x + 5, line_y),
                                 (screen_x + self.rect.width - 5, line_y), 2)


class MovingPlatform(Platform):
    """Moving platform"""

    def __init__(self, x, y, width, start_x, end_x, speed=1):
        super().__init__(x, y, width)
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1
        self.color = CYAN

    def update(self):
        """Update position"""
        self.x += self.speed * self.direction

        if self.x >= self.end_x:
            self.direction = -1
            self.x = self.end_x
        elif self.x <= self.start_x:
            self.direction = 1
            self.x = self.start_x

        self.update_rect()


class Enemy:
    """Enemy obstacle - FIXED HITBOX"""

    def __init__(self, x, y, enemy_type='spike'):
        self.x = x
        self.y = y
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.type = enemy_type
        self.color = OBSTACLE_COLORS.get(enemy_type, RED)
        self.defeated = False
        self.quiz_shown = False
        self.animation_offset = 0

    def get_rect(self):
        """Get exact hitbox rectangle"""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def get_hitbox(self):
        """Get slightly smaller hitbox for player collision (more forgiving)"""
        margin = 5
        return pygame.Rect(
            int(self.x + margin),
            int(self.y + margin),
            self.width - margin * 2,
            self.height - margin * 2
        )

    def defeat(self):
        """Defeat enemy"""
        self.defeated = True

    def update(self):
        """Update animation"""
        if not self.defeated:
            self.animation_offset = (self.animation_offset + 1) % 60

    def draw(self, surface, camera_offset_x):
        """Draw enemy"""
        if self.defeated:
            return

        screen_x = int(self.x - camera_offset_x)
        screen_y = int(self.y)

        # Pulsing animation
        pulse = math.sin(self.animation_offset * 0.1) * 3

        # Shadow
        shadow_rect = pygame.Rect(screen_x + 3, screen_y + 3, self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Body - exact hitbox
        body_rect = pygame.Rect(
            screen_x + int(pulse),
            screen_y + int(pulse),
            self.width,
            self.height
        )
        pygame.draw.rect(surface, self.color, body_rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, body_rect, 3, border_radius=8)

        # Evil eyes
        eye_size = 5
        eye1_x = screen_x + 10 + int(pulse)
        eye2_x = screen_x + self.width - 10 + int(pulse)
        eye_y = screen_y + 12 + int(pulse)

        pygame.draw.circle(surface, WHITE, (eye1_x, eye_y), eye_size)
        pygame.draw.circle(surface, RED, (eye1_x, eye_y), eye_size - 2)
        pygame.draw.circle(surface, WHITE, (eye2_x, eye_y), eye_size)
        pygame.draw.circle(surface, RED, (eye2_x, eye_y), eye_size - 2)


class MovingEnemy(Enemy):
    """Moving enemy"""

    def __init__(self, x, y, enemy_type, start_x, end_x, speed=2):
        super().__init__(x, y, enemy_type)
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1

    def update(self):
        """Update position and animation"""
        super().update()

        if not self.defeated:
            self.x += self.speed * self.direction

            if self.x >= self.end_x:
                self.direction = -1
                self.x = self.end_x
            elif self.x <= self.start_x:
                self.direction = 1
                self.x = self.start_x


class Coin:
    """Collectible coin - FIXED HEIGHT"""

    def __init__(self, x, y):
        self.x = x
        self.y = y  # Now at proper reachable height
        self.radius = COIN_RADIUS
        self.collected = False
        self.quiz_shown = False
        self.animation_offset = 0

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def check_collection(self, player_rect):
        """Check if player collected this coin"""
        if self.collected:
            return False
        return player_rect.colliderect(self.get_rect())

    def update(self):
        """Update animation"""
        if not self.collected:
            self.animation_offset = (self.animation_offset + 1) % 60

    def draw(self, surface, camera_offset_x):
        """Draw coin"""
        if self.collected:
            return

        screen_x = int(self.x - camera_offset_x)

        # Floating animation
        float_offset = math.sin(self.animation_offset * 0.1) * 5
        draw_y = self.y + float_offset

        # Glow
        glow_radius = self.radius + 5
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 215, 0, 100), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, (screen_x - glow_radius, int(draw_y) - glow_radius))

        # Coin
        pygame.draw.circle(surface, GOLD, (screen_x, int(draw_y)), self.radius)
        pygame.draw.circle(surface, YELLOW, (screen_x, int(draw_y)), self.radius - 3)
        pygame.draw.circle(surface, WHITE, (screen_x, int(draw_y)), self.radius, 2)

        # Shine
        pygame.draw.circle(surface, WHITE, (screen_x - 3, int(draw_y) - 3), 4)


class Shield:
    """Shield powerup - FIXED HITBOX"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = SHIELD_SIZE
        self.collected = False
        self.animation_offset = 0

    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(
            int(self.x - self.size // 2),
            int(self.y - self.size // 2),
            self.size,
            self.size
        )

    def check_collection(self, player_rect):
        """Check if player collected this shield"""
        if self.collected:
            return False
        return player_rect.colliderect(self.get_rect())

    def update(self):
        """Update animation"""
        if not self.collected:
            self.animation_offset = (self.animation_offset + 1) % 60

    def draw(self, surface, camera_offset_x):
        """Draw shield"""
        if self.collected:
            return

        screen_x = int(self.x - camera_offset_x)

        # Rotation
        rotation = self.animation_offset * 3

        # Glow
        glow_size = self.size + 10
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 255, 255, 100), (glow_size, glow_size), glow_size)
        surface.blit(glow_surface, (screen_x - glow_size, self.y - glow_size))

        # Shield shape
        points = []
        for i in range(6):
            angle = math.radians(rotation + i * 60)
            px = screen_x + math.cos(angle) * self.size
            py = self.y + math.sin(angle) * self.size
            points.append((px, py))

        pygame.draw.polygon(surface, CYAN, points)
        pygame.draw.polygon(surface, WHITE, points, 3)

        # Center
        pygame.draw.circle(surface, WHITE, (screen_x, self.y), 5)


class Finish:
    """Finish line"""

    def __init__(self, x):
        self.x = x
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 100
        self.width = 80
        self.height = 100
        self.rect = pygame.Rect(int(x), int(self.y), self.width, self.height)
        self.animation_offset = 0

    def update(self):
        """Update animation"""
        self.animation_offset = (self.animation_offset + 1) % 60
        self.rect.x = int(self.x)

    def draw(self, surface, camera_offset_x):
        """Draw finish flag"""
        screen_x = int(self.x - camera_offset_x)

        # Glow
        glow = math.sin(self.animation_offset * 0.1) * 50

        # Pole
        pole_x = screen_x + 10
        pygame.draw.rect(surface, DARK_GRAY, (pole_x, self.y, 10, self.height))

        # Checkered flag
        flag_width = 60
        flag_height = 40
        square_size = 10

        for row in range(4):
            for col in range(6):
                if (row + col) % 2 == 0:
                    color = BLACK
                else:
                    color = WHITE

                square_x = screen_x + 20 + col * square_size
                square_y = self.y + 10 + row * square_size
                pygame.draw.rect(surface, color, (square_x, square_y, square_size, square_size))

        # Border
        border_color = (255, 255, int(100 + glow))
        pygame.draw.rect(surface, border_color,
                         (screen_x + 20, self.y + 10, flag_width, flag_height), 3, border_radius=5)

    def check_finish(self, player_rect):
        """Check if player reached finish"""
        return self.rect.colliderect(player_rect)


def generate_level_layout(level_num, difficulty, num_questions):
    """
    Generate level layout with platforms, enemies, coins, shields, and finish
    """
    platforms = []
    enemies = []
    coins = []
    shields = []

    # Ground platform
    ground = Platform(0, SCREEN_HEIGHT - GROUND_HEIGHT, 5000)
    platforms.append(ground)

    # Level length based on number of questions (each collectible triggers a question)
    items_needed = num_questions
    level_length = 200 + items_needed * 200  # Space out collectibles

    # Generate platforms
    num_platforms = 4 + level_num
    for i in range(num_platforms):
        x = 300 + i * (level_length / num_platforms) + random.randint(-50, 50)
        y = SCREEN_HEIGHT - 150 - random.randint(0, 200)
        width = random.randint(120, 200)

        if random.random() < 0.3:
            start_x = x
            end_x = x + random.randint(100, 150)
            platform = MovingPlatform(x, y, width, start_x, end_x, speed=1)
        else:
            platform = Platform(x, y, width)

        platforms.append(platform)

    # Distribute collectibles evenly to trigger questions
    # Split between coins (60%) and enemies (40%)
    num_coins = int(items_needed * 0.6)
    num_enemies = items_needed - num_coins

    # Place coins at reachable heights
    for i in range(num_coins):
        x = 400 + i * (level_length / num_coins) + random.randint(-50, 50)
        # FIXED: Coins at jump-reachable height
        y = SCREEN_HEIGHT - GROUND_HEIGHT - 80 - random.randint(0, 60)
        coins.append(Coin(x, y))

    # Place enemies on ground
    enemy_types = list(OBSTACLE_COLORS.keys())
    for i in range(num_enemies):
        x = 500 + i * (level_length / num_enemies) + random.randint(-100, 100)
        y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT - 5
        enemy_type = random.choice(enemy_types)

        if random.random() < 0.4:
            start_x = x
            end_x = x + random.randint(100, 200)
            enemy = MovingEnemy(x, y, enemy_type, start_x, end_x, speed=1)
        else:
            enemy = Enemy(x, y, enemy_type)

        enemies.append(enemy)

    # Place shields (bonus items, not required)
    num_shields = 2 + level_num
    for i in range(num_shields):
        x = 600 + i * (level_length / num_shields) + random.randint(-100, 100)
        y = SCREEN_HEIGHT - GROUND_HEIGHT - 100 - random.randint(0, 80)
        shields.append(Shield(x, y))

    # Finish line
    finish = Finish(level_length + 200)

    return platforms, enemies, coins, shields, finish