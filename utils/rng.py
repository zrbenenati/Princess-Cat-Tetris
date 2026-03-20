"""Random queue helpers using 7-bag generation."""

import random

from game.types import TetrominoType

PIECES: list[TetrominoType] = ["I", "O", "T", "S", "Z", "J", "L"]


def create_bag_queue(min_size: int) -> list[TetrominoType]:
    """Create a shuffled piece queue with at least min_size items.

    Args:
        min_size: Minimum queue length to produce.

    Returns:
        Queue generated using repeated shuffled 7-bags.
    """
    queue: list[TetrominoType] = []
    while len(queue) < min_size:
        bag: list[TetrominoType] = PIECES[:]
        random.shuffle(bag)
        queue.extend(bag)
    return queue
