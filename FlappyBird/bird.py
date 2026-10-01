"""
bird.py
=======
Bird (player) class.
Handles gravity, flapping, movement, rotation, and drawing.
Difficulty (gravity, flap strength) is applied from outside.
"""

import config
import pygame


class Bird:
    """The player-controlled bird."""

    def __init__(self):
        """Initialize bird position, velocity, and sprite."""
        # Load and scale sprite
        self.image = pygame.image.load(config.BIRD_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (config.BIRD_WIDTH, config.BIRD_HEIGHT)
        )

        # Position (float for smooth movement)
        self.x = config.BIRD_START_X
        self.y = float(config.BIRD_START_Y)

        # Velocity (vertical only)
        self.velocity = 0.0

        # Rotation angle (visual tilt)
        self.angle = 0.0

        # Hitbox rectangle (used for collision)
        self.rect = pygame.Rect(self.x, self.y, config.BIRD_WIDTH, config.BIRD_HEIGHT)

        # Difficulty-driven physics values
        self.gravity = config.BIRD_GRAVITY
        self.flap_strength = config.BIRD_FLAP_STRENGTH

    def set_difficulty(self, gravity, flap_strength):
        """Apply gravity and flap strength for current difficulty."""
        self.gravity = gravity
        self.flap_strength = flap_strength

    def flap(self):
        """Apply upward velocity when player presses SPACE."""
        self.velocity = self.flap_strength

    def update(self):
        """Apply gravity and update position each frame."""
        # Apply gravity
        self.velocity += self.gravity

        # Clamp velocity to max fall / rise speed
        if self.velocity > config.BIRD_MAX_FALL_SPEED:
            self.velocity = config.BIRD_MAX_FALL_SPEED
        if self.velocity < config.BIRD_MAX_RISE_SPEED:
            self.velocity = config.BIRD_MAX_RISE_SPEED

        # Update Y position
        self.y += self.velocity

        # Update rotation based on velocity (tilt up when rising, down when falling)
        self.angle = -self.velocity * config.BIRD_ROTATION_FACTOR
        self.angle = max(-30, min(90, self.angle))

        # Update rect for collision
        self.rect.x = self.x
        self.rect.y = int(self.y)

    def draw(self, surface):
        """Draw the bird with rotation on the given surface."""
        rotated = pygame.transform.rotate(self.image, -self.angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rotated_rect)

    def reset(self):
        """Reset bird to starting state (used on restart)."""
        self.x = config.BIRD_START_X
        self.y = float(config.BIRD_START_Y)
        self.velocity = 0.0
        self.angle = 0.0
        self.rect.x = self.x
        self.rect.y = int(self.y)

    def get_rect(self):
        """Return the bird's collision rectangle."""
        return self.rect
