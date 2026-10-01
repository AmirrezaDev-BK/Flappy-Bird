"""
config.py
=========
Global configuration for Flappy Bird game.
Contains all constants: window size, colors, physics, UI text,
difficulty, buttons, and modern UI palette.
"""

import os

# ============================================
# WINDOW SETTINGS
# ============================================
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Flappy Bird"

# ============================================
# COLORS (R, G, B) — Modern Palette
# ============================================

# Sky gradient (top -> bottom)
SKY_TOP = (78, 168, 222)
SKY_BOTTOM = (173, 226, 240)

# Ground
GROUND_SAND = (222, 216, 149)
GROUND_LINE = (100, 90, 60)
GROUND_DARK = (180, 174, 110)

# Pipes
PIPE_GREEN = (106, 190, 48)
PIPE_GREEN_DARK = (70, 130, 30)
PIPE_OUTLINE = (40, 80, 20)
PIPE_HIGHLIGHT = (150, 220, 90)

# Text
TEXT_WHITE = (255, 255, 255)
TEXT_BLACK = (0, 0, 0)
TEXT_YELLOW = (255, 220, 50)
TEXT_SHADOW = (30, 30, 30)
TEXT_MUTED = (200, 200, 200)

# UI overlay
UI_OVERLAY = (0, 0, 0, 160)

# Buttons (modern rounded)
BUTTON_BG = (52, 120, 200)
BUTTON_BG_HOVER = (82, 155, 235)
BUTTON_BG_ACTIVE = (30, 90, 160)
BUTTON_BORDER = (255, 255, 255)
BUTTON_TEXT = (255, 255, 255)
BUTTON_SHADOW = (20, 50, 90)

# Pause button (floating on game screen)
PAUSE_BTN_BG = (0, 0, 0, 120)
PAUSE_BTN_HOVER = (0, 0, 0, 180)

# Music card (Now Playing)
CARD_BG = (35, 55, 85)
CARD_BORDER = (100, 160, 220)
CARD_TEXT = (240, 245, 255)
CARD_TEXT_MUTED = (160, 180, 210)

# Progress bar
PROGRESS_BG = (50, 70, 100)
PROGRESS_FILL = (100, 200, 255)

# Playlist items
LIST_ITEM_BG = (40, 60, 90)
LIST_ITEM_ACTIVE = (70, 120, 180)
LIST_ITEM_TEXT = (220, 230, 245)

# Music control buttons
MUSIC_BTN_BG = (60, 90, 140)
MUSIC_BTN_HOVER = (90, 130, 190)
MUSIC_BTN_ACTIVE = (110, 220, 140)

# ============================================
# BUTTON SETTINGS
# ============================================
BUTTON_WIDTH = 320
BUTTON_HEIGHT = 60
BUTTON_PADDING = 18
BUTTON_RADIUS = 14

MUSIC_CTRL_SIZE = 56
MUSIC_CTRL_SPACING = 12

# ============================================
# BIRD SETTINGS
# ============================================
BIRD_WIDTH = 45
BIRD_HEIGHT = 35
BIRD_START_X = 100
BIRD_START_Y = SCREEN_HEIGHT // 2
BIRD_GRAVITY = 0.5
BIRD_FLAP_STRENGTH = -8.5
BIRD_MAX_FALL_SPEED = 12
BIRD_MAX_RISE_SPEED = -12
BIRD_ROTATION_FACTOR = 3

# ============================================
# PIPE SETTINGS
# ============================================
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3
PIPE_SPAWN_DISTANCE = 220
PIPE_MIN_TOP = 80
PIPE_MAX_TOP = SCREEN_HEIGHT - 300
PIPE_CAP_HEIGHT = 30

# ============================================
# GROUND SETTINGS
# ============================================
GROUND_HEIGHT = 80

# ============================================
# DIFFICULTY PROFILES
# ============================================
DIFFICULTY_PROFILES = {
    "Easy": {"gap": 220, "speed": 2.0, "gravity": 0.40},
    "Medium": {"gap": 180, "speed": 3.0, "gravity": 0.50},
    "Hard": {"gap": 140, "speed": 4.5, "gravity": 0.70},
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]
DIFFICULTY_DEFAULT = "Medium"

# ============================================
# GAME STATE IDENTIFIERS
# ============================================
STATE_MENU = "menu"
STATE_HOW_TO_PLAY = "how_to_play"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_MUSIC = "music"

# ============================================
# UI TEXT (English)
# ============================================

# Main Menu
GAME_TITLE = "FLAPPY BIRD"
GAME_SUBTITLE = "Tap to fly. Don't crash."
MENU_START = "Start Game"
MENU_HOW_TO_PLAY = "How to Play"
MENU_DIFFICULTY = "Difficulty"
MENU_MUSIC = "Music"
MENU_QUIT = "Quit"

# How to Play
HOW_TO_PLAY_TITLE = "HOW TO PLAY"
HOW_TO_PLAY_LINES = [
    "Tap anywhere or press SPACE to flap",
    "Avoid the pipes and the ground",
    "Each pipe you pass = +1 point",
    "",
    "P / Pause button  -  Pause the game",
    "S / Stop button   -  Stop music",
    "Left / Right      -  Change track",
    "F                 -  Toggle fullscreen",
    "D                 -  Change difficulty",
    "",
    "Tap BACK to return to menu",
]

# In-game HUD
HUD_SCORE_LABEL = "Score"

# Pause screen
PAUSED_TITLE = "PAUSED"
PAUSED_RESUME = "Resume"
PAUSED_MENU = "Main Menu"

# Game Over
GAME_OVER_TITLE = "GAME OVER"
GAME_OVER_SCORE = "Score"
GAME_OVER_RESTART = "Play Again"
GAME_OVER_MENU = "Main Menu"

# Music Screen
MUSIC_TITLE = "MUSIC"
MUSIC_NOW_PLAYING = "NOW PLAYING"
MUSIC_NO_TRACK = "No track loaded"
MUSIC_PLAYLIST = "Playlist"
MUSIC_EMPTY = "No music added yet. Tap + to add files."
MUSIC_ADD_BUTTON = "+  Add Music"
MUSIC_BACK_BUTTON = "Back"
MUSIC_LOOP_ON = "Loop: ON"
MUSIC_LOOP_OFF = "Loop: OFF"

# Music bar
MUSIC_BAR_NO_TRACK = "No music selected"

# ============================================
# FONT SIZES
# ============================================
FONT_TITLE = 56
FONT_LARGE = 36
FONT_MEDIUM = 26
FONT_SMALL = 20
FONT_TINY = 16

# ============================================
# ASSET PATHS
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIRD_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "bird.png")
