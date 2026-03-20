"""Board collision and lock helpers."""

from game.types import Tetromino
from utils.constants import BOARD_HEIGHT, BOARD_WIDTH


def create_empty_board() -> list[list[str | None]]:
    """Create an empty board matrix.

    Returns:
        A 2D board containing None values.
    """
    return [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def clone_piece(piece: Tetromino) -> Tetromino:
    """Create a deep clone of a tetromino.

    Args:
        piece: Source tetromino.

    Returns:
        Cloned tetromino.
    """
    return Tetromino(
        piece_type=piece.piece_type,
        rotation=piece.rotation,
        matrix=[row[:] for row in piece.matrix],
        position=type(piece.position)(x=piece.position.x, y=piece.position.y),
    )


def has_collision(board: list[list[str | None]], piece: Tetromino) -> bool:
    """Check if piece collides with board bounds or occupied cells.

    Args:
        board: Current board.
        piece: Candidate tetromino.

    Returns:
        True when collision is present.
    """
    for y, row in enumerate(piece.matrix):
        for x, cell in enumerate(row):
            if cell == 0:
                continue
            board_x: int = piece.position.x + x
            board_y: int = piece.position.y + y
            if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:
                return True
            if board_y >= 0 and board[board_y][board_x] is not None:
                return True
    return False


def lock_piece(board: list[list[str | None]], piece: Tetromino) -> list[list[str | None]]:
    """Write active piece blocks into board cells.

    Args:
        board: Current board.
        piece: Piece to merge into the board.

    Returns:
        New board with piece locked.
    """
    next_board: list[list[str | None]] = [row[:] for row in board]
    for y, row in enumerate(piece.matrix):
        for x, cell in enumerate(row):
            if cell == 0:
                continue
            board_x: int = piece.position.x + x
            board_y: int = piece.position.y + y
            if 0 <= board_y < BOARD_HEIGHT:
                next_board[board_y][board_x] = piece.piece_type
    return next_board
