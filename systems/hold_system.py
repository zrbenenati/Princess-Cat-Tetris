"""Hold piece swap behavior."""

from entities.tetromino import create_tetromino
from game.types import Tetromino, TetrominoType
from systems.spawn_system import spawn_piece


def apply_hold(
    active_piece: Tetromino,
    hold_piece: TetrominoType | None,
    queue: list[TetrominoType],
    can_hold: bool,
) -> tuple[Tetromino, TetrominoType | None, list[TetrominoType], bool]:
    """Swap active piece with hold slot.

    Args:
        active_piece: Current active piece.
        hold_piece: Current hold slot piece.
        queue: Upcoming queue.
        can_hold: Whether hold is available this turn.

    Returns:
        Tuple of (new_active_piece, new_hold_piece, new_queue, new_can_hold).
    """
    if not can_hold:
        return (active_piece, hold_piece, queue, can_hold)
    if hold_piece is None:
        spawned_piece, new_queue = spawn_piece(queue)
        return (spawned_piece, active_piece.piece_type, new_queue, False)
    return (create_tetromino(hold_piece), active_piece.piece_type, queue, False)
