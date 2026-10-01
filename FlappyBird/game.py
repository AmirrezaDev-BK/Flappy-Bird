"""
game.py
=======
Core game logic and state machine (modern version).
Manages bird, pipes, ground, score, difficulty, buttons, pause,
touch/mouse input, fullscreen toggle, music screen with return state,
and clickable progress bar.
"""

import pygame
import config
from bird import Bird
from pipe import PipeManager
from music import MusicManager
import ui


class Game:
    """Main game object: holds state and runs the update/draw loop."""

    def __init__(self, screen):
        """Initialize game objects, state, and buttons."""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Game objects
        self.bird = Bird()
        self.pipes = PipeManager()
        self.music = MusicManager()

        # State
        self.state = config.STATE_MENU
        self.difficulty = config.DIFFICULTY_DEFAULT

        # Score (in-memory)
        self.score = 0
        self.high_score = 0

        # Ground scroll offset
        self.ground_offset = 0

        # Fullscreen flag
        self.is_fullscreen = False

        # ---- Buttons per screen ----
        self.menu_buttons = ui.build_main_menu_buttons()
        self.pause_buttons = ui.build_pause_buttons()
        self.game_over_buttons = ui.build_game_over_buttons()

        # Music screen buttons
        (
            self.music_buttons_all,
            self.music_controls,
            self.music_add_btn,
            self.music_back_btn,
        ) = ui.build_music_screen_buttons()

        # Clickable progress bar for the music screen
        self.music_progress_bar = ui.build_progress_bar()

        # Where the Music screen was opened from
        # (so Back returns to the right place)
        self.music_return_state = config.STATE_MENU

        # Playlist items (rebuilt on entering music screen)
        self.playlist_items = []

        # How to Play back button
        self.how_to_play_back_btn = ui.Button(
            70, 50, "Back", "back", icon="back", width=110, height=44
        )

        # Floating pause button on the game screen (top-right)
        self.pause_icon_rect = pygame.Rect(config.SCREEN_WIDTH - 60, 20, 44, 44)
        self.pause_icon_hovered = False

    # ============================================
    # DIFFICULTY
    # ============================================

    def cycle_difficulty(self):
        """Cycle Easy -> Medium -> Hard -> Easy."""
        idx = config.DIFFICULTY_ORDER.index(self.difficulty)
        idx = (idx + 1) % len(config.DIFFICULTY_ORDER)
        self.difficulty = config.DIFFICULTY_ORDER[idx]

    def apply_difficulty(self):
        """Apply current difficulty to bird and pipes."""
        profile = config.DIFFICULTY_PROFILES[self.difficulty]
        self.bird.set_difficulty(profile["gravity"], config.BIRD_FLAP_STRENGTH)
        self.pipes.set_difficulty(
            gap=profile["gap"],
            speed=profile["speed"],
            spawn_distance=config.PIPE_SPAWN_DISTANCE,
        )

    # ============================================
    # FULLSCREEN
    # ============================================

    def toggle_fullscreen(self):
        """Toggle between resizable window and fullscreen."""
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
                pygame.SCALED | pygame.FULLSCREEN,
            )
        else:
            self.screen = pygame.display.set_mode(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
                pygame.SCALED | pygame.RESIZABLE,
            )

    # ============================================
    # GAME FLOW
    # ============================================

    def start_game(self):
        """Start a fresh game with current difficulty."""
        self.bird.reset()
        self.pipes.reset()
        self.apply_difficulty()
        self.score = 0
        self.state = config.STATE_PLAYING

    def die(self):
        """Handle bird death: update high score, switch to game over."""
        if self.score > self.high_score:
            self.high_score = self.score
        self.state = config.STATE_GAME_OVER

    def back_to_menu(self):
        """Return to main menu and reset current score."""
        self.score = 0
        self.state = config.STATE_MENU

    def enter_music_screen(self, from_state=config.STATE_MENU):
        """Prepare and enter music screen. Remembers where we came from."""
        self.music_return_state = from_state
        self.refresh_playlist_items()
        self.state = config.STATE_MUSIC

    def refresh_playlist_items(self):
        """Rebuild playlist item rectangles from current playlist."""
        self.playlist_items = ui.build_playlist_items(self.music)

    # ============================================
    # EVENT HANDLING
    # ============================================

    def handle_events(self):
        """Process all input events."""
        mouse_pos = pygame.mouse.get_pos()
        self.pause_icon_hovered = self.pause_icon_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            # ---- Mouse / touch ----
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
                continue

            # ---- Keyboard ----
            if event.type != pygame.KEYDOWN:
                continue

            key = event.key

            # Fullscreen (F)
            if key == pygame.K_f:
                self.toggle_fullscreen()
                continue

            # Global music controls
            if key == pygame.K_s:
                self.music.stop()
                continue
            if key == pygame.K_LEFT:
                self.music.previous()
                continue
            if key == pygame.K_RIGHT:
                self.music.next()
                continue

            # Per-state keyboard
            if self.state == config.STATE_MENU:
                self._handle_menu_key(key)
            elif self.state == config.STATE_HOW_TO_PLAY:
                self._handle_how_to_play_key(key)
            elif self.state == config.STATE_PLAYING:
                self._handle_playing_key(key)
            elif self.state == config.STATE_PAUSED:
                self._handle_paused_key(key)
            elif self.state == config.STATE_GAME_OVER:
                self._handle_game_over_key(key)
            elif self.state == config.STATE_MUSIC:
                self._handle_music_key(key)

        # Update hover states
        self._update_hover(mouse_pos)

    # ---------- Keyboard handlers ----------

    def _handle_menu_key(self, key):
        if key == pygame.K_SPACE:
            self.start_game()
        elif key == pygame.K_h:
            self.state = config.STATE_HOW_TO_PLAY
        elif key == pygame.K_d:
            self.cycle_difficulty()
        elif key == pygame.K_m:
            self.enter_music_screen(config.STATE_MENU)
        elif key == pygame.K_ESCAPE:
            self.running = False

    def _handle_how_to_play_key(self, key):
        if key == pygame.K_ESCAPE:
            self.state = config.STATE_MENU
        elif key == pygame.K_d:
            self.cycle_difficulty()

    def _handle_playing_key(self, key):
        if key == pygame.K_SPACE:
            self.bird.flap()
        elif key == pygame.K_p:
            self.state = config.STATE_PAUSED

    def _handle_paused_key(self, key):
        if key == pygame.K_p:
            self.state = config.STATE_PLAYING
        elif key == pygame.K_ESCAPE:
            self.back_to_menu()

    def _handle_game_over_key(self, key):
        if key == pygame.K_SPACE:
            self.start_game()
        elif key == pygame.K_ESCAPE:
            self.back_to_menu()

    def _handle_music_key(self, key):
        if key == pygame.K_SPACE:
            self.music.toggle_play_stop()
        elif key == pygame.K_l:
            self.music.toggle_loop()
        elif key == pygame.K_a:
            self.music.add_tracks()
            self.refresh_playlist_items()
        elif key == pygame.K_ESCAPE:
            self.state = self.music_return_state

    # ---------- Click dispatcher ----------

    def _handle_click(self, pos):
        """Dispatch mouse/touch click to the active screen."""
        if self.state == config.STATE_MENU:
            self._click_buttons(self.menu_buttons, pos)

        elif self.state == config.STATE_HOW_TO_PLAY:
            if self.how_to_play_back_btn.is_clicked(pos):
                self.state = config.STATE_MENU

        elif self.state == config.STATE_PLAYING:
            # Floating pause button?
            if self.pause_icon_rect.collidepoint(pos):
                self.state = config.STATE_PAUSED
            else:
                # Tap anywhere = flap
                self.bird.flap()

        elif self.state == config.STATE_PAUSED:
            self._click_buttons(self.pause_buttons, pos)

        elif self.state == config.STATE_GAME_OVER:
            self._click_buttons(self.game_over_buttons, pos)

        elif self.state == config.STATE_MUSIC:
            self._click_music_screen(pos)

    def _click_music_screen(self, pos):
        """Handle clicks on the music screen."""
        # Progress bar (seek)
        if self.music_progress_bar.is_clicked(pos):
            ratio = self.music_progress_bar.get_ratio(pos)
            track = self.music.get_current_track()
            if track and track.get("duration", 0) > 0:
                target = ratio * track["duration"]
                self.music.seek(target)
            return

        # Controls (prev / play / stop / next / loop)
        for btn in self.music_controls:
            if btn.is_clicked(pos):
                self._run_action(btn.action)
                return

        # Playlist items
        for item in self.playlist_items:
            if item.is_clicked(pos):
                self.music.select_track(item.index)
                return

        # Add / Back
        if self.music_add_btn.is_clicked(pos):
            self.music.add_tracks()
            self.refresh_playlist_items()
            return
        if self.music_back_btn.is_clicked(pos):
            self.state = self.music_return_state
            return

    def _click_buttons(self, buttons, pos):
        """Find and run the clicked button."""
        for btn in buttons:
            if btn.is_clicked(pos):
                self._run_action(btn.action)
                return

    def _run_action(self, action):
        """Execute a button's action identifier."""
        if action == "start":
            self.start_game()
        elif action == "how_to_play":
            self.state = config.STATE_HOW_TO_PLAY
        elif action == "music":
            self.enter_music_screen(config.STATE_MENU)
        elif action == "open_music":
            self.enter_music_screen(config.STATE_PAUSED)
        elif action == "difficulty":
            self.cycle_difficulty()
        elif action == "quit":
            self.running = False
        elif action == "resume":
            self.state = config.STATE_PLAYING
        elif action == "main_menu":
            self.back_to_menu()
        elif action == "play_again":
            self.start_game()
        elif action == "back":
            self.state = self.music_return_state
        # Music controls
        elif action == "play":
            self.music.toggle_play_stop()
        elif action == "stop":
            self.music.stop()
        elif action == "prev":
            self.music.previous()
        elif action == "next":
            self.music.next()
        elif action == "loop":
            self.music.toggle_loop()
        elif action == "add_music":
            self.music.add_tracks()
            self.refresh_playlist_items()

    # ---------- Hover update ----------

    def _update_hover(self, mouse_pos):
        """Update hover state for all visible buttons."""
        if self.state == config.STATE_MENU:
            for b in self.menu_buttons:
                b.update_hover(mouse_pos)

        elif self.state == config.STATE_HOW_TO_PLAY:
            self.how_to_play_back_btn.update_hover(mouse_pos)

        elif self.state == config.STATE_PAUSED:
            for b in self.pause_buttons:
                b.update_hover(mouse_pos)

        elif self.state == config.STATE_GAME_OVER:
            for b in self.game_over_buttons:
                b.update_hover(mouse_pos)

        elif self.state == config.STATE_MUSIC:
            for b in self.music_controls:
                b.update_hover(mouse_pos)
            self.music_add_btn.update_hover(mouse_pos)
            self.music_back_btn.update_hover(mouse_pos)

    # ============================================
    # UPDATE
    # ============================================

    def update(self):
        """Update game logic."""
        if self.state == config.STATE_PLAYING:
            self._update_playing()

    def _update_playing(self):
        """Physics, scoring, collision checks."""
        self.bird.update()

        passed = self.pipes.update(self.bird.get_rect())
        self.score += passed

        speed = config.DIFFICULTY_PROFILES[self.difficulty]["speed"]
        self.ground_offset = (self.ground_offset + speed) % 40

        bird_rect = self.bird.get_rect()
        ground_top = config.SCREEN_HEIGHT - config.GROUND_HEIGHT

        if bird_rect.bottom >= ground_top:
            self.die()
            return

        if bird_rect.top < 0:
            self.bird.y = 0
            self.bird.velocity = 0
            self.bird.rect.y = 0

        if self.pipes.collides_with(bird_rect):
            self.die()
            return

    # ============================================
    # DRAW
    # ============================================

    def draw(self):
        """Draw the current state."""
        ui.draw_gradient_bg(self.screen)

        if self.state == config.STATE_MENU:
            ui.draw_main_menu(self.screen, self.menu_buttons, self.difficulty)

        elif self.state == config.STATE_HOW_TO_PLAY:
            ui.draw_how_to_play(self.screen, self.how_to_play_back_btn)

        elif self.state == config.STATE_PLAYING:
            self._draw_world()
            ui.draw_hud(self.screen, self.score)
            ui.draw_pause_icon_button(
                self.screen, self.pause_icon_rect, self.pause_icon_hovered
            )

        elif self.state == config.STATE_PAUSED:
            self._draw_world()
            ui.draw_pause_screen(self.screen, self.pause_buttons)

        elif self.state == config.STATE_GAME_OVER:
            self._draw_world()
            ui.draw_game_over(self.screen, self.score, self.game_over_buttons)

        elif self.state == config.STATE_MUSIC:
            ui.draw_music_screen(
                self.screen,
                self.music,
                self.music_controls,
                self.music_add_btn,
                self.music_back_btn,
                self.playlist_items,
                self.music_progress_bar,
            )

        # Music bar (only during gameplay)
        if self.state == config.STATE_PLAYING:
            ui.draw_music_bar(self.screen, self.music)

    def _draw_world(self):
        """Draw pipes, ground, and bird (used during play & overlays)."""
        self.pipes.draw(self.screen)
        self._draw_ground()
        self.bird.draw(self.screen)

    def _draw_ground(self):
        """Draw the sand ground with a scrolling dashed line."""
        ground_top = config.SCREEN_HEIGHT - config.GROUND_HEIGHT

        ground_rect = pygame.Rect(
            0, ground_top, config.SCREEN_WIDTH, config.GROUND_HEIGHT
        )
        pygame.draw.rect(self.screen, config.GROUND_SAND, ground_rect)

        pygame.draw.line(
            self.screen,
            config.GROUND_LINE,
            (0, ground_top),
            (config.SCREEN_WIDTH, ground_top),
            3,
        )

        dash_w = 20
        dash_gap = 20
        y = ground_top + 12
        x = -int(self.ground_offset)
        while x < config.SCREEN_WIDTH:
            pygame.draw.rect(self.screen, config.GROUND_LINE, (x, y, dash_w, 4))
            x += dash_w + dash_gap

    # ============================================
    # MAIN LOOP
    # ============================================

    def run(self):
        """Run the main game loop until the user quits."""
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
