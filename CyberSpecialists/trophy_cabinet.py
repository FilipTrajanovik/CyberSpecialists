"""
Trophy Cabinet - Medal collection screen with wooden shelves
"""
# -*- coding: utf-8 -*-

import pygame
import asyncio
import random
import math
from constants import *
from ui import draw_gradient_background, draw_cute_button, draw_text_with_shadow


class TrophyCabinet:
    """Displays user's medals on wooden shelves"""

    def __init__(self, fonts, lang_manager, db, user_id):
        self.fonts = fonts
        self.lang = lang_manager
        self.db = db
        self.user_id = user_id
        self.medals = self._load_user_medals()

    def _load_user_medals(self):
        """Load medal data from database"""
        medals_data = []
        try:
            # Get best scores for each level
            cursor = self.db.conn.cursor()
            for level_num in range(1, 6):
                cursor.execute("""
                    SELECT MAX(score), MAX(questions_correct) 
                    FROM scores 
                    WHERE user_id = ? AND level_id = ?
                """, (self.user_id, level_num))
                result = cursor.fetchone()

                if result and result[0] is not None:
                    medals_data.append({
                        'level': level_num,
                        'score': result[0],
                        'correct': result[1] or 0,
                        'unlocked': True
                    })
                else:
                    medals_data.append({
                        'level': level_num,
                        'unlocked': False
                    })
        except Exception as e:
            print(f"Error loading medals: {e}")

        return medals_data

    def draw_shelf(self, surface, y, level_data_pair):
        """Draw a wooden shelf with two levels"""
        # Shelf board
        shelf_rect = pygame.Rect(150, y, SCREEN_WIDTH - 300, 30)
        # Wooden color
        pygame.draw.rect(surface, (139, 69, 19), shelf_rect, border_radius=5)
        pygame.draw.rect(surface, (101, 67, 33), shelf_rect, 3, border_radius=5)

        # Draw two medal spots
        for i, level_data in enumerate(level_data_pair):
            if level_data is None: continue

            spot_x = 350 + i * 500
            
            # Level label
            level_text = f"{self.lang.get('level')} {level_data['level']}"
            draw_text_with_shadow(surface, level_text, spot_x, y + 60, 
                                 self.fonts['small'], WHITE)

            if level_data['unlocked']:
                # Draw medal
                medal_y = y - 60
                # Glow effect
                glow_size = int(40 + math.sin(pygame.time.get_ticks() * 0.005) * 5)
                pygame.draw.circle(surface, (255, 215, 0, 100), (spot_x, medal_y), glow_size)
                
                # Gold circle
                pygame.draw.circle(surface, GOLD, (spot_x, medal_y), 35)
                pygame.draw.circle(surface, YELLOW, (spot_x, medal_y), 30)
                
                # Ribbon
                ribbon_poly = [
                    (spot_x - 15, medal_y - 50),
                    (spot_x + 15, medal_y - 50),
                    (spot_x, medal_y)
                ]
                pygame.draw.polygon(surface, RED, ribbon_poly)
                
                # Level number on medal
                num_surf = self.fonts['medium'].render(str(level_data['level']), True, (100, 80, 0))
                num_rect = num_surf.get_rect(center=(spot_x, medal_y))
                surface.blit(num_surf, num_rect)
            else:
                # Locked spot
                medal_y = y - 60
                pygame.draw.circle(surface, (100, 100, 100), (spot_x, medal_y), 35)
                lock_text = self.fonts['medium'].render("🔒", True, (50, 50, 50))
                lock_rect = lock_text.get_rect(center=(spot_x, medal_y))
                surface.blit(lock_text, lock_rect)

    def show(self, screen, clock):
        """Main trophy cabinet loop"""
        button_was_pressed = False
        
        while True:
            draw_gradient_background(screen, (40, 20, 0), (80, 40, 20)) # Dark wood theme
            
            # Title
            draw_text_with_shadow(screen, self.lang.get('trophy_cabinet'), SCREEN_WIDTH // 2, 60,
                                 self.fonts['large'], GOLD, BLACK, 4)

            # Draw shelves
            # Shelf 1: Level 1 & 2
            self.draw_shelf(screen, 250, [self.medals[0], self.medals[1]])
            # Shelf 2: Level 3 & 4
            self.draw_shelf(screen, 450, [self.medals[2], self.medals[3]])
            # Shelf 3: Level 5
            self.draw_shelf(screen, 650, [self.medals[4], None])

            # Back button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, self.lang.get('back'), SCREEN_WIDTH // 2 - 150, 720, 300, 60,
                               RED, PINK, self.fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    pygame.time.wait(200)
                    pygame.event.clear()
                    return

            button_was_pressed = mouse_pressed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.flip()
            clock.tick(FPS)

    async def show_async(self, screen, clock):
        """Main trophy cabinet loop (async)"""
        button_was_pressed = False
        
        while True:
            draw_gradient_background(screen, (40, 20, 0), (80, 40, 20)) # Dark wood theme
            
            # Title
            draw_text_with_shadow(screen, self.lang.get('trophy_cabinet'), SCREEN_WIDTH // 2, 60,
                                 self.fonts['large'], GOLD, BLACK, 4)

            # Draw shelves
            # Shelf 1: Level 1 & 2
            self.draw_shelf(screen, 250, [self.medals[0], self.medals[1]])
            # Shelf 2: Level 3 & 4
            self.draw_shelf(screen, 450, [self.medals[2], self.medals[3]])
            # Shelf 3: Level 5
            self.draw_shelf(screen, 650, [self.medals[4], None])

            # Back button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, self.lang.get('back'), SCREEN_WIDTH // 2 - 150, 720, 300, 60,
                               RED, PINK, self.fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    await asyncio.sleep(0.2)
                    pygame.event.clear()
                    return

            button_was_pressed = mouse_pressed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)


