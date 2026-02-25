"""
COMPLETE WORKING main.py - Albanian support + All levels working + Points synchronized + Settings Screen
"""

import pygame
import sys
import time
from constants import *
from language import LanguageManager
from database import Database
from ui import draw_gradient_background, draw_cute_button, draw_text_with_shadow
from trophy_cabinet import TrophyCabinet, show_level_complete_animation

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Интернет Безбедност - Детска Игра")
clock = pygame.time.Clock()

# Language Manager and Database - GLOBAL
lang_manager = LanguageManager()
db = Database()

# Current user and play session
current_user = None
play_session_start = None


# Fonts
def load_fonts():
    try:
        return {
            'title': pygame.font.Font(None, FONT_SIZES['title']),
            'large': pygame.font.Font(None, FONT_SIZES['large']),
            'medium': pygame.font.Font(None, FONT_SIZES['medium']),
            'small': pygame.font.Font(None, FONT_SIZES['small']),
            'tiny': pygame.font.Font(None, FONT_SIZES['tiny']),
            'mini': pygame.font.Font(None, FONT_SIZES['mini'])
        }
    except:
        return {
            'title': pygame.font.SysFont('dejavusans', FONT_SIZES['title']),
            'large': pygame.font.SysFont('dejavusans', FONT_SIZES['large']),
            'medium': pygame.font.SysFont('dejavusans', FONT_SIZES['medium']),
            'small': pygame.font.SysFont('dejavusans', FONT_SIZES['small']),
            'tiny': pygame.font.SysFont('dejavusans', FONT_SIZES['tiny']),
            'mini': pygame.font.SysFont('dejavusans', FONT_SIZES['mini'])
        }


fonts = load_fonts()


def pause_menu(screen, clock, fonts, lang_manager):
    """
    Pause menu with Resume and Exit options
    Returns: 'resume' or 'exit'
    """
    button_was_pressed = False

    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    while True:
        # Draw the overlay
        screen.blit(overlay, (0, 0))

        # Draw pause title
        pause_text = lang_manager.get('pause')
        draw_text_with_shadow(screen, pause_text, SCREEN_WIDTH // 2, 200,
                              fonts['title'], YELLOW, DARK_BLUE, 5)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Resume button
        resume_text = lang_manager.get('resume')
        if draw_cute_button(screen, resume_text, 400, 350, 400, 80,
                            GREEN, DARK_BLUE, fonts['large']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200)
                pygame.event.clear()
                return 'resume'

        # Exit to menu button
        exit_text = lang_manager.get('menu')
        if draw_cute_button(screen, exit_text, 400, 460, 400, 80,
                            RED, PINK, fonts['large']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200)
                pygame.event.clear()
                return 'exit'

        button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Press ESC again to resume
                    pygame.time.wait(200)
                    pygame.event.clear()
                    return 'resume'

        pygame.display.flip()
        clock.tick(FPS)


