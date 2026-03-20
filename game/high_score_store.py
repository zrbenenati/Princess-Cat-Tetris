"""Simple JSON file persistence for high score."""

import json
from pathlib import Path

from utils.constants import HIGH_SCORE_FILE


def read_high_score() -> int:
    """Read high score from disk.

    Returns:
        Stored high score or zero if file is missing/invalid.
    """
    path: Path = Path(HIGH_SCORE_FILE)
    if not path.exists():
        return 0
    try:
        data: dict[str, int] = json.loads(path.read_text(encoding="utf-8"))
        score: int = int(data.get("high_score", 0))
        return max(0, score)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def write_high_score(score: int) -> None:
    """Write high score to disk.

    Args:
        score: Score to persist.
    """
    if score < 0:
        raise ValueError("score must be non-negative")
    path: Path = Path(HIGH_SCORE_FILE)
    payload: dict[str, int] = {"high_score": score}
    path.write_text(json.dumps(payload), encoding="utf-8")
