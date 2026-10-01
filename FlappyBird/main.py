"""
main.py
=======
Entry point for Flappy Bird (modern version).
Starts the game in a resizable window (SCALED).
User can press F to toggle fullscreen, or use window controls.
"""

import config
import pygame
from game import Game


def main():
    """Initialize pygame and start the game."""
    pygame.init()

    # Resizable + SCALED: logical 480x720 is scaled to fit window.
    # Window controls (minimize, maximize, close) are available.
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SCALED | pygame.RESIZABLE
    )
    pygame.display.set_caption(config.TITLE)

    game = Game(screen)
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