def show_level_complete_animation(screen, clock, fonts, lang_manager, level_num):
    """Celebration animation when level is completed"""
    particles = []
    for _ in range(100):
        particles.append({
            'x': SCREEN_WIDTH // 2,
            'y': SCREEN_HEIGHT // 2,
            'vx': random.uniform(-10, 10),
            'vy': random.uniform(-15, 5),
            'color': random.choice([GOLD, YELLOW, WHITE, CYAN, PINK]),
            'life': random.randint(60, 120)
        })

    animation_time = 0
    while animation_time < 180: # 3 seconds
        draw_gradient_background(screen, DARK_BLUE, (0, 0, 20))
        
        # Draw and update particles
        for p in particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3 # gravity
            p['life'] -= 1
            if p['life'] > 0:
                pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 4)
            else:
                particles.remove(p)

        # Medal appears
        medal_scale = min(1.0, animation_time / 60)
        medal_size = int(150 * medal_scale)
        if medal_size > 0:
            spot_x = SCREEN_WIDTH // 2
            spot_y = SCREEN_HEIGHT // 2 - 50
            pygame.draw.circle(screen, GOLD, (spot_x, spot_y), medal_size // 2)
            pygame.draw.circle(screen, YELLOW, (spot_x, spot_y), medal_size // 2 - 10)
            
            text = fonts['large'].render(str(level_num), True, (100, 80, 0))
            text_rect = text.get_rect(center=(spot_x, spot_y))
            screen.blit(text, text_rect)

        # Text
        if animation_time > 60:
            draw_text_with_shadow(screen, lang_manager.get('level_complete'), 
                                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                                 fonts['title'], YELLOW, DARK_BLUE, 5)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return # Skip animation

        pygame.display.flip()
        clock.tick(FPS)
        animation_time += 1

    # Wait a bit before closing
    pygame.time.wait(1000)


async def show_level_complete_animation_async(screen, clock, fonts, lang_manager, level_num):
    """Celebration animation when level is completed (async)"""
    particles = []
    for _ in range(100):
        particles.append({
            'x': SCREEN_WIDTH // 2,
            'y': SCREEN_HEIGHT // 2,
            'vx': random.uniform(-10, 10),
            'vy': random.uniform(-15, 5),
            'color': random.choice([GOLD, YELLOW, WHITE, CYAN, PINK]),
            'life': random.randint(60, 120)
        })

    animation_time = 0
    while animation_time < 180: # 3 seconds
        draw_gradient_background(screen, DARK_BLUE, (0, 0, 20))
        
        # Draw and update particles
        for p in particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3 # gravity
            p['life'] -= 1
            if p['life'] > 0:
                pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 4)
            else:
                particles.remove(p)

        # Medal appears
        medal_scale = min(1.0, animation_time / 60)
        medal_size = int(150 * medal_scale)
        if medal_size > 0:
            spot_x = SCREEN_WIDTH // 2
            spot_y = SCREEN_HEIGHT // 2 - 50
            pygame.draw.circle(screen, GOLD, (spot_x, spot_y), medal_size // 2)
            pygame.draw.circle(screen, YELLOW, (spot_x, spot_y), medal_size // 2 - 10)
            
            text = fonts['large'].render(str(level_num), True, (100, 80, 0))
            text_rect = text.get_rect(center=(spot_x, spot_y))
            screen.blit(text, text_rect)

        # Text
        if animation_time > 60:
            draw_text_with_shadow(screen, lang_manager.get('level_complete'), 
                                 SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                                 fonts['title'], YELLOW, DARK_BLUE, 5)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return # Skip animation

        pygame.display.flip()
        clock.tick(FPS)
        animation_time += 1
        await asyncio.sleep(0)

    # Wait a bit before closing
    await asyncio.sleep(1)
