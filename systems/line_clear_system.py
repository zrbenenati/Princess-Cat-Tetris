"""Line clear detection and board compaction."""


def clear_lines(board: list[list[str | None]]) -> tuple[list[list[str | None]], int]:
    """Remove fully occupied rows and insert empty rows at top.

    Args:
        board: Current board.

    Returns:
        Tuple of (new_board, cleared_line_count).
    """
    remaining: list[list[str | None]] = [row for row in board if any(cell is None for cell in row)]
    cleared: int = len(board) - len(remaining)
    width: int = len(board[0])
    new_rows: list[list[str | None]] = [[None for _ in range(width)] for _ in range(cleared)]
    return (new_rows + remaining, cleared)
