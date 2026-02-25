"""
Trophy Cabinet - Medal collection screen with wooden shelves
"""

import pygame
import random
import math
from constants import *
from ui import draw_gradient_background, draw_cute_button, draw_text_with_shadow


class TrophyCabinet:
    """Trophy cabinet showing medals on wooden shelves"""

    def __init__(self, fonts, lang_manager, db, user_id):
        self.fonts = fonts
        self.lang = lang_manager
        self.db = db
        self.user_id = user_id

        # Load medal images
        self.medal_images = {}
        for i in range(1, 6):
            try:
                img = pygame.image.load(f'creatives/level{i}-removebg-preview.png')
                img = pygame.transform.scale(img, (150, 150))
                self.medal_images[i] = img
            except:
                self.medal_images[i] = None

        # Get completion data from database
        self.completion_data = self._get_completion_data()

        # Animation
        self.glow_offset = 0

    def _get_completion_data(self):
        """Get how many times each level was completed"""
        completion_counts = {}

        cursor = self.db.conn.cursor()
        for level in range(1, 6):
            cursor.execute('''
                SELECT COUNT(*) FROM scores 
                WHERE user_id = ? AND level = ?
            ''', (self.user_id, level))
            count = cursor.fetchone()[0]
            completion_counts[level] = count

        return completion_counts

    def _draw_wooden_shelf(self, surface, x, y, width, height):
        """Draw a wooden shelf"""
        # Main shelf (brown wood color)
        shelf_rect = pygame.Rect(x, y, width, height)

        # Wood gradient
        for i in range(height):
            ratio = i / height
            color = (
                int(139 - ratio * 30),  # Brown
                int(90 - ratio * 20),
                int(43 - ratio * 10)
            )
            pygame.draw.line(surface, color, (x, y + i), (x + width, y + i))

        # Wood grain lines
        for i in range(3):
            grain_y = y + 5 + i * (height // 4)
            pygame.draw.line(surface, (120, 80, 40), (x + 10, grain_y), (x + width - 10, grain_y), 1)

        # Shelf edge (darker)
        pygame.draw.line(surface, (80, 50, 25), (x, y), (x + width, y), 3)
        pygame.draw.line(surface, (60, 40, 20), (x, y + height - 1), (x + width, y + height - 1), 2)

        # Nails/screws
        nail_positions = [x + 30, x + width - 30]
        for nail_x in nail_positions:
            pygame.draw.circle(surface, (60, 40, 20), (nail_x, y + height // 2), 4)
            pygame.draw.circle(surface, (40, 25, 10), (nail_x, y + height // 2), 2)

    def show(self, screen, clock):
        """Display trophy cabinet"""
        button_was_pressed = False

        while True:
            # Background
            draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

            # Title
            title_text = self.lang.get('trophy_cabinet')
            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 60,
                                  self.fonts['title'], GOLD, (80, 50, 20), 5)

            # Cabinet frame (dark wood)
            cabinet_rect = pygame.Rect(80, 140, SCREEN_WIDTH - 160, 530)

            # Cabinet background (darker wood)
            for i in range(cabinet_rect.height):
                ratio = i / cabinet_rect.height
                color = (
                    int(50 - ratio * 10),
                    int(35 - ratio * 5),
                    int(25 - ratio * 5)
                )
                pygame.draw.line(screen, color,
                                 (cabinet_rect.x, cabinet_rect.y + i),
                                 (cabinet_rect.right, cabinet_rect.y + i))

            # Cabinet frame border
            pygame.draw.rect(screen, (100, 65, 35), cabinet_rect, 8, border_radius=15)
            pygame.draw.rect(screen, (80, 50, 25), cabinet_rect, 4, border_radius=15)

            # Draw wooden shelves
            shelf_y_positions = [280, 450]  # Two shelves
            for shelf_y in shelf_y_positions:
                self._draw_wooden_shelf(screen, cabinet_rect.x + 20, shelf_y,
                                        cabinet_rect.width - 40, 25)

            # Medal positions - 3 on top shelf, 2 on bottom shelf
            medal_positions = [
                # Top shelf (levels 1, 2, 3)
                (SCREEN_WIDTH // 2 - 280, 200),
                (SCREEN_WIDTH // 2, 200),
                (SCREEN_WIDTH // 2 + 280, 200),
                # Bottom shelf (levels 4, 5)
                (SCREEN_WIDTH // 2 - 140, 370),
                (SCREEN_WIDTH // 2 + 140, 370),
            ]

            # Draw medals
            for level_num, (medal_x, medal_y) in enumerate(medal_positions, 1):
                completion_count = self.completion_data.get(level_num, 0)

                if completion_count > 0:
                    # Medal earned - NO GLOW, just show medal

                    # Medal image
                    if self.medal_images.get(level_num):
                        screen.blit(self.medal_images[level_num], (medal_x - 75, medal_y - 75))

                    # Completion count badge (PURPLE)
                    badge_y = medal_y + 85
                    badge_rect = pygame.Rect(medal_x - 40, badge_y, 80, 35)

                    # Badge background
                    pygame.draw.rect(screen, PURPLE, badge_rect, border_radius=17)
                    pygame.draw.rect(screen, GOLD, badge_rect, 3, border_radius=17)

                    # Count text
                    count_text = f"x{completion_count}"
                    count_surface = self.fonts['medium'].render(count_text, True, GOLD)
                    count_rect = count_surface.get_rect(center=badge_rect.center)
                    screen.blit(count_surface, count_rect)

                else:
                    # Medal not earned - show empty plaque
                    plaque_rect = pygame.Rect(medal_x - 80, medal_y - 80, 160, 160)

                    # Plaque (dark wood)
                    pygame.draw.rect(screen, (60, 40, 25), plaque_rect, border_radius=15)
                    pygame.draw.rect(screen, (40, 25, 15), plaque_rect, 4, border_radius=15)

                    # Lock icon
                    lock_y = medal_y - 30
                    # Lock body
                    pygame.draw.rect(screen, (80, 80, 80),
                                     (medal_x - 20, lock_y + 15, 40, 30), border_radius=5)
                    # Lock shackle
                    pygame.draw.arc(screen, (80, 80, 80),
                                    (medal_x - 25, lock_y - 10, 50, 40),
                                    0, 3.14159, 5)

                    # Locked text
                    lock_text = self.lang.get('locked')
                    lock_surface = self.fonts['tiny'].render(lock_text, True, (120, 120, 120))
                    lock_rect = lock_surface.get_rect(center=(medal_x, medal_y + 50))
                    screen.blit(lock_surface, lock_rect)

                # Level name label (small plaque below)
                label_y = medal_y + 130
                label_rect = pygame.Rect(medal_x - 90, label_y, 180, 30)

                # Wood plaque for name
                pygame.draw.rect(screen, (100, 65, 35), label_rect, border_radius=8)
                pygame.draw.rect(screen, (80, 50, 25), label_rect, 2, border_radius=8)

                # Level name
                level_name = f"{self.lang.get('level')} {level_num}"
                name_surface = self.fonts['tiny'].render(level_name, True, (220, 200, 150))
                name_rect = name_surface.get_rect(center=label_rect.center)
                screen.blit(name_surface, name_rect)

            # Total completions sign (wooden plaque at bottom)
            total_completions = sum(self.completion_data.values())
            total_plaque = pygame.Rect(SCREEN_WIDTH // 2 - 200, 600, 400, 50)

            # Draw wooden plaque
            for i in range(50):
                ratio = i / 50
                color = (
                    int(120 - ratio * 20),
                    int(80 - ratio * 15),
                    int(45 - ratio * 10)
                )
                pygame.draw.line(screen, color,
                                 (total_plaque.x, total_plaque.y + i),
                                 (total_plaque.right, total_plaque.y + i))

            pygame.draw.rect(screen, (80, 50, 25), total_plaque, 4, border_radius=12)

            # Total text
            total_text = f"{self.lang.get('total')} {total_completions} {self.lang.get('completions')}"
            total_surface = self.fonts['medium'].render(total_text, True, GOLD)
            total_rect = total_surface.get_rect(center=total_plaque.center)
            screen.blit(total_surface, total_rect)

            # Back button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, self.lang.get('back'), 450, 700, 300, 60,
                                RED, PINK, self.fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    pygame.time.wait(200)
                    pygame.event.clear()
                    return

            button_was_pressed = mouse_pressed
            self.glow_offset += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.wait(200)
                        pygame.event.clear()
                        return

            pygame.display.flip()
            clock.tick(FPS)


def show_level_complete_animation(screen, clock, fonts, lang_manager, level_num):
    """Show celebration animation when level is completed"""

    # Play medal winning sound
    try:
        medal_sound = pygame.mixer.Sound('creatives/medal-winning.wav')
        medal_sound.play()
    except:
        pass  # Sound file not found, continue without sound

    # Load medal image
    try:
        medal_image = pygame.image.load(f'creatives/level{level_num}-removebg-preview.png')
        medal_image = pygame.transform.scale(medal_image, (200, 200))
    except:
        medal_image = None

    # Confetti particles
    confetti = []
    for _ in range(CONFETTI_COUNT):
        confetti.append({
            'x': random.randint(0, SCREEN_WIDTH),
            'y': random.randint(-SCREEN_HEIGHT, 0),
            'vel_y': random.randint(2, 6),
            'vel_x': random.randint(-2, 2),
            'color': random.choice([RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, CYAN]),
            'size': random.randint(4, 8)
        })

    # Animation variables
    medal_scale = 0
    text_alpha = 0
    animation_time = 0
    max_animation_time = 180  # 3 seconds

    while animation_time < max_animation_time:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Update confetti
        for particle in confetti:
            particle['y'] += particle['vel_y']
            particle['x'] += particle['vel_x']

            # Draw confetti
            pygame.draw.circle(screen, particle['color'],
                               (int(particle['x']), int(particle['y'])),
                               particle['size'])

            # Reset if off screen
            if particle['y'] > SCREEN_HEIGHT:
                particle['y'] = -10
                particle['x'] = random.randint(0, SCREEN_WIDTH)

        # Animate medal (scale up)
        if animation_time < 60:
            medal_scale = animation_time / 60.0
        else:
            medal_scale = 1.0

        # Animate text (fade in)
        if animation_time > 30:
            text_alpha = min(255, (animation_time - 30) * 8)

        # Draw medal
        if medal_image and medal_scale > 0:
            scaled_size = int(200 * medal_scale)
            if scaled_size > 0:
                scaled_medal = pygame.transform.scale(medal_image, (scaled_size, scaled_size))
                medal_x = SCREEN_WIDTH // 2 - scaled_size // 2
                medal_y = SCREEN_HEIGHT // 2 - scaled_size // 2 - 50
                screen.blit(scaled_medal, (medal_x, medal_y))

                # Glow effect
                if medal_scale >= 1.0:
                    glow_size = int(20 * abs(math.sin(animation_time * 0.1)))
                    glow_rect = pygame.Rect(medal_x - glow_size, medal_y - glow_size,
                                            scaled_size + glow_size * 2, scaled_size + glow_size * 2)
                    pygame.draw.rect(screen, GOLD, glow_rect, 5, border_radius=20)

        # Draw congratulations text
        if text_alpha > 0:
            congrats_text = lang_manager.get('congratulations')
            complete_text = lang_manager.get('level_complete')

            congrats_surface = fonts['title'].render(congrats_text, True, GOLD)
            congrats_surface.set_alpha(text_alpha)
            congrats_rect = congrats_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(congrats_surface, congrats_rect)

            complete_surface = fonts['large'].render(complete_text, True, YELLOW)
            complete_surface.set_alpha(text_alpha)
            complete_rect = complete_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(complete_surface, complete_rect)

        # Check for skip
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Skip animation

        pygame.display.flip()
        clock.tick(FPS)
        animation_time += 1

    # Wait a bit before closing
    pygame.time.wait(1000)