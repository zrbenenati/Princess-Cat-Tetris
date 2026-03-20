"""Shared constants for board dimensions, timing, and scoring."""

BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 20
TILE_SIZE: int = 28
PANEL_WIDTH: int = 240

WINDOW_WIDTH: int = BOARD_WIDTH * TILE_SIZE + PANEL_WIDTH
WINDOW_HEIGHT: int = BOARD_HEIGHT * TILE_SIZE

FPS: int = 60
LOCK_DELAY_SECONDS: float = 0.45

LINES_PER_LEVEL: int = 10
BASE_FALL_SECONDS: float = 0.8
MIN_FALL_SECONDS: float = 0.08

SCORE_TABLE: dict[int, int] = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
}

HIGH_SCORE_FILE: str = "high_score.json"
