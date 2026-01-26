

import pygame
import math
from constants import *


def draw_gradient_background(surface, color1, color2):
    """Draw vertical gradient background"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def draw_text_with_shadow(surface, text, x, y, font, color, shadow_color, shadow_offset):
    """Draw text with shadow - CENTERED"""
    shadow_surface = font.render(text, True, shadow_color)
    shadow_rect = shadow_surface.get_rect(center=(x + shadow_offset, y + shadow_offset))
    surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def draw_cute_button(surface, text, x, y, width, height, color, hover_color, font):
    """Draw button with hover effect"""
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    is_hovering = button_rect.collidepoint(mouse_pos)

    # Shadow
    shadow_rect = pygame.Rect(x + 5, y + 5, width, height)
    pygame.draw.rect(surface, BLACK, shadow_rect, border_radius=20)

    # Button
    button_color = hover_color if is_hovering else color
    pygame.draw.rect(surface, button_color, button_rect, border_radius=20)
    pygame.draw.rect(surface, WHITE, button_rect, 4, border_radius=20)

    # Text - CENTERED
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)

    # Glow effect when hovering
    if is_hovering:
        glow_rect = pygame.Rect(x - 3, y - 3, width + 6, height + 6)
        pygame.draw.rect(surface, YELLOW, glow_rect, 3, border_radius=22)

    return is_hovering


class Camera:
    """Camera for smooth scrolling"""

    def __init__(self):
        self.offset_x = 0

    def update(self, player_x):
        """Center camera on player"""
        target_offset = player_x - SCREEN_WIDTH // 2
        self.offset_x = max(0, target_offset)


class Timer:
    """Game timer"""

    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.time_left = time_limit

    def update(self):
        """Update timer"""
        if self.time_left > 0:
            self.time_left -= 1 / FPS

    def draw(self, surface, font):
        """Draw timer - BIGGER"""
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"

        # Timer box
        timer_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, 15, 200, 60)
        pygame.draw.rect(surface, DARK_BLUE, timer_box, border_radius=15)
        pygame.draw.rect(surface, YELLOW if self.time_left > 30 else RED, timer_box, 4, border_radius=15)

        # Time text - CENTERED
        time_surface = font.render(time_text, True, WHITE)
        time_rect = time_surface.get_rect(center=timer_box.center)
        surface.blit(time_surface, time_rect)


class ScoreDisplay:
    """Score display"""

    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.score = 0
        self.displayed_score = 0

    def set_score(self, score):
        """Set score"""
        self.score = score

    def update(self):
        """Animate score"""
        if self.displayed_score < self.score:
            self.displayed_score += 1

    def draw(self, surface):
        """Draw score - BIGGER"""
        score_box = pygame.Rect(self.x, self.y, 180, 60)
        pygame.draw.rect(surface, PURPLE, score_box, border_radius=15)
        pygame.draw.rect(surface, GOLD, score_box, 4, border_radius=15)

        score_text = f"{self.displayed_score}"
        score_surface = self.font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=score_box.center)
        surface.blit(score_surface, score_rect)


class QuizOverlay:
    """Quiz question overlay - BIGGER DESIGN"""

    def __init__(self, question_data, fonts):
        self.question_data = question_data
        self.fonts = fonts
        self.selected_answer = None
        self.show_result = False
        self.correct = False

    def handle_click(self, mouse_pos):
        """Handle answer click"""
        if self.show_result:
            return None

        # Check each answer button
        for i in range(len(self.question_data['answers'])):
            button_y = 380 + i * 90
            button_rect = pygame.Rect(250, button_y, 700, 70)

            if button_rect.collidepoint(mouse_pos):
                self.selected_answer = i
                self.correct = (i == self.question_data['correct'])
                self.show_result = True
                return self.correct

        return None

    def draw(self, surface):
        """Draw quiz overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Quiz box
        box_width = 900
        box_height = 600
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        # Shadow
        shadow_rect = pygame.Rect(box_x + 8, box_y + 8, box_width, box_height)
        pygame.draw.rect(surface, BLACK, shadow_rect, border_radius=30)

        # Box
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(surface, WHITE, box_rect, border_radius=30)
        pygame.draw.rect(surface, GOLD, box_rect, 6, border_radius=30)

        # Question text - word wrapped and BIGGER
        question_text = self.question_data['question']
        words = question_text.split()
        lines = []
        current_line = []
        max_width = box_width - 100

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.fonts['medium'].render(test_line, True, DARK_BLUE)
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        # Draw question lines
        y_offset = box_y + 60
        for line in lines:
            line_surface = self.fonts['medium'].render(line, True, DARK_BLUE)
            line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            surface.blit(line_surface, line_rect)
            y_offset += 55

        # Answer buttons - BIGGER
        for i, answer in enumerate(self.question_data['answers']):
            button_y = box_y + 250 + i * 90
            button_rect = pygame.Rect(box_x + 50, button_y, box_width - 100, 70)

            # Button color
            if self.show_result:
                if i == self.question_data['correct']:
                    button_color = GREEN
                elif i == self.selected_answer:
                    button_color = RED
                else:
                    button_color = LIGHT_GRAY
            else:
                button_color = BLUE

            # Shadow
            shadow = pygame.Rect(button_rect.x + 4, button_rect.y + 4,
                                 button_rect.width, button_rect.height)
            pygame.draw.rect(surface, BLACK, shadow, border_radius=15)

            # Button
            pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
            pygame.draw.rect(surface, WHITE, button_rect, 4, border_radius=15)

            # Answer text - CENTERED
            answer_surface = self.fonts['small'].render(answer, True, WHITE)
            answer_rect = answer_surface.get_rect(center=button_rect.center)
            surface.blit(answer_surface, answer_rect)


