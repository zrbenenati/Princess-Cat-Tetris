"""Piece queue and spawning operations."""

from entities.tetromino import create_tetromino
from game.types import Tetromino, TetrominoType
from utils.rng import create_bag_queue

NEXT_QUEUE_MIN: int = 5


def ensure_queue(queue: list[TetrominoType]) -> list[TetrominoType]:
    """Ensure queue has enough upcoming pieces.

    Args:
        queue: Existing queue.

    Returns:
        Queue with at least NEXT_QUEUE_MIN items.
    """
    if len(queue) >= NEXT_QUEUE_MIN:
        return queue
    return queue + create_bag_queue(NEXT_QUEUE_MIN - len(queue))


def spawn_piece(queue: list[TetrominoType]) -> tuple[Tetromino, list[TetrominoType]]:
    """Spawn next piece and replenish queue.

    Args:
        queue: Existing next queue.

    Returns:
        Tuple of (spawned_piece, updated_queue).
    """
    filled: list[TetrominoType] = ensure_queue(queue)
    next_type: TetrominoType = filled[0]
    rest: list[TetrominoType] = filled[1:]
    return (create_tetromino(next_type), ensure_queue(rest))
