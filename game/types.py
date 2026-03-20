"""Typed models used by game logic."""

from dataclasses import dataclass
from typing import Literal

TetrominoType = Literal["I", "O", "T", "S", "Z", "J", "L"]
PlayState = Literal["name_entry", "playing", "paused", "game_over", "high_scores"]
InputAction = Literal[
    "move_left",
    "move_right",
    "soft_drop",
    "hard_drop",
    "rotate_cw",
    "rotate_ccw",
    "hold",
    "toggle_pause",
    "start_game",
    "backspace",
]


@dataclass
class Point:
    """A 2D integer coordinate."""

    x: int
    y: int


@dataclass
class Tetromino:
    """Active tetromino data used by systems."""

    piece_type: TetrominoType
    rotation: int
    matrix: list[list[int]]
    position: Point


@dataclass
class GameMetrics:
    """Scoring and progression metrics."""

    score: int
    level: int
    lines_cleared: int
    high_score: int


@dataclass
class ScoreEntry:
    """One high score row with player name."""

    player_name: str
    score: int


@dataclass
class PieceQueue:
    """Next and hold piece state."""

    next_pieces: list[TetrominoType]
    hold_piece: TetrominoType | None
    can_hold: bool


@dataclass
class GameContext:
    """Top-level game state shared across loop and renderer."""

    board: list[list[str | None]]
    active_piece: Tetromino
    ghost_piece: Tetromino
    queue: PieceQueue
    metrics: GameMetrics
    play_state: PlayState
    player_name: str
    high_scores: list[ScoreEntry]
