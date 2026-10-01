"""
ui.py
=====
Modern UI: rounded buttons with icons, cards, progress bar (clickable),
gradient background, music player screen, and touch support.
"""

import pygame
import config


# ============================================
# FONT CACHE
# ============================================
_font_cache = {}


def get_font(size):
    """Return a cached default font at the given size."""
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]


# ============================================
# BASIC HELPERS
# ============================================


def draw_text_centered(surface, text, size, y, color=config.TEXT_WHITE):
    """Draw a single line of text centered horizontally at given Y."""
    font = get_font(size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(config.SCREEN_WIDTH // 2, y))
    surface.blit(rendered, rect)


def draw_text_with_shadow(surface, text, size, y, color=config.TEXT_WHITE):
    """Draw centered text with a small drop shadow."""
    font = get_font(size)
    shadow = font.render(text, True, config.TEXT_SHADOW)
    main = font.render(text, True, color)
    cx = config.SCREEN_WIDTH // 2
    surface.blit(shadow, shadow.get_rect(center=(cx + 2, y + 2)))
    surface.blit(main, main.get_rect(center=(cx, y)))


def draw_gradient_bg(surface):
    """Draw a vertical sky gradient covering the whole screen."""
    top = config.SKY_TOP
    bottom = config.SKY_BOTTOM
    height = config.SCREEN_HEIGHT
    width = config.SCREEN_WIDTH

    for y in range(height):
        t = y / height
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def draw_overlay(surface, alpha=160):
    """Draw a semi-transparent black overlay."""
    overlay = pygame.Surface(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))


def draw_rounded_rect(surface, color, rect, radius, border_color=None, border_width=0):
    """Draw a rounded rectangle with optional border."""
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border_color and border_width > 0:
        pygame.draw.rect(
            surface, border_color, rect, border_width, border_radius=radius
        )


# ============================================
# BUTTON CLASS
# ============================================


class Button:
    """A clickable, rounded button with hover, shadow, and optional icon."""

    def __init__(
        self,
        center_x,
        center_y,
        label,
        action,
        width=None,
        height=None,
        icon=None,
        bg=None,
        bg_hover=None,
        text_color=None,
        radius=None,
    ):
        self.label = label
        self.action = action
        self.icon = icon

        w = width if width is not None else config.BUTTON_WIDTH
        h = height if height is not None else config.BUTTON_HEIGHT
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (center_x, center_y)

        self.bg = bg if bg is not None else config.BUTTON_BG
        self.bg_hover = bg_hover if bg_hover is not None else config.BUTTON_BG_HOVER
        self.text_color = text_color if text_color is not None else config.BUTTON_TEXT
        self.radius = radius if radius is not None else config.BUTTON_RADIUS

        self.is_hovered = False

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface):
        # Shadow
        shadow_rect = self.rect.move(0, 4)
        shadow_surf = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surf,
            (0, 0, 0, 90),
            shadow_surf.get_rect(),
            border_radius=self.radius,
        )
        surface.blit(shadow_surf, shadow_rect.topleft)

        # Background
        color = self.bg_hover if self.is_hovered else self.bg
        draw_rounded_rect(surface, color, self.rect, self.radius)

        # Border
        draw_rounded_rect(
            surface,
            color,
            self.rect,
            self.radius,
            border_color=config.BUTTON_BORDER,
            border_width=2,
        )

        # Icon
        icon_w = 0
        if self.icon:
            icon_w = self._draw_icon(surface)

        # Label
        font = get_font(config.FONT_MEDIUM)
        rendered = font.render(self.label, True, self.text_color)
        total_w = rendered.get_width() + (icon_w + 10 if icon_w else 0)
        start_x = self.rect.centerx - total_w // 2

        if icon_w:
            surface.blit(
                rendered,
                (start_x + icon_w + 10, self.rect.centery - rendered.get_height() // 2),
            )
        else:
            surface.blit(
                rendered, (start_x, self.rect.centery - rendered.get_height() // 2)
            )

    def _draw_icon(self, surface):
        size = 22
        cx = self.rect.x + 22
        cy = self.rect.centery

        if self.icon == "play":
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx - 6, cy - 9), (cx - 6, cy + 9), (cx + 10, cy)],
            )
        elif self.icon == "stop":
            pygame.draw.rect(surface, self.text_color, (cx - 7, cy - 7, 14, 14))
        elif self.icon == "pause":
            pygame.draw.rect(surface, self.text_color, (cx - 7, cy - 8, 5, 16))
            pygame.draw.rect(surface, self.text_color, (cx + 2, cy - 8, 5, 16))
        elif self.icon == "prev":
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx + 6, cy - 9), (cx + 6, cy + 9), (cx - 6, cy)],
            )
            pygame.draw.rect(surface, self.text_color, (cx - 10, cy - 9, 4, 18))
        elif self.icon == "next":
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx - 6, cy - 9), (cx - 6, cy + 9), (cx + 6, cy)],
            )
            pygame.draw.rect(surface, self.text_color, (cx + 6, cy - 9, 4, 18))
        elif self.icon == "plus":
            pygame.draw.rect(surface, self.text_color, (cx - 10, cy - 2, 20, 4))
            pygame.draw.rect(surface, self.text_color, (cx - 2, cy - 10, 4, 20))
        elif self.icon == "back":
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx + 8, cy - 9), (cx + 8, cy + 9), (cx - 8, cy)],
            )
        elif self.icon == "home":
            pygame.draw.polygon(
                surface, self.text_color, [(cx, cy - 10), (cx - 10, cy), (cx + 10, cy)]
            )
            pygame.draw.rect(surface, self.text_color, (cx - 7, cy, 14, 10))
        elif self.icon == "music":
            pygame.draw.circle(surface, self.text_color, (cx - 4, cy + 6), 4)
            pygame.draw.rect(surface, self.text_color, (cx - 1, cy - 10, 3, 16))
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx + 2, cy - 10), (cx + 10, cy - 6), (cx + 2, cy - 2)],
            )
        elif self.icon == "loop":
            pygame.draw.circle(surface, self.text_color, (cx, cy), 9, 3)
            pygame.draw.polygon(
                surface,
                self.text_color,
                [(cx + 6, cy - 10), (cx + 12, cy - 5), (cx + 4, cy - 4)],
            )

        return size


