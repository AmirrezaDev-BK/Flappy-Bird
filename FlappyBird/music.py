"""
music.py
========
MusicManager (singleton).
Handles playlist, playback, stop (with real position memory),
seek, next/prev, per-track loop, progress, and adding tracks via file dialog.
"""

import os
import pygame
import tkinter as tk
from tkinter import filedialog
import config


class MusicManager:
    """Singleton music player for the whole game."""

    _instance = None

    def __new__(cls):
        """Ensure only one MusicManager instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize playlist and state flags."""
        if self._initialized:
            return
        self._initialized = True

        self.playlist = []
        self.current_index = -1
        self.is_playing = False

        # Position memory
        self._saved_position = 0.0  # position to resume from (seconds)
        self._start_offset = 0.0  # where current playback started

        try:
            pygame.mixer.init()
        except pygame.error:
            pass

    # ============================================
    # PLAYLIST MANAGEMENT
    # ============================================

    def add_tracks(self):
        """Open file dialog and add selected music files to playlist."""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        paths = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.ogg *.wav"),
                ("All Files", "*.*"),
            ],
        )
        root.destroy()

        added = 0
        for path in paths:
            self._add_single(path)
            added += 1

        if self.current_index == -1 and self.playlist:
            self.current_index = 0

        if added > 0 and not self.is_playing:
            self.play()

        return added

    def _add_single(self, path):
        """Add a single track dict to the playlist."""
        name = os.path.basename(path)
        duration = self._get_duration(path)
        self.playlist.append(
            {
                "path": path,
                "name": name,
                "loop": True,
                "duration": duration,
            }
        )

    def _get_duration(self, path):
        """Try to get duration of an audio file in seconds."""
        try:
            sound = pygame.mixer.Sound(path)
            return sound.get_length()
        except pygame.error:
            return 0.0

    def clear_playlist(self):
        """Stop playback and clear the playlist."""
        self.stop()
        self.playlist = []
        self.current_index = -1
        self._saved_position = 0.0
        self._start_offset = 0.0

    # ============================================
    # PLAYBACK CONTROLS
    # ============================================

    def play(self):
        """Start (or resume) playback from saved position if available."""
        if not self.playlist:
            return
        if self.current_index == -1:
            self.current_index = 0

        track = self.playlist[self.current_index]

        try:
            pygame.mixer.music.load(track["path"])
            loops = -1 if track["loop"] else 0

            if self._saved_position > 0:
                pygame.mixer.music.play(loops=loops, start=self._saved_position)
                self._start_offset = self._saved_position
                self._saved_position = 0.0
            else:
                pygame.mixer.music.play(loops=loops)
                self._start_offset = 0.0

            self.is_playing = True
        except pygame.error:
            self.next()

    def stop(self):
        """Stop playback but remember position to resume later."""
        self._saved_position = self.get_position()
        pygame.mixer.music.stop()
        self.is_playing = False

    def toggle_play_stop(self):
        """Toggle between play and stop for the current track."""
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def next(self):
        """Skip to next track and play from the beginning."""
        if not self.playlist:
            return
        self._saved_position = 0.0
        self._start_offset = 0.0
        self.current_index = (self.current_index + 1) % len(self.playlist)
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play()

    def previous(self):
        """Go back to previous track and play from the beginning."""
        if not self.playlist:
            return
        self._saved_position = 0.0
        self._start_offset = 0.0
        self.current_index = (self.current_index - 1) % len(self.playlist)
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play()

    def toggle_loop(self):
        """Toggle loop flag; if playing, restart from current position."""
        if not self.playlist:
            return
        track = self.playlist[self.current_index]
        track["loop"] = not track["loop"]

        if self.is_playing:
            self._saved_position = self.get_position()
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play()

    def select_track(self, index):
        """Select a track by index; play from the beginning."""
        if 0 <= index < len(self.playlist):
            self._saved_position = 0.0
            self._start_offset = 0.0
            self.current_index = index
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play()

    def seek(self, seconds):
        """Seek to the given position (in seconds) in the current track."""
        if not self.playlist:
            return
        track = self.get_current_track()
        if track is None:
            return

        # Clamp to track duration
        duration = track.get("duration", 0.0)
        if duration > 0:
            seconds = max(0.0, min(seconds, duration - 0.1))
        else:
            seconds = max(0.0, seconds)

        self._saved_position = seconds
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play()

    # ============================================
    # INFO GETTERS
    # ============================================

    def get_current_track(self):
        if not self.playlist or self.current_index == -1:
            return None
        return self.playlist[self.current_index]

    def has_playlist(self):
        return len(self.playlist) > 0

    def get_position(self):
        """Return real position in seconds, accounting for resume offset."""
        if not self.is_playing:
            return 0.0
        try:
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms < 0:
                return 0.0
            return self._start_offset + pos_ms / 1000.0
        except pygame.error:
            return 0.0

    def get_progress(self):
        track = self.get_current_track()
        if track is None:
            return 0.0
        duration = track.get("duration", 0.0)
        if duration <= 0:
            return 0.0
        pos = self.get_position()
        if pos >= duration:
            return 1.0
        return pos / duration

    def get_time_string(self):
        track = self.get_current_track()
        if track is None:
            return "0:00 / 0:00"

        duration = track.get("duration", 0.0)
        pos = self.get_position()

        def fmt(s):
            s = int(s)
            return f"{s // 60}:{s % 60:02d}"

        return f"{fmt(pos)} / {fmt(duration)}"

    def get_status_text(self):
        track = self.get_current_track()
        if track is None:
            return config.MUSIC_BAR_NO_TRACK

        symbol = ">" if self.is_playing else "[]"
        loop_tag = "[Loop: ON]" if track["loop"] else "[Loop: OFF]"
        return f"{symbol}  {track['name']}  {loop_tag}"
