"""Scoring and level progression calculations."""

import math

from utils.constants import BASE_FALL_SECONDS, LINES_PER_LEVEL, MIN_FALL_SECONDS, SCORE_TABLE


def score_for_clear(lines: int, level: int) -> int:
    """Compute score gain from line clears.

    Args:
        lines: Number of lines cleared in one lock.
        level: Current level.

    Returns:
        Score delta.
    """
    if lines <= 0:
        return 0
    base: int = SCORE_TABLE.get(lines, 0)
    return base * level


def compute_level(lines_cleared: int) -> int:
    """Compute level from total cleared lines.

    Args:
        lines_cleared: Running line total.

    Returns:
        Current level (starting at 1).
    """
    return (lines_cleared // LINES_PER_LEVEL) + 1


def fall_interval_seconds(level: int) -> float:
    """Compute gravity interval based on level.

    Args:
        level: Current level.

    Returns:
        Seconds between automatic drops.
    """
    scaled: float = BASE_FALL_SECONDS * math.pow(0.86, level - 1)
    return max(MIN_FALL_SECONDS, scaled)