# ============================================
# PROGRESS BAR CLASS (clickable)
# ============================================


class ProgressBar:
    """A clickable progress bar for the Now Playing card."""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def is_clicked(self, pos):
        """Return True if the given position is on the bar."""
        return self.rect.collidepoint(pos)

    def get_ratio(self, pos):
        """Return the click ratio [0.0, 1.0] along the bar."""
        ratio = (pos[0] - self.rect.x) / self.rect.width
        return max(0.0, min(1.0, ratio))


# ============================================
# BUTTON BUILDERS
# ============================================


def build_main_menu_buttons():
    """Buttons for the main menu (Start / How / Music / Difficulty / Quit)."""
    cx = config.SCREEN_WIDTH // 2
    y = 320
    step = config.BUTTON_HEIGHT + config.BUTTON_PADDING
    return [
        Button(cx, y, config.MENU_START, "start", icon="play"),
        Button(cx, y + step, config.MENU_HOW_TO_PLAY, "how_to_play"),
        Button(cx, y + step * 2, config.MENU_MUSIC, "music", icon="music"),
        Button(cx, y + step * 3, config.MENU_DIFFICULTY, "difficulty"),
        Button(cx, y + step * 4, config.MENU_QUIT, "quit"),
    ]


def build_game_over_buttons():
    """Buttons for the game over screen."""
    cx = config.SCREEN_WIDTH // 2
    y = 470
    step = config.BUTTON_HEIGHT + config.BUTTON_PADDING
    return [
        Button(cx, y, config.GAME_OVER_RESTART, "play_again", icon="play"),
        Button(cx, y + step, config.GAME_OVER_MENU, "main_menu", icon="home"),
    ]


def build_pause_buttons():
    """Buttons for the pause screen (Resume / Music / Main Menu)."""
    cx = config.SCREEN_WIDTH // 2
    y = 340
    step = config.BUTTON_HEIGHT + config.BUTTON_PADDING
    return [
        Button(cx, y, config.PAUSED_RESUME, "resume", icon="play"),
        Button(cx, y + step, "Music", "open_music", icon="music"),
        Button(cx, y + step * 2, config.PAUSED_MENU, "main_menu", icon="home"),
    ]


def build_music_screen_buttons():
    """Buttons for the music screen: controls + add + back."""
    cx = config.SCREEN_WIDTH // 2

    row_y = 260
    size = config.MUSIC_CTRL_SIZE
    spacing = config.MUSIC_CTRL_SPACING
    total_w = size * 5 + spacing * 4
    start_x = cx - total_w // 2 + size // 2

    controls = [
        Button(start_x, row_y, "", "prev", width=size, height=size, icon="prev"),
        Button(
            start_x + (size + spacing),
            row_y,
            "",
            "play",
            width=size,
            height=size,
            icon="play",
        ),
        Button(
            start_x + (size + spacing) * 2,
            row_y,
            "",
            "stop",
            width=size,
            height=size,
            icon="stop",
        ),
        Button(
            start_x + (size + spacing) * 3,
            row_y,
            "",
            "next",
            width=size,
            height=size,
            icon="next",
        ),
        Button(
            start_x + (size + spacing) * 4,
            row_y,
            "",
            "loop",
            width=size,
            height=size,
            icon="loop",
        ),
    ]

    add_btn = Button(
        cx,
        config.SCREEN_HEIGHT - 180,
        config.MUSIC_ADD_BUTTON,
        "add_music",
        icon="plus",
        width=260,
    )

    back_btn = Button(
        70, 50, config.MUSIC_BACK_BUTTON, "back", icon="back", width=110, height=44
    )

    return controls + [add_btn, back_btn], controls, add_btn, back_btn