class PauseMenu:
    """Pause menu"""

    def __init__(self, fonts):
        self.fonts = fonts
        self.options = ['Продолжи', 'Рестартирај', 'Мени']

    def handle_input(self, event):
        """Handle input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(self.options):
                button_y = 350 + i * 100
                button_rect = pygame.Rect(400, button_y, 400, 70)
                if button_rect.collidepoint(mouse_pos):
                    return option
        return None

    def draw(self, surface):
        """Draw pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        # Title
        draw_text_with_shadow(surface, "ПАУЗА", SCREEN_WIDTH // 2, 200,
                              self.fonts['title'], YELLOW, BLACK, 5)

        # Options
        colors = [GREEN, ORANGE, RED]
        for i, option in enumerate(self.options):
            button_y = 350 + i * 100
            draw_cute_button(surface, option, 400, button_y, 400, 70,
                             colors[i], DARK_BLUE, self.fonts['medium'])


# Add this to the end of ui.py to handle the question format properly

class QuizOverlay:
    """Quiz question overlay - BIGGER DESIGN"""

    def __init__(self, question_data, fonts):
        self.question_data = question_data
        self.fonts = fonts
        self.selected_answer = None
        self.show_result = False
        self.correct = False

        # Parse question format - handle both formats
        if 'answers' in question_data:
            # Old format
            self.answers = question_data['answers']
            self.correct_index = question_data['correct']
        elif 'options' in question_data:
            # New format from questions_bank.py
            self.answers = [opt['text'] if isinstance(opt, dict) else opt for opt in question_data['options']]
            # Find correct answer index
            for i, opt in enumerate(question_data['options']):
                if isinstance(opt, dict) and opt.get('correct'):
                    self.correct_index = i
                    break

    def handle_click(self, mouse_pos):
        """Handle answer click"""
        if self.show_result:
            return None

        # Check each answer button
        for i in range(len(self.answers)):
            button_y = 380 + i * 90
            button_rect = pygame.Rect(250, button_y, 700, 70)

            if button_rect.collidepoint(mouse_pos):
                self.selected_answer = i
                self.correct = (i == self.correct_index)
                self.show_result = True
                return self.correct

        return None

    def draw(self, surface):
        """Draw quiz overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Quiz box
        box_width = 900
        box_height = 600
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2

        # Shadow
        shadow_rect = pygame.Rect(box_x + 8, box_y + 8, box_width, box_height)
        pygame.draw.rect(surface, BLACK, shadow_rect, border_radius=30)

        # Box
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(surface, WHITE, box_rect, border_radius=30)
        pygame.draw.rect(surface, GOLD, box_rect, 6, border_radius=30)

        # Question text - word wrapped and BIGGER
        question_text = self.question_data['question']
        words = question_text.split()
        lines = []
        current_line = []
        max_width = box_width - 100

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.fonts['medium'].render(test_line, True, DARK_BLUE)
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        # Draw question lines
        y_offset = box_y + 60
        for line in lines:
            line_surface = self.fonts['medium'].render(line, True, DARK_BLUE)
            line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            surface.blit(line_surface, line_rect)
            y_offset += 55

        # Answer buttons - BIGGER
        for i, answer in enumerate(self.answers):
            button_y = box_y + 250 + i * 90
            button_rect = pygame.Rect(box_x + 50, button_y, box_width - 100, 70)

            # Button color
            if self.show_result:
                if i == self.correct_index:
                    button_color = GREEN
                elif i == self.selected_answer:
                    button_color = RED
                else:
                    button_color = LIGHT_GRAY
            else:
                button_color = BLUE

            # Shadow
            shadow = pygame.Rect(button_rect.x + 4, button_rect.y + 4,
                                 button_rect.width, button_rect.height)
            pygame.draw.rect(surface, BLACK, shadow, border_radius=15)

            # Button
            pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
            pygame.draw.rect(surface, WHITE, button_rect, 4, border_radius=15)

            # Answer text - CENTERED
            answer_surface = self.fonts['small'].render(answer, True, WHITE)
            answer_rect = answer_surface.get_rect(center=button_rect.center)
            surface.blit(answer_surface, answer_rect)