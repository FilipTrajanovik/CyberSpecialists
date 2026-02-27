# -*- coding: utf-8 -*-


import pygame
from constants import *


class Player:


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True

        # Health
        self.health = 3
        self.max_health = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = INVINCIBILITY_FRAMES

        # Collectibles
        self.coins_collected = 0
        self.shields_collected = 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def get_hitbox(self):

        margin = self.width * 0.1
        return pygame.Rect(
            int(self.x + margin),
            int(self.y + margin),
            int(self.width - margin * 2),
            int(self.height - margin * 2)
        )

    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        self.facing_right = False

    def move_right(self):
        self.vel_x = PLAYER_SPEED
        self.facing_right = True

    def stop_horizontal(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20

    def update(self, platforms):
        self.apply_gravity()

        self.x += self.vel_x
        self.y += self.vel_y

        self.on_ground = False
        player_rect = self.get_rect()

        for platform in platforms:
            platform.update_rect()
            if player_rect.colliderect(platform.rect):
                if self.vel_y > 0 and player_rect.bottom - 10 < platform.rect.top + self.vel_y:
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0 and player_rect.top + 10 > platform.rect.bottom:
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                elif self.vel_x > 0:
                    self.x = platform.rect.left - self.width
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.x = platform.rect.right
                    self.vel_x = 0

        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.vel_y = 0
            self.on_ground = True

        # Update invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def take_damage(self):
        if not self.invincible and self.health > 0:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            return True
        return False

    def collect_shield(self):
        """Collect shield powerup"""
        if self.health < self.max_health:
            self.health += 1
        self.shields_collected += 1

    def collect_coin(self):
        """Collect coin"""
        self.coins_collected += 1

    def draw(self, surface, camera_offset_x):
        """Draw player with camera offset"""
        screen_x = int(self.x - camera_offset_x)
        screen_y = int(self.y)

        # Flashing effect when invincible
        if self.invincible and (self.invincible_timer // 5) % 2 == 0:
            return

        # Shadow
        shadow_rect = pygame.Rect(screen_x + 5, screen_y + 5, self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Body
        body_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
        pygame.draw.rect(surface, PLAYER_COLOR, body_rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, body_rect, 3, border_radius=8)

        # Eyes
        eye_y = screen_y + 15
        if self.facing_right:
            eye1_x = screen_x + 30
            eye2_x = screen_x + 40
        else:
            eye1_x = screen_x + 10
            eye2_x = screen_x + 20

        pygame.draw.circle(surface, WHITE, (eye1_x, eye_y), 6)
        pygame.draw.circle(surface, BLACK, (eye1_x, eye_y), 3)
        pygame.draw.circle(surface, WHITE, (eye2_x, eye_y), 6)
        pygame.draw.circle(surface, BLACK, (eye2_x, eye_y), 3)

    def draw_ui(self, surface, font_small):
        """Draw health, coins, shields"""
        # Health hearts - FIXED SIZE
        heart_size = 30  # Larger hearts
        heart_y = 20
        for i in range(self.max_health):
            heart_x = 20 + i * 40  # More spacing
            if i < self.health:
                # Full heart
                pygame.draw.circle(surface, RED, (heart_x, heart_y), heart_size // 2)
                pygame.draw.circle(surface, RED, (heart_x + heart_size // 2, heart_y), heart_size // 2)
                points = [
                    (heart_x - heart_size // 2, heart_y),
                    (heart_x + heart_size, heart_y),
                    (heart_x + heart_size // 4, heart_y + heart_size)
                ]
                pygame.draw.polygon(surface, RED, points)
                # Border
                pygame.draw.circle(surface, WHITE, (heart_x, heart_y), heart_size // 2, 2)
                pygame.draw.circle(surface, WHITE, (heart_x + heart_size // 2, heart_y), heart_size // 2, 2)
            else:
                # Empty heart
                pygame.draw.circle(surface, DARK_GRAY, (heart_x, heart_y), heart_size // 2)
                pygame.draw.circle(surface, DARK_GRAY, (heart_x + heart_size // 2, heart_y), heart_size // 2)
                points = [
                    (heart_x - heart_size // 2, heart_y),
                    (heart_x + heart_size, heart_y),
                    (heart_x + heart_size // 4, heart_y + heart_size)
                ]
                pygame.draw.polygon(surface, DARK_GRAY, points)
                pygame.draw.circle(surface, WHITE, (heart_x, heart_y), heart_size // 2, 2)
                pygame.draw.circle(surface, WHITE, (heart_x + heart_size // 2, heart_y), heart_size // 2, 2)

        # Coins counter
        coin_box = pygame.Rect(20, 70, 150, 40)
        pygame.draw.rect(surface, GOLD, coin_box, border_radius=10)
        pygame.draw.rect(surface, WHITE, coin_box, 3, border_radius=10)
        coin_text = font_small.render(f"Coins: {self.coins_collected}", True, WHITE)
        surface.blit(coin_text, (30, 78))

        # Shields counter
        shield_box = pygame.Rect(20, 120, 150, 40)
        pygame.draw.rect(surface, CYAN, shield_box, border_radius=10)
        pygame.draw.rect(surface, WHITE, shield_box, 3, border_radius=10)
        shield_text = font_small.render(f"Shields: {self.shields_collected}", True, WHITE)
        surface.blit(shield_text, (30, 128))