def build_progress_bar():
    """Build the clickable progress bar matching the Now Playing card."""
    card_x = 40
    card_y = 90
    card_w = config.SCREEN_WIDTH - 80
    bar_x = card_x + 16
    bar_y = card_y + 78
    bar_w = card_w - 32
    bar_h = 10
    return ProgressBar(bar_x, bar_y, bar_w, bar_h)


# ============================================
# SCREEN: MAIN MENU
# ============================================


def draw_main_menu(surface, buttons, difficulty):
    """Draw the main menu with title, subtitle, and buttons."""
    draw_text_with_shadow(
        surface, config.GAME_TITLE, config.FONT_TITLE, 120, config.TEXT_YELLOW
    )
    draw_text_centered(
        surface, config.GAME_SUBTITLE, config.FONT_SMALL, 170, config.TEXT_MUTED
    )

    for btn in buttons:
        if btn.action == "difficulty":
            btn.label = f"{config.MENU_DIFFICULTY}: {difficulty}"
        btn.draw(surface)


# ============================================
# SCREEN: HOW TO PLAY
# ============================================


def draw_how_to_play(surface, back_button):
    """Draw the How to Play screen with a back button."""
    draw_text_with_shadow(
        surface, config.HOW_TO_PLAY_TITLE, config.FONT_LARGE, 70, config.TEXT_YELLOW
    )

    y = 150
    for line in config.HOW_TO_PLAY_LINES:
        if line:
            draw_text_centered(surface, line, config.FONT_SMALL, y)
        y += 32

    back_button.draw(surface)


# ============================================
# SCREEN: PAUSE
# ============================================


def draw_pause_screen(surface, buttons):
    """Draw the pause overlay with title and buttons."""
    draw_overlay(surface, alpha=180)
    draw_text_with_shadow(
        surface, config.PAUSED_TITLE, config.FONT_TITLE, 240, config.TEXT_YELLOW
    )
    for btn in buttons:
        btn.draw(surface)


# ============================================
# SCREEN: GAME OVER
# ============================================


def draw_game_over(surface, score, buttons):
    """Draw the game over overlay with score and buttons."""
    draw_overlay(surface, alpha=180)
    draw_text_with_shadow(
        surface, config.GAME_OVER_TITLE, config.FONT_TITLE, 250, config.TEXT_YELLOW
    )
    draw_text_with_shadow(
        surface,
        f"{config.GAME_OVER_SCORE}: {score}",
        config.FONT_LARGE,
        335,
        config.TEXT_WHITE,
    )
    for btn in buttons:
        btn.draw(surface)


# ============================================
# IN-GAME HUD
# ============================================


def draw_hud(surface, score):
    """Draw score at top center during gameplay."""
    draw_text_with_shadow(surface, f"{score}", config.FONT_TITLE, 70)


def draw_pause_icon_button(surface, rect, hovered):
    """Draw the floating pause button on the game screen."""
    color = config.PAUSE_BTN_HOVER if hovered else config.PAUSE_BTN_BG

    btn_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, color, btn_surf.get_rect(), border_radius=10)
    surface.blit(btn_surf, rect.topleft)

    cx, cy = rect.center
    pygame.draw.rect(surface, (255, 255, 255), (cx - 7, cy - 9, 5, 18))
    pygame.draw.rect(surface, (255, 255, 255), (cx + 2, cy - 9, 5, 18))


# ============================================
# MUSIC SCREEN
# ============================================


