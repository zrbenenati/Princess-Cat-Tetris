"""Piece rotation with simple wall-kick offsets."""

from entities.tetromino import rotate_matrix
from game.types import Tetromino
from systems.collision_system import clone_piece, has_collision

KICK_OFFSETS: list[tuple[int, int]] = [
    (0, 0),
    (-1, 0),
    (1, 0),
    (-2, 0),
    (2, 0),
    (0, -1),
]


def try_rotate(
    board: list[list[str | None]],
    piece: Tetromino,
    clockwise: bool,
) -> Tetromino:
    """Rotate piece and resolve collisions with kick offsets.

    Args:
        board: Current board.
        piece: Active piece.
        clockwise: Rotation direction.

    Returns:
        Rotated piece if valid, else original.
    """
    rotated: Tetromino = clone_piece(piece)
    rotated.matrix = rotate_matrix(piece.matrix, clockwise)
    rotated.rotation = (piece.rotation + (1 if clockwise else 3)) % 4
    for offset_x, offset_y in KICK_OFFSETS:
        candidate: Tetromino = clone_piece(rotated)
        candidate.position.x += offset_x
        candidate.position.y += offset_y
        if not has_collision(board, candidate):
            return candidate
    return piece
