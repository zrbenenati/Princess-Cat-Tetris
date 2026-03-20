"""Simple JSON file persistence for named high scores."""

import json
from pathlib import Path

from game.types import ScoreEntry
from utils.constants import HIGH_SCORE_FILE


def read_high_scores() -> list[ScoreEntry]:
    """Read named high scores from disk.

    Returns:
        Sorted list of score entries (high to low).
    """
    path: Path = Path(HIGH_SCORE_FILE)
    if not path.exists():
        return []
    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw_data, dict) and "high_score" in raw_data:
            # Backward compatibility with previous format.
            legacy_score: int = int(raw_data.get("high_score", 0))
            if legacy_score <= 0:
                return []
            return [ScoreEntry(player_name="Player", score=legacy_score)]

        if not isinstance(raw_data, list):
            return []
        scores: list[ScoreEntry] = []
        for row in raw_data:
            if not isinstance(row, dict):
                continue
            player_name: str = str(row.get("player_name", "Player")).strip() or "Player"
            score: int = int(row.get("score", 0))
            if score < 0:
                continue
            scores.append(ScoreEntry(player_name=player_name, score=score))
        return sorted(scores, key=lambda item: item.score, reverse=True)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return []


def write_high_scores(scores: list[ScoreEntry]) -> None:
    """Write named high scores to disk.

    Args:
        scores: Score rows to persist.
    """
    for row in scores:
        if row.score < 0:
            raise ValueError("score must be non-negative")
    path: Path = Path(HIGH_SCORE_FILE)
    payload: list[dict[str, str | int]] = [
        {"player_name": row.player_name, "score": row.score}
        for row in scores
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")


def submit_score(player_name: str, score: int, limit: int = 10) -> list[ScoreEntry]:
    """Insert a player's score and return trimmed leaderboard.

    Args:
        player_name: Name to display on leaderboard.
        score: Score value to submit.
        limit: Max rows to keep.

    Returns:
        Updated sorted leaderboard.
    """
    if score < 0:
        raise ValueError("score must be non-negative")
    normalized_name: str = player_name.strip() or "Player"
    scores: list[ScoreEntry] = read_high_scores()
    scores.append(ScoreEntry(player_name=normalized_name, score=score))
    updated: list[ScoreEntry] = sorted(scores, key=lambda row: row.score, reverse=True)[:limit]
    write_high_scores(updated)
    return updated
