"""
Mini-games for each level - Different gameplay mechanics
"""

import pygame
import random
import math
from constants import *


class PasswordStrengthMiniGame:
    """Level 1: Test password strength by typing correctly"""

    def __init__(self, fonts, lang_manager):
        self.fonts = fonts
        self.lang = lang_manager
        self.lang = lang_manager
        self.passwords = ['P@ssw0rd!', 'SecurePass123#', 'MyS3cure#Key', 'Str0ng!Pass']
        self.current_password = random.choice(self.passwords)
        self.user_input = ''
        self.time_limit = 15
        self.timer = self.time_limit * 60
        self.completed = False
        self.success = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.user_input == self.current_password:
                    self.completed = True
                    self.success = True
            elif len(self.user_input) < 30:
                self.user_input += event.unicode

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.success = False

    def draw(self, screen):
        draw_gradient_background(screen, GRADIENTS['level1'])

        title = self.fonts['large'].render('Напиши сигурна лозинка:', True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        # Target password
        target_rect = pygame.Rect(300, 300, 600, 60)
        pygame.draw.rect(screen, DARK_BLUE, target_rect, border_radius=10)
        target_text = self.fonts['medium'].render(self.current_password, True, GOLD)
        screen.blit(target_text, (target_rect.centerx - target_text.get_width() // 2, 315))

        # User input
        input_rect = pygame.Rect(300, 400, 600, 60)
        pygame.draw.rect(screen, WHITE, input_rect, border_radius=10)
        pygame.draw.rect(screen, GREEN if self.user_input == self.current_password else RED, input_rect, 3,
                         border_radius=10)
        input_text = self.fonts['medium'].render(self.user_input, True, BLACK)
        screen.blit(input_text, (input_rect.x + 10, 415))

        # Timer
        timer_text = self.fonts['small'].render(f'Time: {self.timer // 60}s', True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 500))


class PhishingDetectorMiniGame:
    """Level 2: Click on phishing indicators in fake emails"""

    def __init__(self, fonts, lang_manager):
        self.fonts = fonts
        self.lang = lang_manager
        self.lang = lang_manager
        self.indicators = [
            {'pos': (300, 250), 'size': 200, 'text': 'Wrong sender', 'found': False},
            {'pos': (300, 350), 'size': 220, 'text': 'Suspicious link', 'found': False},
            {'pos': (300, 450), 'size': 180, 'text': 'Urgent demand', 'found': False}
        ]
        self.time_limit = 20
        self.timer = self.time_limit * 60
        self.completed = False
        self.success = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for indicator in self.indicators:
                rect = pygame.Rect(indicator['pos'][0], indicator['pos'][1], indicator['size'], 40)
                if rect.collidepoint(mouse_pos):
                    indicator['found'] = True

            if all(ind['found'] for ind in self.indicators):
                self.completed = True
                self.success = True

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.success = False

    def draw(self, screen):
        draw_gradient_background(screen, GRADIENTS['level2'])

        title = self.fonts['large'].render('Најди ги сите phishing индикатори!', True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Fake email
        email_rect = pygame.Rect(200, 200, 800, 350)
        pygame.draw.rect(screen, WHITE, email_rect, border_radius=10)
        pygame.draw.rect(screen, DARK_BLUE, email_rect, 3, border_radius=10)

        # Indicators
        for i, indicator in enumerate(self.indicators):
            color = GREEN if indicator['found'] else RED
            rect = pygame.Rect(indicator['pos'][0], indicator['pos'][1], indicator['size'], 40)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            text = self.fonts['small'].render(indicator['text'], True, WHITE)
            screen.blit(text, (rect.x + 10, rect.y + 10))

        # Timer
        timer_text = self.fonts['small'].render(f'Time: {self.timer // 60}s', True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 600))


class DataProtectionMiniGame:
    """Level 3: Drag personal info to safe/unsafe zones"""

    def __init__(self, fonts, lang_manager):
        self.fonts = fonts
        self.lang = lang_manager
        self.lang = lang_manager
        self.items = [
            {'text': 'Име и Презиме', 'safe': False, 'pos': [300, 200], 'dragging': False},
            {'text': 'Домашна Адреса', 'safe': False, 'pos': [300, 260], 'dragging': False},
            {'text': 'Омилена Боја', 'safe': True, 'pos': [300, 320], 'dragging': False},
            {'text': 'Кредитна Картичка', 'safe': False, 'pos': [300, 380], 'dragging': False}
        ]
        self.dragging_item = None
        self.time_limit = 25
        self.timer = self.time_limit * 60
        self.completed = False
        self.success = False
        self.safe_zone = pygame.Rect(700, 200, 250, 250)
        self.unsafe_zone = pygame.Rect(700, 480, 250, 150)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.items:
                rect = pygame.Rect(item['pos'][0], item['pos'][1], 180, 40)
                if rect.collidepoint(mouse_pos):
                    item['dragging'] = True
                    self.dragging_item = item

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_item:
                mouse_pos = pygame.mouse.get_pos()
                if self.safe_zone.collidepoint(mouse_pos) and not self.dragging_item['safe']:
                    self.dragging_item['placed'] = 'safe'
                elif self.unsafe_zone.collidepoint(mouse_pos) and self.dragging_item['safe']:
                    self.dragging_item['placed'] = 'unsafe'
                self.dragging_item['dragging'] = False
                self.dragging_item = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_item:
                mouse_pos = pygame.mouse.get_pos()
                self.dragging_item['pos'] = [mouse_pos[0] - 90, mouse_pos[1] - 20]

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.success = False

        if all('placed' in item for item in self.items):
            self.completed = True
            self.success = True

    def draw(self, screen):
        draw_gradient_background(screen, GRADIENTS['level3'])

        title = self.fonts['large'].render('Sort Information: Safe to Share?', True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Safe zone
        pygame.draw.rect(screen, GREEN, self.safe_zone, border_radius=10)
        safe_label = self.fonts['medium'].render('Safe to Share', True, WHITE)
        screen.blit(safe_label, (self.safe_zone.centerx - safe_label.get_width() // 2, 220))

        # Unsafe zone
        pygame.draw.rect(screen, RED, self.unsafe_zone, border_radius=10)
        unsafe_label = self.fonts['medium'].render('Keep Private', True, WHITE)
        screen.blit(unsafe_label, (self.unsafe_zone.centerx - unsafe_label.get_width() // 2, 510))

        # Items
        for item in self.items:
            rect = pygame.Rect(item['pos'][0], item['pos'][1], 180, 40)
            pygame.draw.rect(screen, BLUE, rect, border_radius=5)
            text = self.fonts['small'].render(item['text'], True, WHITE)
            screen.blit(text, (rect.x + 10, rect.y + 10))


class ScamSpotterMiniGame:
    """Level 4: Identify scam elements in scenarios"""

    def __init__(self, fonts, lang_manager):
        self.fonts = fonts
        self.lang = lang_manager
        self.lang = lang_manager
        self.scenarios = [
            {'text': '"Ти освои 1 милион денари, Кликни ОВДЕ!"', 'is_scam': True, 'answered': False},
            {'text': '"Емаил од твојот наставник по историја"', 'is_scam': False, 'answered': False},
            {'text': '"ВАШИОТ ПРОФИЛ КЕ БИДЕ ИЗГАСЕН ВЕДНАШ! КЛИКНИ ОВДЕ"', 'is_scam': True, 'answered': False}
        ]
        self.current_scenario = 0
        self.time_limit = 20
        self.timer = self.time_limit * 60
        self.completed = False
        self.success = False
        self.correct_answers = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_scenario < len(self.scenarios):
                mouse_pos = pygame.mouse.get_pos()
                scam_button = pygame.Rect(300, 500, 200, 60)
                legit_button = pygame.Rect(700, 500, 200, 60)

                if scam_button.collidepoint(mouse_pos):
                    if self.scenarios[self.current_scenario]['is_scam']:
                        self.correct_answers += 1
                    self.current_scenario += 1
                elif legit_button.collidepoint(mouse_pos):
                    if not self.scenarios[self.current_scenario]['is_scam']:
                        self.correct_answers += 1
                    self.current_scenario += 1

                if self.current_scenario >= len(self.scenarios):
                    self.completed = True
                    self.success = self.correct_answers >= 2

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.success = False

    def draw(self, screen):
        draw_gradient_background(screen, GRADIENTS['level4'])

        title = self.fonts['large'].render('Is This a Scam?', True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        if self.current_scenario < len(self.scenarios):
            # Scenario text
            scenario_text = self.scenarios[self.current_scenario]['text']
            text_surface = self.fonts['medium'].render(scenario_text, True, WHITE)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 300))

            # Buttons
            scam_button = pygame.Rect(300, 500, 200, 60)
            pygame.draw.rect(screen, RED, scam_button, border_radius=10)
            scam_text = self.fonts['medium'].render('SCAM', True, WHITE)
            screen.blit(scam_text, (scam_button.centerx - scam_text.get_width() // 2, 515))

            legit_button = pygame.Rect(700, 500, 200, 60)
            pygame.draw.rect(screen, GREEN, legit_button, border_radius=10)
            legit_text = self.fonts['medium'].render('LEGIT', True, WHITE)
            screen.blit(legit_text, (legit_button.centerx - legit_text.get_width() // 2, 515))


class CyberBullyResponseMiniGame:
    """Level 5: Choose correct responses to cyberbullying"""

    def __init__(self, fonts, lang_manager):
        self.fonts = fonts
        self.lang = lang_manager
        self.lang = lang_manager
        self.scenarios = [
            {
                'text': 'Некој ми испрати порака за тебе!',
                'options': ['Одговори', 'Пријави и блокирај', 'Сподели информации за тебе'],
                'correct': 1
            },
            {
                'text': 'Твоите пријатели споделиле срамна слика од тебе',
                'options': ['Не прави ништо', 'Пријави на родител', 'Објави слика и од нив'],
                'correct': 1
            }
        ]
        self.current_scenario = 0
        self.time_limit = 25
        self.timer = self.time_limit * 60
        self.completed = False
        self.success = False
        self.correct_answers = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_scenario < len(self.scenarios):
                mouse_pos = pygame.mouse.get_pos()
                for i in range(3):
                    button_rect = pygame.Rect(300, 400 + i * 80, 600, 60)
                    if button_rect.collidepoint(mouse_pos):
                        if i == self.scenarios[self.current_scenario]['correct']:
                            self.correct_answers += 1
                        self.current_scenario += 1

                        if self.current_scenario >= len(self.scenarios):
                            self.completed = True
                            self.success = self.correct_answers >= 1

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.completed = True
            self.success = False

    def draw(self, screen):
        draw_gradient_background(screen, GRADIENTS['level5'])

        title = self.fonts['large'].render('How to Respond?', True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        if self.current_scenario < len(self.scenarios):
            scenario = self.scenarios[self.current_scenario]

            # Scenario text
            scenario_text = self.fonts['medium'].render(scenario['text'], True, WHITE)
            screen.blit(scenario_text, (SCREEN_WIDTH // 2 - scenario_text.get_width() // 2, 250))

            # Option buttons
            for i, option in enumerate(scenario['options']):
                button_rect = pygame.Rect(300, 400 + i * 80, 600, 60)
                pygame.draw.rect(screen, BLUE, button_rect, border_radius=10)
                option_text = self.fonts['small'].render(option, True, WHITE)
                screen.blit(option_text, (button_rect.centerx - option_text.get_width() // 2, 415 + i * 80))


def draw_gradient_background(screen, gradient):

    color1, color2 = gradient
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))


def get_minigame_for_level(level_num, fonts, lang_manager):

    minigames = {
        1: PasswordStrengthMiniGame,
        2: PhishingDetectorMiniGame,
        3: DataProtectionMiniGame,
        4: ScamSpotterMiniGame,
        5: CyberBullyResponseMiniGame
    }
    return minigames.get(level_num, PasswordStrengthMiniGame)(fonts, lang_manager)