def draw_music_screen(
    surface, music_manager, controls, add_btn, back_btn, list_items, progress_bar
):
    """Draw the modern music screen: card + controls + playlist."""
    draw_text_with_shadow(
        surface, config.MUSIC_TITLE, config.FONT_LARGE, 50, config.TEXT_YELLOW
    )

    # Now Playing card
    card_x = 40
    card_y = 90
    card_w = config.SCREEN_WIDTH - 80
    card_h = 120
    card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

    draw_rounded_rect(surface, config.CARD_BG, card_rect, 14)
    draw_rounded_rect(
        surface,
        config.CARD_BG,
        card_rect,
        14,
        border_color=config.CARD_BORDER,
        border_width=2,
    )

    font_small = get_font(config.FONT_TINY)
    lbl = font_small.render(config.MUSIC_NOW_PLAYING, True, config.CARD_TEXT_MUTED)
    surface.blit(lbl, (card_x + 16, card_y + 12))

    # Track name
    track = music_manager.get_current_track()
    font_med = get_font(config.FONT_MEDIUM)
    if track:
        name = track["name"]
        if len(name) > 30:
            name = name[:27] + "..."
        name_surf = font_med.render(name, True, config.CARD_TEXT)
    else:
        name_surf = font_med.render(config.MUSIC_NO_TRACK, True, config.CARD_TEXT_MUTED)
    surface.blit(name_surf, (card_x + 16, card_y + 34))

    # Progress bar (from ProgressBar object)
    bar_rect = progress_bar.rect
    draw_rounded_rect(surface, config.PROGRESS_BG, bar_rect, 5)

    progress = music_manager.get_progress()
    fill_w = int(bar_rect.width * progress)
    if fill_w > 0:
        fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_w, bar_rect.height)
        draw_rounded_rect(surface, config.PROGRESS_FILL, fill_rect, 5)

    # Time + Loop status
    time_surf = font_small.render(
        music_manager.get_time_string(), True, config.CARD_TEXT_MUTED
    )
    surface.blit(time_surf, (card_x + 16, card_y + 92))

    if track:
        loop_txt = config.MUSIC_LOOP_ON if track["loop"] else config.MUSIC_LOOP_OFF
        loop_color = (
            config.MUSIC_BTN_ACTIVE if track["loop"] else config.CARD_TEXT_MUTED
        )
        loop_surf = font_small.render(loop_txt, True, loop_color)
        surface.blit(
            loop_surf, (card_x + card_w - loop_surf.get_width() - 16, card_y + 92)
        )

    # Controls
    for ctrl in controls:
        ctrl.draw(surface)

    # Playlist header
    draw_text_centered(surface, config.MUSIC_PLAYLIST, config.FONT_MEDIUM, 320)

    # Playlist items
    if not music_manager.has_playlist():
        draw_text_centered(surface, config.MUSIC_EMPTY, config.FONT_SMALL, 380)
    else:
        font_item = get_font(config.FONT_SMALL)
        for item in list_items:
            item.draw(surface, font_item, music_manager)

    # Add + Back
    add_btn.draw(surface)
    back_btn.draw(surface)


class PlaylistItem:
    """A clickable playlist row."""

    def __init__(self, index, y):
        self.index = index
        self.rect = pygame.Rect(40, y, config.SCREEN_WIDTH - 80, 40)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface, font, music_manager):
        """Draw this playlist item."""
        is_active = self.index == music_manager.current_index
        bg = config.LIST_ITEM_ACTIVE if is_active else config.LIST_ITEM_BG
        draw_rounded_rect(surface, bg, self.rect, 8)

        track = music_manager.playlist[self.index]
        marker = ">" if is_active else " "
        name = track["name"]
        if len(name) > 32:
            name = name[:29] + "..."
        line = f"{marker}  {self.index + 1}.  {name}"
        text = font.render(line, True, config.LIST_ITEM_TEXT)
        surface.blit(
            text, (self.rect.x + 12, self.rect.centery - text.get_height() // 2)
        )


def build_playlist_items(music_manager):
    """Build a list of PlaylistItem objects for the current playlist."""
    items = []
    start_y = 360
    item_h = 46
    max_items = 5

    for i in range(min(len(music_manager.playlist), max_items)):
        items.append(PlaylistItem(i, start_y + i * item_h))
    return items


# ============================================
# MUSIC BAR (during gameplay)
# ============================================


def draw_music_bar(surface, music_manager):
    """Draw a slim music status bar at the bottom (during gameplay only)."""
    bar_height = 34
    bar_y = config.SCREEN_HEIGHT - bar_height

    bar_surf = pygame.Surface((config.SCREEN_WIDTH, bar_height), pygame.SRCALPHA)
    bar_surf.fill((0, 0, 0, 130))
    surface.blit(bar_surf, (0, bar_y))

    pygame.draw.line(
        surface, (255, 255, 255, 60), (0, bar_y), (config.SCREEN_WIDTH, bar_y), 1
    )

    font = get_font(config.FONT_TINY)
    text = music_manager.get_status_text()
    rendered = font.render(text, True, config.TEXT_WHITE)
    rect = rendered.get_rect(center=(config.SCREEN_WIDTH // 2, bar_y + bar_height // 2))
    surface.blit(rendered, rect)
