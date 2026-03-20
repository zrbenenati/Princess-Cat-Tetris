"""Finite state machine for high-level game states."""

from game.types import PlayState


class GameStateMachine:
    """Tracks transitions between menu, playing, paused, and game over."""

    def __init__(self) -> None:
        self._state: PlayState = "name_entry"

    def get_state(self) -> PlayState:
        """Return the current play state.

        Returns:
            Current game state.
        """
        return self._state

    def start(self) -> None:
        """Enter playing state from non-playing states."""
        self._state = "playing"

    def toggle_pause(self) -> None:
        """Toggle between paused and playing states."""
        if self._state == "playing":
            self._state = "paused"
        elif self._state == "paused":
            self._state = "playing"

    def game_over(self) -> None:
        """Transition into game-over state."""
        self._state = "game_over"

    def name_entry(self) -> None:
        """Transition to player-name entry state."""
        self._state = "name_entry"

    def show_high_scores(self) -> None:
        """Transition to high scores state."""
        self._state = "high_scores"
