"""
Константи за играта
"""

import pygame
import math

# Екран
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Бои
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (13, 110, 253)
YELLOW = (255, 193, 7)
ORANGE = (253, 126, 20)
PURPLE = (111, 66, 193)
CYAN = (13, 202, 240)
PINK = (214, 51, 132)
GOLD = (255, 215, 0)
DARK_GRAY = (52, 58, 64)
LIGHT_GRAY = (173, 181, 189)
DARK_BLUE = (25, 42, 86)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)

# Градиенти
GRADIENTS = {
    'menu': [(25, 42, 86), (111, 66, 193)],
    'story': [(25, 42, 86), (111, 66, 193)],
    'level1': [(13, 110, 253), (111, 66, 193)],
    'level2': [(253, 126, 20), (220, 53, 69)],
    'level3': [(40, 167, 69), (13, 202, 240)],
    'level4': [(220, 53, 69), (111, 66, 193)],
    'level5': [(111, 66, 193), (214, 51, 132)],
    'results': [(40, 167, 69), (13, 110, 253)]
}

# Играч
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 6
PLAYER_JUMP_POWER = 18
GRAVITY = 0.6
PLAYER_COLOR = RED

# Платформи
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = GREEN
GROUND_HEIGHT = 50

# Препреки
OBSTACLE_WIDTH = 35
OBSTACLE_HEIGHT = 35
OBSTACLE_COLORS = {
    'spike': RED,
    'virus': PURPLE,
    'hacker': DARK_BLUE,
    'phishing': ORANGE,
    'malware': PINK
}

# Collectibles
COIN_RADIUS = 15
SHIELD_SIZE = 25

# Поени
POINTS = {
    'coin': 10,
    'shield': 15,
    'quiz_correct': 30,
    'quiz_wrong': 0,
    'enemy_defeat': 20,
    'hit_obstacle': 0,
    'level_complete': 100
}

# Invincibility
INVINCIBILITY_FRAMES = 180

# Тајмер - INCREASED (in seconds)
LEVEL_TIME_LIMITS = {
    'easy': 600,    # 10 minutes
    'medium': 480,  # 8 minutes
    'hard': 360     # 6 minutes
}

# Фонтови - BIGGER
FONT_SIZES = {
    'title': 96,
    'large': 64,
    'medium': 48,
    'small': 32,
    'tiny': 24,
    'mini': 20
}

# Прашања по ниво
QUESTIONS_PER_LEVEL = {
    'easy': 5,
    'medium': 7,
    'hard': 10
}

# Тежини
DIFFICULTIES = {
    'easy': {
        'name': 'Лесно / E Lehtë',
        'description': 'Повеќе време, помалку непријатели',
        'time_multiplier': 1.5,
        'questions_per_level': 5,
        'enemies': 3,
        'platforms': 8
    },
    'medium': {
        'name': 'Средно / Mesatare',
        'description': 'Балансирана игра за сите',
        'time_multiplier': 1.0,
        'questions_per_level': 7,
        'enemies': 5,
        'platforms': 10
    },
    'hard': {
        'name': 'Тешко / E Vështirë',
        'description': 'Малку време, многу непријатели!',
        'time_multiplier': 0.75,
        'questions_per_level': 10,
        'enemies': 7,
        'platforms': 12
    }
}

# Ранкови
RANK_THRESHOLDS = [
    {'min': 0, 'max': 199, 'name': 'Почетник', 'stars': 1, 'color': (205, 127, 50)},
    {'min': 200, 'max': 399, 'name': 'Ученик', 'stars': 2, 'color': (192, 192, 192)},
    {'min': 400, 'max': 599, 'name': 'Напреден', 'stars': 3, 'color': GOLD},
    {'min': 600, 'max': 799, 'name': 'Експерт', 'stars': 4, 'color': CYAN},
    {'min': 800, 'max': 9999, 'name': 'Мајстор', 'stars': 5, 'color': PURPLE}
]

# Additional constants
MAX_SCORES = {1: 200, 2: 200, 3: 200, 4: 200, 5: 200}
RANKS = RANK_THRESHOLDS

# Level types - Different gameplay for each level
LEVEL_TYPES = {
    1: 'platformer',  # Traditional platformer
    2: 'parkour',     # Parkour with jumps
    3: 'maze',        # Maze navigation
    4: 'runner',      # Auto-runner style
    5: 'mixed'        # Mixed challenges
}

# Trophy Cabinet / Achievements
CONFETTI_COUNT = 150  # Number of confetti particles in celebration