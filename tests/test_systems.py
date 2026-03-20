"""Unit tests for core, testable game systems."""

from entities.tetromino import create_tetromino
from systems.collision_system import create_empty_board, has_collision
from systems.line_clear_system import clear_lines
from systems.scoring_system import compute_level, fall_interval_seconds, score_for_clear


def test_clear_lines_removes_filled_row() -> None:
    """Clear lines should remove fully occupied rows."""
    board = create_empty_board()
    board[-1] = ["I" for _ in board[-1]]
    new_board, cleared = clear_lines(board)
    assert cleared == 1
    assert all(cell is None for cell in new_board[0])


def test_collision_detects_left_wall() -> None:
    """Collision should trigger when piece exits board bounds."""
    board = create_empty_board()
    piece = create_tetromino("O")
    piece.position.x = -1
    assert has_collision(board, piece) is True


def test_score_level_and_speed_scale() -> None:
    """Score and gravity should scale with level progression."""
    assert score_for_clear(4, 2) == 1600
    assert compute_level(0) == 1
    assert compute_level(20) == 3
    assert fall_interval_seconds(10) < fall_interval_seconds(1)
