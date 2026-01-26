"""
Story screens with scrollable text - LANGUAGE SUPPORT
"""

import pygame
from constants import *
from ui import draw_gradient_background, draw_cute_button


class StoryScreen:
    """Story screen with scrollable text"""

    def __init__(self, level_num, font_large, font_medium, font_small, font_tiny, lang_manager):
        self.level_num = level_num
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.font_tiny = font_tiny
        self.lang = lang_manager
        self.scroll_offset = 0
        self.max_scroll = 0

    def show(self, screen, clock):
        """Show story screen with scrolling"""
        from game_data import get_story

        story_data = get_story(self.level_num, self.lang.get_lang_code())
        if not story_data:
            return

        button_was_pressed = False

        # Prepare story text lines
        box_width = 1100
        text_margin = 50
        max_width = box_width - (text_margin * 2)

        # Create all text surfaces
        lines = []

        # Title
        title_surface = self.font_large.render(story_data['title'], True, PURPLE)
        lines.append({'surface': title_surface, 'y_offset': 0, 'type': 'title'})
        current_y = 80

        # Story paragraphs
        for paragraph in story_data['story']:
            words = paragraph.split()
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.font_small.render(test_line, True, BLACK)

                if test_surface.get_width() <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        line_surface = self.font_small.render(' '.join(current_line), True, BLACK)
                        lines.append({'surface': line_surface, 'y_offset': current_y, 'type': 'text'})
                        current_y += 35
                    current_line = [word]

            if current_line:
                line_surface = self.font_small.render(' '.join(current_line), True, BLACK)
                lines.append({'surface': line_surface, 'y_offset': current_y, 'type': 'text'})
                current_y += 35

            current_y += 20  # Extra space between paragraphs

        # Lesson at the end
        if 'lesson' in story_data:
            current_y += 20
            lesson_label = self.font_medium.render(self.lang.get('what_learned'), True, ORANGE)
            lines.append({'surface': lesson_label, 'y_offset': current_y, 'type': 'lesson_label'})
            current_y += 50

            lesson_words = story_data['lesson'].split()
            lesson_line = []

            for word in lesson_words:
                test_line = ' '.join(lesson_line + [word])
                test_surface = self.font_small.render(test_line, True, BLACK)

                if test_surface.get_width() <= max_width:
                    lesson_line.append(word)
                else:
                    if lesson_line:
                        line_surface = self.font_small.render(' '.join(lesson_line), True, GREEN)
                        lines.append({'surface': line_surface, 'y_offset': current_y, 'type': 'lesson'})
                        current_y += 35
                    lesson_line = [word]

            if lesson_line:
                line_surface = self.font_small.render(' '.join(lesson_line), True, GREEN)
                lines.append({'surface': line_surface, 'y_offset': current_y, 'type': 'lesson'})
                current_y += 35

        self.max_scroll = max(0, current_y - 600)

        # Main loop
        while True:
            draw_gradient_background(screen, GRADIENTS['story'][0], GRADIENTS['story'][1])

            # Header
            header_text = self.lang.get('real_story')
            header_surface = self.font_large.render(header_text, True, ORANGE)
            header_rect = header_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(header_surface, header_rect)

            # Story box
            box = pygame.Rect(50, 150, box_width, 500)
            pygame.draw.rect(screen, WHITE, box, border_radius=20)
            pygame.draw.rect(screen, GOLD, box, 5, border_radius=20)

            # Clip area for scrolling
            clip_rect = pygame.Rect(box.x + text_margin, box.y + 20, max_width, box.height - 40)
            screen.set_clip(clip_rect)

            # Draw all lines with scroll offset
            for line in lines:
                y_pos = box.y + 30 + line['y_offset'] - self.scroll_offset
                if box.y - 50 < y_pos < box.y + box.height + 50:
                    x_pos = box.x + text_margin
                    if line['type'] == 'title':
                        x_pos = box.x + (box_width - line['surface'].get_width()) // 2
                    screen.blit(line['surface'], (x_pos, y_pos))

            screen.set_clip(None)

            # Scroll instruction
            if self.max_scroll > 0:
                scroll_text = self.lang.get('scroll_for_more')
                scroll_surface = self.font_tiny.render(scroll_text, True, LIGHT_GRAY)
                scroll_rect = scroll_surface.get_rect(center=(SCREEN_WIDTH // 2, 670))
                screen.blit(scroll_surface, scroll_rect)

            # Start button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, self.lang.get('start_playing'), 400, 710, 400, 60,
                                GREEN, DARK_BLUE, self.font_medium):
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
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        pygame.time.wait(200)
                        pygame.event.clear()
                        return
                    elif event.key == pygame.K_DOWN:
                        self.scroll_offset = min(self.scroll_offset + 30, self.max_scroll)
                    elif event.key == pygame.K_UP:
                        self.scroll_offset = max(self.scroll_offset - 30, 0)

                if event.type == pygame.MOUSEWHEEL:
                    self.scroll_offset = max(0, min(self.scroll_offset - event.y * 30, self.max_scroll))

            pygame.display.flip()
            clock.tick(FPS)


class TipsScreen:
    """Tips screen before level starts"""

    def __init__(self, level_num, font_large, font_medium, font_small, font_tiny, lang_manager):
        self.level_num = level_num
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.font_tiny = font_tiny
        self.lang = lang_manager

    def show(self, screen, clock):
        """Show tips screen"""
        from game_data import get_tips

        tips = get_tips(self.level_num, self.lang.get_lang_code())
        if not tips:
            return

        button_was_pressed = False

        while True:
            draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

            # Header
            header_text = self.lang.get('how_to_play')
            header_surface = self.font_large.render(header_text, True, YELLOW)
            header_rect = header_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(header_surface, header_rect)

            # Tips box
            box = pygame.Rect(200, 200, 800, 400)
            pygame.draw.rect(screen, WHITE, box, border_radius=20)
            pygame.draw.rect(screen, CYAN, box, 5, border_radius=20)

            # Draw tips
            y_offset = 250
            for i, tip in enumerate(tips, 1):
                tip_text = f"{i}. {tip}"
                tip_surface = self.font_small.render(tip_text, True, BLACK)
                tip_rect = tip_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(tip_surface, tip_rect)
                y_offset += 60

            # Start button
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, self.lang.get('begin'), 400, 650, 400, 70,
                                GREEN, DARK_BLUE, self.font_large):
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
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        pygame.time.wait(200)
                        pygame.event.clear()
                        return

            pygame.display.flip()
            clock.tick(FPS)