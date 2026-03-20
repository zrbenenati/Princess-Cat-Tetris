"""Tetromino construction and matrix rotation helpers."""

from game.types import Point, Tetromino, TetrominoType

SHAPES: dict[TetrominoType, list[list[int]]] = {
    "I": [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "T": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],
}


def create_tetromino(piece_type: TetrominoType) -> Tetromino:
    """Create a spawn-position tetromino.

    Args:
        piece_type: The tetromino piece identifier.

    Returns:
        A new tetromino in spawn orientation.
    """
    return Tetromino(
        piece_type=piece_type,
        rotation=0,
        matrix=[row[:] for row in SHAPES[piece_type]],
        position=Point(x=3, y=0),
    )


def rotate_matrix(matrix: list[list[int]], clockwise: bool) -> list[list[int]]:
    """Rotate a square matrix by 90 degrees.

    Args:
        matrix: Piece shape matrix.
        clockwise: Whether to rotate clockwise.

    Returns:
        Rotated matrix copy.
    """
    size: int = len(matrix)
    result: list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]
    for y in range(size):
        for x in range(size):
            if clockwise:
                result[x][size - y - 1] = matrix[y][x]
            else:
                result[size - x - 1][y] = matrix[y][x]
    return result