def language_selection_screen():
    """Language selection screen"""
    button_was_pressed = False
    selected_lang = None

    char_images = []
    for i in range(1, 4):
        try:
            img = pygame.image.load(f'creatives/slika{i}-removebg-preview.png')
            img = pygame.transform.scale(img, (120, 120))
            char_images.append(img)
        except:
            char_images.append(None)

    while selected_lang is None:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        title_text = "Избери Јазик / Zgjidh Gjuhën"
        draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 150,
                              fonts['title'], YELLOW, DARK_BLUE, 5)

        subtitle_text = "Select Language"
        subtitle_surface = fonts['large'].render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 240))
        screen.blit(subtitle_surface, subtitle_rect)

        char_y = 300
        if len(char_images) >= 3:
            if char_images[0]:
                screen.blit(char_images[0], (200, char_y))
            if char_images[1]:
                screen.blit(char_images[1], (SCREEN_WIDTH // 2 - 60, char_y))
            if char_images[2]:
                screen.blit(char_images[2], (SCREEN_WIDTH - 320, char_y))

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if draw_cute_button(screen, "Македонски", 110, 480, 250, 80,
                            CYAN, BLUE, fonts['medium']):
            if mouse_pressed and not button_was_pressed:
                selected_lang = 'mk'

        if draw_cute_button(screen, "Shqip", 475, 480, 250, 80,
                            GREEN, DARK_BLUE, fonts['medium']):
            if mouse_pressed and not button_was_pressed:
                selected_lang = 'sq'

        if draw_cute_button(screen, "English", 840, 480, 250, 80,
                            ORANGE, RED, fonts['medium']):
            if mouse_pressed and not button_was_pressed:
                selected_lang = 'en'

        button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

    lang_manager.set_language(selected_lang)
    pygame.time.wait(500)
    pygame.event.clear()


def set_play_time_screen():
    """Parent sets daily play time limit"""
    button_was_pressed = False
    selected_time = 30
    time_options = [15, 30, 45, 60, 90, 120]

    while True:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        draw_text_with_shadow(screen, lang_manager.get('parental_control'), SCREEN_WIDTH // 2, 80,
                              fonts['large'], YELLOW, DARK_BLUE, 4)

        try:
            parent_img = pygame.image.load('creatives/slika2-removebg-preview.png')
            parent_img = pygame.transform.scale(parent_img, (100, 100))
            screen.blit(parent_img, (SCREEN_WIDTH // 2 - 50, 150))
        except:
            pass

        instruction1 = fonts['small'].render(lang_manager.get('for_parents'), True, WHITE)
        inst1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(instruction1, inst1_rect)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        for i, time_opt in enumerate(time_options):
            row = i // 3
            col = i % 3
            x = 250 + col * 250
            y = 380 + row * 100

            time_text = f"{time_opt} {lang_manager.get('min')}"
            button_color = GREEN if time_opt == selected_time else CYAN
            hover_color = DARK_BLUE if time_opt == selected_time else BLUE

            if draw_cute_button(screen, time_text, x, y, 200, 70,
                                button_color, hover_color, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    selected_time = time_opt

        selected_box = pygame.Rect(400, 600, 400, 60)
        pygame.draw.rect(screen, GOLD, selected_box, border_radius=15)
        pygame.draw.rect(screen, WHITE, selected_box, 3, border_radius=15)
        selected_display = fonts['medium'].render(
            f"{lang_manager.get('selected')}: {selected_time} {lang_manager.get('minutes_per_day')}",
            True, BLACK
        )
        selected_rect = selected_display.get_rect(center=selected_box.center)
        screen.blit(selected_display, selected_rect)

        if draw_cute_button(screen, lang_manager.get('confirm_and_start'), 350, 690, 500, 70,
                            GREEN, DARK_BLUE, fonts['medium']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200)
                pygame.event.clear()
                return selected_time

        button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


def settings_screen():
    """Settings screen - manage play time"""
    pygame.time.wait(200)
    pygame.event.clear()

    button_was_pressed = False
    mode = 'main'  # 'main', 'set', 'add', 'reset'
    selected_time = 60
    time_options = [15, 30, 60, 90, 120, 240]

    while True:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        if mode == 'main':
            # Main settings screen - show current info and action buttons

            # Title
            title_text = lang_manager.get('settings')
            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 80,
                                  fonts['large'], YELLOW, DARK_BLUE, 4)

            # Get current play time info
            if current_user:
                limit, played = db.get_play_time_info(current_user['id'])
                remaining = limit - played
            else:
                limit, played, remaining = 60, 0, 60

            # Current play time info box
            info_box_rect = pygame.Rect(250, 150, 700, 180)
            pygame.draw.rect(screen, DARK_BLUE, info_box_rect, border_radius=15)
            pygame.draw.rect(screen, GOLD, info_box_rect, 3, border_radius=15)

            # Display current time info
            limit_text = f"{lang_manager.get('daily_limit_label')} {limit} {lang_manager.get('minutes')}"
            played_text = f"{lang_manager.get('played_today')} {played} {lang_manager.get('minutes')}"
            remaining_text = f"{lang_manager.get('remaining_label')} {remaining} {lang_manager.get('minutes')}"

            limit_surface = fonts['medium'].render(limit_text, True, WHITE)
            played_surface = fonts['medium'].render(played_text, True, YELLOW)
            remaining_surface = fonts['medium'].render(remaining_text, True, GREEN if remaining > 30 else RED)

            screen.blit(limit_surface, (info_box_rect.centerx - limit_surface.get_width() // 2, 175))
            screen.blit(played_surface, (info_box_rect.centerx - played_surface.get_width() // 2, 220))
            screen.blit(remaining_surface, (info_box_rect.centerx - remaining_surface.get_width() // 2, 265))

            # Action selection text
            action_text = lang_manager.get('select_action')
            action_surface = fonts['medium'].render(action_text, True, WHITE)
            screen.blit(action_surface, (SCREEN_WIDTH // 2 - action_surface.get_width() // 2, 330))

            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Action buttons
            button_y = 400

            # SET button (set new limit from 0)
            set_btn_text = lang_manager.get('set_new_limit')
            if draw_cute_button(screen, set_btn_text, 200, button_y, 350, 70,
                                CYAN, BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'set'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # ADD button (add time to current limit)
            add_btn_text = lang_manager.get('add_time')
            if draw_cute_button(screen, add_btn_text, 700, button_y, 300, 70,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'add'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # RESET button (reset today's played time to 0)
            reset_btn_text = lang_manager.get('reset_played_time')
            if draw_cute_button(screen, reset_btn_text, 350, button_y + 100, 500, 70,
                                ORANGE, RED, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'reset'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # Back button
            back_text = lang_manager.get('back')
            if draw_cute_button(screen, back_text, 450, 650, 300, 60,
                                RED, PINK, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    pygame.time.wait(200)
                    pygame.event.clear()
                    return

            button_was_pressed = mouse_pressed

        elif mode == 'set':
            # SET mode - choose new limit (replaces current limit)
            title_text = lang_manager.get('set_new_limit')
            instruction_text = lang_manager.get('choose_new_limit')

            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 100,
                                  fonts['large'], YELLOW, DARK_BLUE, 4)

            instruction_surface = fonts['medium'].render(instruction_text, True, WHITE)
            screen.blit(instruction_surface, (SCREEN_WIDTH // 2 - instruction_surface.get_width() // 2, 180))

            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Time option buttons
            for i, time_opt in enumerate(time_options):
                row = i // 3
                col = i % 3
                x = 250 + col * 250
                y = 280 + row * 100

                time_text = f"{time_opt} {lang_manager.get('minutes')}"

                button_color = GREEN if time_opt == selected_time else CYAN
                hover_color = DARK_BLUE if time_opt == selected_time else BLUE

                if draw_cute_button(screen, time_text, x, y, 200, 70,
                                    button_color, hover_color, fonts['medium']):
                    if mouse_pressed and not button_was_pressed:
                        selected_time = time_opt

            # Show selected
            selected_box = pygame.Rect(350, 520, 500, 60)
            pygame.draw.rect(screen, GOLD, selected_box, border_radius=15)
            pygame.draw.rect(screen, WHITE, selected_box, 3, border_radius=15)

            selected_display_text = f"{lang_manager.get('selected')}: {selected_time} {lang_manager.get('minutes')}"

            selected_display = fonts['medium'].render(selected_display_text, True, BLACK)
            selected_rect = selected_display.get_rect(center=selected_box.center)
            screen.blit(selected_display, selected_rect)

            # Confirm button
            confirm_text = lang_manager.get('confirm')
            if draw_cute_button(screen, confirm_text, 350, 610, 250, 60,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    if current_user:
                        db.update_play_time_limit(current_user['id'], selected_time)
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # Back button
            back_text = lang_manager.get('back')
            if draw_cute_button(screen, back_text, 650, 610, 250, 60,
                                RED, PINK, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            button_was_pressed = mouse_pressed

        elif mode == 'add':
            # ADD mode - add time to current limit
            title_text = lang_manager.get('add_time')
            instruction_text = lang_manager.get('how_many_minutes')

            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 100,
                                  fonts['large'], YELLOW, DARK_BLUE, 4)

            instruction_surface = fonts['medium'].render(instruction_text, True, WHITE)
            screen.blit(instruction_surface, (SCREEN_WIDTH // 2 - instruction_surface.get_width() // 2, 180))

            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Time option buttons
            for i, time_opt in enumerate(time_options):
                row = i // 3
                col = i % 3
                x = 250 + col * 250
                y = 280 + row * 100

                time_text = f"+{time_opt} {lang_manager.get('min')}"

                button_color = GREEN if time_opt == selected_time else CYAN
                hover_color = DARK_BLUE if time_opt == selected_time else BLUE

                if draw_cute_button(screen, time_text, x, y, 200, 70,
                                    button_color, hover_color, fonts['medium']):
                    if mouse_pressed and not button_was_pressed:
                        selected_time = time_opt

            # Show selected
            selected_box = pygame.Rect(350, 520, 500, 60)
            pygame.draw.rect(screen, GOLD, selected_box, border_radius=15)
            pygame.draw.rect(screen, WHITE, selected_box, 3, border_radius=15)

            selected_display_text = f"{lang_manager.get('will_be_added')} +{selected_time} {lang_manager.get('minutes')}"

            selected_display = fonts['medium'].render(selected_display_text, True, BLACK)
            selected_rect = selected_display.get_rect(center=selected_box.center)
            screen.blit(selected_display, selected_rect)

            # Confirm button
            confirm_text = lang_manager.get('confirm')
            if draw_cute_button(screen, confirm_text, 350, 610, 250, 60,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    if current_user:
                        db.extend_play_time(current_user['id'], selected_time)
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # Back button
            back_text = lang_manager.get('back')
            if draw_cute_button(screen, back_text, 650, 610, 250, 60,
                                RED, PINK, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            button_was_pressed = mouse_pressed

        elif mode == 'reset':
            # RESET mode - confirm reset of today's played time
            title_text = lang_manager.get('reset_played_time')
            warning_text = lang_manager.get('confirm_reset_q')
            warning_text2 = lang_manager.get('confirm_reset_q2')
            confirm_text = lang_manager.get('yes_reset')
            cancel_text = lang_manager.get('no_back')

            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 150,
                                  fonts['large'], YELLOW, DARK_BLUE, 4)

            # Warning icon
            pygame.draw.circle(screen, ORANGE, (SCREEN_WIDTH // 2, 280), 60)
            pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH // 2, 280), 55)
            warning_symbol = fonts['title'].render("!", True, RED)
            warning_rect = warning_symbol.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(warning_symbol, warning_rect)

            # Warning text
            warning_surface1 = fonts['medium'].render(warning_text, True, WHITE)
            warning_surface2 = fonts['medium'].render(warning_text2, True, WHITE)
            screen.blit(warning_surface1, (SCREEN_WIDTH // 2 - warning_surface1.get_width() // 2, 370))
            screen.blit(warning_surface2, (SCREEN_WIDTH // 2 - warning_surface2.get_width() // 2, 420))

            mouse_pressed = pygame.mouse.get_pressed()[0]

            # Confirm button
            if draw_cute_button(screen, confirm_text, 300, 500, 300, 70,
                                RED, PINK, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    if current_user:
                        db.reset_daily_play_time(current_user['id'])
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            # Cancel button
            if draw_cute_button(screen, cancel_text, 700, 500, 300, 70,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'main'
                    pygame.time.wait(200)
                    pygame.event.clear()

            button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if mode == 'main':
                        pygame.time.wait(200)
                        pygame.event.clear()
                        return
                    else:
                        mode = 'main'
                        pygame.time.wait(200)
                        pygame.event.clear()

        pygame.display.flip()
        clock.tick(FPS)


def login_register_screen():
    """Login or Register screen"""
    global current_user
    button_was_pressed = False
    mode = 'main'
    username_input = ''
    password_input = ''
    message = ''
    message_color = WHITE
    active_field = 'username'

    while current_user is None:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        if mode == 'main':
            title = lang_manager.get('title')
            draw_text_with_shadow(screen, title, SCREEN_WIDTH // 2, 150,
                                  fonts['title'], YELLOW, DARK_BLUE, 5)

            subtitle = lang_manager.get('subtitle')
            subtitle_surface = fonts['medium'].render(subtitle, True, WHITE)
            subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(subtitle_surface, subtitle_rect)

            char_images = []
            for i in range(1, 4):
                try:
                    img = pygame.image.load(f'creatives/slika{i}-removebg-preview.png')
                    img = pygame.transform.scale(img, (150, 150))
                    char_images.append(img)
                except:
                    char_images.append(None)

            char_y = 300
            spacing = SCREEN_WIDTH // 4
            for i, char_img in enumerate(char_images):
                if char_img:
                    x_pos = spacing * (i + 1) - 75
                    screen.blit(char_img, (x_pos, char_y))

            mouse_pressed = pygame.mouse.get_pressed()[0]
            if draw_cute_button(screen, lang_manager.get('login'), 350, 500, 200, 70,
                                BLUE, CYAN, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'login'
                    message = ''
                    pygame.time.wait(200)
                    pygame.event.clear()

            if draw_cute_button(screen, lang_manager.get('register'), 650, 500, 300, 70,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'register'
                    message = ''
                    pygame.time.wait(200)
                    pygame.event.clear()

            button_was_pressed = mouse_pressed

        elif mode in ['login', 'register']:
            title_text = lang_manager.get('login_title') if mode == 'login' else lang_manager.get('register_title')
            draw_text_with_shadow(screen, title_text, SCREEN_WIDTH // 2, 150,
                                  fonts['large'], YELLOW, DARK_BLUE, 4)

            username_label = fonts['small'].render(lang_manager.get('username'), True, WHITE)
            screen.blit(username_label, (400, 280))

            username_box = pygame.Rect(400, 320, 400, 50)
            username_color = YELLOW if active_field == 'username' else WHITE
            pygame.draw.rect(screen, username_color, username_box, 3, border_radius=10)
            pygame.draw.rect(screen, DARK_BLUE, username_box, border_radius=10)

            username_surface = fonts['medium'].render(username_input, True, WHITE)
            screen.blit(username_surface, (410, 330))

            password_label = fonts['small'].render(lang_manager.get('password'), True, WHITE)
            screen.blit(password_label, (400, 400))

            password_box = pygame.Rect(400, 440, 400, 50)
            password_color = YELLOW if active_field == 'password' else WHITE
            pygame.draw.rect(screen, password_color, password_box, 3, border_radius=10)
            pygame.draw.rect(screen, DARK_BLUE, password_box, border_radius=10)

            password_display = '*' * len(password_input)
            password_surface = fonts['medium'].render(password_display, True, WHITE)
            screen.blit(password_surface, (410, 450))

            if message:
                message_surface = fonts['small'].render(message, True, message_color)
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 530))
                screen.blit(message_surface, message_rect)

            mouse_pressed = pygame.mouse.get_pressed()[0]

            button_text = lang_manager.get('login') if mode == 'login' else lang_manager.get('register')
            if draw_cute_button(screen, button_text, 450, 570, 300, 60,
                                GREEN, DARK_BLUE, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    if username_input and password_input:
                        if mode == 'register':
                            play_time_limit = set_play_time_screen()
                            current_lang = lang_manager.get_lang_code()
                            success, user_id = db.register_user(username_input, password_input,
                                                                current_lang,
                                                                play_time_limit)
                            if success:
                                message = lang_manager.get('registration_success')
                                message_color = GREEN
                                success, user_data = db.login_user(username_input, password_input)
                                if success:
                                    current_user = user_data
                                    saved_lang = user_data.get('language', 'mk')
                                    lang_manager.set_language(saved_lang)
                                    break
                            else:
                                message = lang_manager.get('username_taken')
                                message_color = RED
                        else:
                            success, user_data = db.login_user(username_input, password_input)
                            if success:
                                current_user = user_data
                                saved_lang = user_data.get('language', 'mk')
                                lang_manager.set_language(saved_lang)
                                break
                            else:
                                message = lang_manager.get('invalid_credentials')
                                message_color = RED
                    else:
                        message = lang_manager.get('fill_all_fields')
                        message_color = ORANGE
                    pygame.time.wait(200)
                    pygame.event.clear()

            if draw_cute_button(screen, lang_manager.get('back'), 450, 650, 300, 60,
                                RED, PINK, fonts['medium']):
                if mouse_pressed and not button_was_pressed:
                    mode = 'main'
                    username_input = ''
                    password_input = ''
                    message = ''
                    pygame.time.wait(200)
                    pygame.event.clear()

            button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode in ['login', 'register']:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_box.collidepoint(event.pos):
                        active_field = 'username'
                    elif password_box.collidepoint(event.pos):
                        active_field = 'password'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if active_field == 'username':
                            username_input = username_input[:-1]
                        else:
                            password_input = password_input[:-1]
                    elif event.key == pygame.K_TAB:
                        active_field = 'password' if active_field == 'username' else 'username'
                    elif event.unicode.isprintable():
                        if active_field == 'username' and len(username_input) < 20:
                            username_input += event.unicode
                        elif active_field == 'password' and len(password_input) < 30:
                            password_input += event.unicode

        pygame.display.flip()
        clock.tick(FPS)


def main_menu():
    """Main menu"""
    pygame.time.wait(200)
    pygame.event.clear()

    button_was_pressed = False

    char_images = []
    for i in range(1, 4):
        try:
            img = pygame.image.load(f'creatives/slika{i}-removebg-preview.png')
            img = pygame.transform.scale(img, (80, 80))  # Reduced size to fit
            char_images.append(img)
        except:
            char_images.append(None)

    # Load spaceship button image for Level 4
    try:
        spaceship_button_img = pygame.image.load('creatives/spaceship-button.png')
    except:
        spaceship_button_img = None

    # Load Level 3 button image
    try:
        level3_button_img = pygame.image.load('images/maze-button.png')
    except:
        try:
            level3_button_img = pygame.image.load('creatives/level3-removebg-preview.png')
        except:
            level3_button_img = None

    # Load Super Mario button image for Level 1
    try:
        supermario_button_img = pygame.image.load('creatives/supermario-button.png')
    except:
        supermario_button_img = None

    # Load Parkour button image for Level 2
    try:
        parkour_button_img = pygame.image.load('creatives/parkour-button.png')
    except:
        parkour_button_img = None

    # Load Memory button image for Level 5
    try:
        memory_button_img = pygame.image.load('creatives/memory-button.png')
    except:
        memory_button_img = None

    while True:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        title = lang_manager.get('title')
        draw_text_with_shadow(screen, title, SCREEN_WIDTH // 2, 50,
                              fonts['large'], YELLOW, DARK_BLUE, 4)

        if current_user:
            # Get total points from database
            try:
                cursor = db.conn.cursor()
                cursor.execute("SELECT SUM(score) FROM scores WHERE user_id = ?", (current_user['id'],))
                result = cursor.fetchone()
                total_points = result[0] if result[0] else 0
            except:
                total_points = 0

            # Create user info box
            info_text = f"{current_user['username']} | {total_points} {lang_manager.get('score')}"
            info_surface = fonts['medium'].render(info_text, True, WHITE)
            info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))

            # Draw box
            box_padding = 20
            info_box = pygame.Rect(
                info_rect.x - box_padding,
                info_rect.y - 10,
                info_rect.width + box_padding * 2,
                info_rect.height + 20
            )
            pygame.draw.rect(screen, DARK_BLUE, info_box, border_radius=15)
            pygame.draw.rect(screen, GOLD, info_box, 3, border_radius=15)
            screen.blit(info_surface, info_rect)

        if current_user and current_user.get('play_time_limit', 0) > 0:
            remaining = db.get_play_time_remaining(current_user['id'])
            time_box = pygame.Rect(SCREEN_WIDTH - 200, 20, 180, 50)
            time_color = GREEN if remaining > 30 else (ORANGE if remaining > 10 else RED)
            pygame.draw.rect(screen, time_color, time_box, border_radius=15)
            pygame.draw.rect(screen, WHITE, time_box, 3, border_radius=15)
            time_text = f"{remaining} {lang_manager.get('min')}"
            time_surface = fonts['small'].render(time_text, True, WHITE)
            time_rect = time_surface.get_rect(center=time_box.center)
            screen.blit(time_surface, time_rect)

        # Characters
        char_y = 130
        spacing = SCREEN_WIDTH // 4
        for i, char_img in enumerate(char_images):
            if char_img:
                x_pos = spacing * (i + 1) - 40
                screen.blit(char_img, (x_pos, char_y))

        # Levels Section
        button_y_start = 220
        button_height = 65
        button_spacing = 85  # 65px height + 20px gap
        button_width = 700
        button_x = (SCREEN_WIDTH - button_width) // 2

        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        level_images = {
            1: supermario_button_img, 2: parkour_button_img,
            3: level3_button_img, 4: spaceship_button_img,
            5: memory_button_img
        }

        # Unique Level Colors
        level_colors = [CYAN, ORANGE, GREEN, RED, PURPLE]

        for level_num in range(1, 6):
            level_key = f'level{level_num}'
            level_text = lang_manager.get(level_key)
            y_pos = button_y_start + (level_num - 1) * button_spacing

            button_rect = pygame.Rect(button_x, y_pos, button_width, button_height)
            is_hovering = button_rect.collidepoint(mouse_pos)
            is_clicking = is_hovering and mouse_pressed

            # Click Offset
            draw_y = y_pos + (2 if is_clicking else 0)
            
            # Button Color Logic
            base_color = level_colors[level_num - 1]
            if is_clicking:
                draw_color = tuple(max(0, c - 40) for c in base_color)
            elif is_hovering:
                draw_color = tuple(min(255, c + 30) for c in base_color)
            else:
                draw_color = base_color

            # Draw shadow
            pygame.draw.rect(screen, (0, 0, 0, 80), (button_x + 4, draw_y + 4, button_width, button_height), border_radius=32)

            # Main pill base
            pygame.draw.rect(screen, draw_color, (button_x, draw_y, button_width, button_height), border_radius=32)

            # Glass Effect (Top highlight)
            glass_surface = pygame.Surface((button_width, button_height // 2), pygame.SRCALPHA)
            glass_surface.fill((255, 255, 255, 30))
            screen.blit(glass_surface, (button_x, draw_y))

            # Icon Container (100px width sub-rect)
            icon_box = pygame.Rect(button_x + 5, draw_y + 5, 90, button_height - 10)
            pygame.draw.rect(screen, WHITE, icon_box, border_radius=25)
            pygame.draw.rect(screen, DARK_BLUE, icon_box, 2, border_radius=25)

            if level_images[level_num]:
                img = level_images[level_num]
                img_aspect = img.get_width() / img.get_height()
                target_h = icon_box.height - 10
                target_w = int(target_h * img_aspect)
                if target_w > icon_box.width - 10:
                    target_w = icon_box.width - 10
                    target_h = int(target_w / img_aspect)
                
                scaled_img = pygame.transform.scale(img, (target_w, target_h))
                screen.blit(scaled_img, (icon_box.centerx - target_w // 2, icon_box.centery - target_h // 2))

            # Text section - Centered in remaining space
            text_area_x = button_x + 100
            text_area_width = button_width - 100
            text_surface = fonts['medium'].render(level_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(text_area_x + text_area_width // 2, draw_y + button_height // 2))
            
            # Text shadow
            shadow_surf = fonts['medium'].render(level_text, True, BLACK)
            screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text_surface, text_rect)

            # White Border
            pygame.draw.rect(screen, WHITE, (button_x, draw_y, button_width, button_height), 3, border_radius=32)

            if is_hovering and mouse_pressed and not button_was_pressed:
                pygame.time.wait(300)
                pygame.event.clear()
                return level_num

        # Bottom Row
        FOREST_GREEN = (34, 139, 34)
        bottom_y = 720
        
        # Settings (250px)
        if draw_cute_button(screen, lang_manager.get('settings'), 50, bottom_y, 250, 60, FOREST_GREEN, GREEN, fonts['small']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200); pygame.event.clear(); return 'settings'

        # Trophy Cabinet (440px)
        if draw_cute_button(screen, lang_manager.get('trophy_cabinet'), 380, bottom_y, 440, 60, FOREST_GREEN, GREEN, fonts['small']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200); pygame.event.clear()
                TrophyCabinet(fonts, lang_manager, db, current_user['id']).show(screen, clock)

        # Leaderboard (250px)
        if draw_cute_button(screen, lang_manager.get('leaderboard'), 900, bottom_y, 250, 60, FOREST_GREEN, GREEN, fonts['small']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200); pygame.event.clear(); return 'leaderboard'

        button_was_pressed = mouse_pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        pygame.display.flip()
        clock.tick(FPS)

        button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


def leaderboard_screen():
    """Show leaderboard with search functionality"""
    pygame.time.wait(200)
    pygame.event.clear()

    button_was_pressed = False
    search_text = ""
    search_active = False

    while True:
        draw_gradient_background(screen, GRADIENTS['menu'][0], GRADIENTS['menu'][1])

        draw_text_with_shadow(screen, lang_manager.get('leaderboard_title'), SCREEN_WIDTH // 2, 60,
                              fonts['large'], GOLD, DARK_BLUE, 4)

        # Search bar
        search_box = pygame.Rect(300, 130, 600, 50)
        search_color = CYAN if search_active else LIGHT_GRAY
        pygame.draw.rect(screen, WHITE, search_box, border_radius=15)
        pygame.draw.rect(screen, search_color, search_box, 4, border_radius=15)

        # Search placeholder or text
        if search_text == "" and not search_active:
            placeholder = lang_manager.get('search_player')
            search_surface = fonts['small'].render(placeholder, True, LIGHT_GRAY)
        else:
            search_surface = fonts['small'].render(search_text, True, BLACK)

        search_rect = search_surface.get_rect(midleft=(search_box.x + 15, search_box.centery))
        screen.blit(search_surface, search_rect)

        # Search icon
        search_icon_text = "🔍"
        try:
            search_icon = fonts['small'].render(search_icon_text, True, GOLD)
            screen.blit(search_icon, (search_box.right - 40, search_box.centery - 15))
        except:
            pass

        # Get leaderboard (filtered or full)
        top_players = db.get_leaderboard(level=None, limit=100)  # Get more results for searching

        # Filter by search text if any
        if search_text:
            filtered_players = [(username, score, correct) for username, score, correct in top_players
                                if search_text.lower() in username.lower()]
        else:
            filtered_players = top_players[:10]  # Show top 10 by default

        # Display results
        y_offset = 210
        max_display = 10

        if len(filtered_players) == 0:
            if search_text:
                no_data_text = lang_manager.get('no_player_found')
            else:
                no_data_text = lang_manager.get('no_scores')

            no_data = fonts['small'].render(no_data_text, True, WHITE)
            no_data_rect = no_data.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 100))
            screen.blit(no_data, no_data_rect)
        else:
            # Display header
            header_box = pygame.Rect(250, y_offset, 700, 40)
            pygame.draw.rect(screen, DARK_BLUE, header_box, border_radius=10)

            header_text = f"{lang_manager.get('rank')}       {lang_manager.get('name')}                    {lang_manager.get('score')}"

            header_surface = fonts['small'].render(header_text, True, GOLD)
            header_rect = header_surface.get_rect(center=header_box.center)
            screen.blit(header_surface, header_rect)

            y_offset += 50

            # Display players
            for i, (username, total_score, total_correct) in enumerate(filtered_players[:max_display], 1):
                # Find actual rank in full leaderboard
                actual_rank = next((idx for idx, (name, _, _) in enumerate(top_players, 1) if name == username), i)

                # Background for each row
                row_box = pygame.Rect(250, y_offset, 700, 45)
                row_color = PURPLE if i % 2 == 0 else DARK_BLUE
                pygame.draw.rect(screen, row_color, row_box, border_radius=10)

                # Highlight if it's the current user
                if current_user and username == current_user['username']:
                    pygame.draw.rect(screen, GOLD, row_box, 4, border_radius=10)

                # Rank number
                rank_surface = fonts['small'].render(f"{actual_rank}.", True, GOLD if actual_rank <= 3 else WHITE)
                screen.blit(rank_surface, (280, y_offset + 10))

                # Username
                name_surface = fonts['small'].render(username, True, WHITE)
                screen.blit(name_surface, (380, y_offset + 10))

                # Score
                score_surface = fonts['small'].render(str(total_score), True, YELLOW)
                screen.blit(score_surface, (780, y_offset + 10))

                y_offset += 50

            # Show count of results
            if search_text:
                count_text = f"{lang_manager.get('found_players')} {len(filtered_players)}"

                count_surface = fonts['tiny'].render(count_text, True, LIGHT_GRAY)
                count_rect = count_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 10))
                screen.blit(count_surface, count_rect)

        # Back button
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if draw_cute_button(screen, lang_manager.get('back'), 450, 700, 300, 60,
                            RED, PINK, fonts['medium']):
            if mouse_pressed and not button_was_pressed:
                pygame.time.wait(200)
                pygame.event.clear()
                return

        button_was_pressed = mouse_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if clicked on search box
                if search_box.collidepoint(event.pos):
                    search_active = True
                else:
                    search_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if search_active:
                        search_active = False
                    else:
                        pygame.time.wait(200)
                        pygame.event.clear()
                        return

                elif search_active:
                    if event.key == pygame.K_RETURN:
                        search_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        search_text = search_text[:-1]
                    else:
                        # Add character to search text
                        if len(search_text) < 20:  # Limit search length
                            search_text += event.unicode

        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Main game loop"""
    global play_session_start

    # Language selection
    language_selection_screen()

    # Login/Register
    login_register_screen()

    # Start play session timer
    play_session_start = time.time()

    # Main loop
    while True:
        # Show main menu
        action = main_menu()

        # Check if settings
        if action == 'settings':
            settings_screen()
            continue

        # Check if leaderboard
        if action == 'leaderboard':
            leaderboard_screen()
            continue

        # Check if valid level number
        if not isinstance(action, int) or action < 1 or action > 5:
            continue

        # User selected a level
        level_num = action

        # Show story
        from story import StoryScreen, TipsScreen
        story = StoryScreen(level_num, fonts['large'], fonts['medium'],
                            fonts['small'], fonts['tiny'], lang_manager)
        story.show(screen, clock)

        # Show tips
        tips = TipsScreen(level_num, fonts['large'], fonts['medium'],
                          fonts['small'], fonts['tiny'], lang_manager)
        tips.show(screen, clock)

        # Choose level type
        if level_num == 1:
            from levels import GameLevel
            level = GameLevel(level_num, 'medium', fonts, lang_manager)
        elif level_num == 2:
            from level2_parkour import ParkourLevel
            level = ParkourLevel(level_num, 'medium', fonts, lang_manager)
        elif level_num == 3:
            from level3_maze import MazeLevel
            level = MazeLevel(level_num, 'medium', fonts, lang_manager)
        elif level_num == 4:
            try:
                from special_levels import SpaceshipLevel
                level = SpaceshipLevel(level_num, 'medium', fonts, lang_manager)
            except:
                from levels import GameLevel
                level = GameLevel(level_num, 'medium', fonts, lang_manager)
        elif level_num == 5:
            try:
                from special_levels import MemoryCardLevel
                level = MemoryCardLevel(level_num, 'medium', fonts, lang_manager)
            except:
                from levels import GameLevel
                level = GameLevel(level_num, 'medium', fonts, lang_manager)

        # Play level
        result = level.run(screen, clock)

        # Save score and COMMIT IMMEDIATELY for point synchronization
        if current_user and isinstance(result, dict):
            db.save_score(
                current_user['id'],
                level_num,
                result.get('score', 0),
                int(result.get('time_taken', 0)),
                result.get('questions_correct', 0),
                result.get('questions_total', 0)
            )
            db.conn.commit()  # Force commit for immediate points update

            # Show medal celebration
            if result.get('score', 0) > 0:
                show_level_complete_animation(screen, clock, fonts, lang_manager, level_num)


if __name__ == '__main__':
    main()