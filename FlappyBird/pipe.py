"""
pipe.py
=======
Pipe class and PipeManager.
Handles spawning, moving, drawing, and collision for pipe pairs.
Difficulty affects gap size, pipe speed, and spawn distance.
"""

import random
import pygame
import config


class Pipe:
    """A single pair of pipes (top + bottom) with a gap between them."""

    def __init__(self, x, gap, speed):
        """Create a pipe pair at given X with difficulty parameters."""
        self.x = x
        self.gap = gap
        self.speed = speed

        # Random vertical position of the gap
        self.gap_y = random.randint(config.PIPE_MIN_TOP, config.PIPE_MAX_TOP)

        # Top pipe rect (from y=0 down to gap_y)
        self.top_rect = pygame.Rect(self.x, 0, config.PIPE_WIDTH, self.gap_y)

        # Bottom pipe rect (from gap_y + gap down to ground)
        bottom_y = self.gap_y + self.gap
        bottom_height = config.SCREEN_HEIGHT - config.GROUND_HEIGHT - bottom_y
        self.bottom_rect = pygame.Rect(
            self.x, bottom_y, config.PIPE_WIDTH, bottom_height
        )

        # Track whether bird has passed this pipe (for scoring)
        self.passed = False

    def update(self):
        """Move pipe to the left each frame."""
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, surface):
        """Draw both pipes with caps."""
        self._draw_pipe(surface, self.top_rect, is_top=True)
        self._draw_pipe(surface, self.bottom_rect, is_top=False)

    def _draw_pipe(self, surface, rect, is_top):
        """Draw a single pipe: body, shading, outline, and cap."""
        # Pipe body
        pygame.draw.rect(surface, config.PIPE_GREEN, rect)

        # Left highlight strip
        highlight = pygame.Rect(rect.x + 4, rect.y, 10, rect.height)
        pygame.draw.rect(surface, config.PIPE_GREEN_DARK, highlight)

        # Outline
        pygame.draw.rect(surface, config.PIPE_OUTLINE, rect, 3)

        # Cap (lip) at the gap end
        cap_h = config.PIPE_CAP_HEIGHT
        cap_x = rect.x - 5
        cap_w = rect.width + 10

        if is_top:
            cap_y = rect.bottom - cap_h
        else:
            cap_y = rect.top

        cap_rect = pygame.Rect(cap_x, cap_y, cap_w, cap_h)
        pygame.draw.rect(surface, config.PIPE_GREEN, cap_rect)
        pygame.draw.rect(surface, config.PIPE_OUTLINE, cap_rect, 3)

    def is_offscreen(self):
        """Check if pipe has moved completely off the left side."""
        return self.x + config.PIPE_WIDTH < 0

    def collides_with(self, rect):
        """Check collision against a rectangle (usually the bird)."""
        return self.top_rect.colliderect(rect) or self.bottom_rect.colliderect(rect)

    def check_passed(self, bird_rect):
        """Return True if bird just passed this pipe (for +1 score)."""
        if not self.passed and bird_rect.left > self.x + config.PIPE_WIDTH:
            self.passed = True
            return True
        return False


class PipeManager:
    """Manages spawning, updating, drawing, and collision of all pipes."""

    def __init__(self):
        """Initialize empty pipe list and spawn counter."""
        self.pipes = []
        self.spawn_timer = 0
        self.spawn_distance = config.PIPE_SPAWN_DISTANCE
        self.gap = config.PIPE_GAP
        self.speed = config.PIPE_SPEED

    def set_difficulty(self, gap, speed, spawn_distance):
        """Apply difficulty settings (called on game start)."""
        self.gap = gap
        self.speed = speed
        self.spawn_distance = spawn_distance

    def reset(self):
        """Clear all pipes and reset spawn timer."""
        self.pipes = []
        self.spawn_timer = 0

    def update(self, bird_rect):
        """
        Update all pipes, spawn new ones, remove offscreen ones.
        Returns number of pipes the bird passed this frame.
        """
        # Update existing pipes
        for pipe in self.pipes:
            pipe.update()

        # Remove offscreen pipes
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]

        # Spawn new pipes based on distance travelled
        self.spawn_timer += self.speed
        if self.spawn_timer >= self.spawn_distance:
            self.spawn_timer = 0
            spawn_x = config.SCREEN_WIDTH + 20
            self.pipes.append(Pipe(spawn_x, self.gap, self.speed))

        # Count how many pipes the bird just passed
        passed_count = 0
        for pipe in self.pipes:
            if pipe.check_passed(bird_rect):
                passed_count += 1

        return passed_count

    def draw(self, surface):
        """Draw all pipes."""
        for pipe in self.pipes:
            pipe.draw(surface)

    def collides_with(self, rect):
        """Return True if any pipe collides with the given rectangle."""
        for pipe in self.pipes:
            if pipe.collides_with(rect):
                return True
        return False
