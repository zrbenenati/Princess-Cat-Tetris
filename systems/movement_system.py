"""Horizontal and vertical movement behavior."""

from game.types import Tetromino
from systems.collision_system import clone_piece, has_collision


def try_move(
    board: list[list[str | None]],
    piece: Tetromino,
    delta_x: int,
    delta_y: int,
) -> Tetromino:
    """Attempt to move a piece and reject collisions.

    Args:
        board: Current board.
        piece: Active piece.
        delta_x: Horizontal delta.
        delta_y: Vertical delta.

    Returns:
        Moved piece or original if blocked.
    """
    next_piece: Tetromino = clone_piece(piece)
    next_piece.position.x += delta_x
    next_piece.position.y += delta_y
    if has_collision(board, next_piece):
        return piece
    return next_piece


def hard_drop(board: list[list[str | None]], piece: Tetromino) -> Tetromino:
    """Drop piece until it reaches the floor or stacked blocks.

    Args:
        board: Current board.
        piece: Active piece.

    Returns:
        Piece positioned at final drop location.
    """
    dropped: Tetromino = piece
    while True:
        moved: Tetromino = try_move(board, dropped, 0, 1)
        if moved is dropped:
            return dropped
        dropped = moved


def compute_ghost_piece(board: list[list[str | None]], piece: Tetromino) -> Tetromino:
    """Compute where a hard drop would land.

    Args:
        board: Current board.
        piece: Active piece.

    Returns:
        Ghost piece position.
    """
    return hard_drop(board, piece)
