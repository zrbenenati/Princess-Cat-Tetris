"""Core Tetris game orchestrator with isolated systems."""

from dataclasses import replace

from entities.tetromino import create_tetromino
from game.high_score_store import read_high_score, write_high_score
from game.state_machine import GameStateMachine
from game.types import GameContext, GameMetrics, InputAction, PieceQueue, Tetromino
from systems.collision_system import clone_piece, create_empty_board, has_collision, lock_piece
from systems.hold_system import apply_hold
from systems.line_clear_system import clear_lines
from systems.movement_system import compute_ghost_piece, hard_drop, try_move
from systems.rotation_system import try_rotate
from systems.scoring_system import compute_level, fall_interval_seconds, score_for_clear
from systems.spawn_system import ensure_queue, spawn_piece
from utils.constants import LOCK_DELAY_SECONDS


class TetrisGame:
    """Coordinates input actions, updates, and state transitions."""

    def __init__(self) -> None:
        self.state_machine: GameStateMachine = GameStateMachine()
        high_score: int = read_high_score()
        seeded_queue = ensure_queue([])
        active_piece, queue = spawn_piece(seeded_queue)
        self.context: GameContext = GameContext(
            board=create_empty_board(),
            active_piece=active_piece,
            ghost_piece=clone_piece(active_piece),
            queue=PieceQueue(next_pieces=queue, hold_piece=None, can_hold=True),
            metrics=GameMetrics(score=0, level=1, lines_cleared=0, high_score=high_score),
            play_state=self.state_machine.get_state(),
        )
        self.drop_accumulator: float = 0.0
        self.lock_accumulator: float = 0.0
        self._refresh_ghost()

    def frame_update(self, delta_seconds: float, actions: list[InputAction]) -> None:
        """Process one game frame.

        Args:
            delta_seconds: Frame delta time in seconds.
            actions: Input actions queued for this frame.
        """
        self._handle_actions(actions)
        self._update(delta_seconds)

    def _handle_actions(self, actions: list[InputAction]) -> None:
        for action in actions:
            if action == "start_game" and self.context.play_state in ("menu", "game_over"):
                self._reset_game()
                self.state_machine.start()
            elif action == "toggle_pause":
                self.state_machine.toggle_pause()
            self.context.play_state = self.state_machine.get_state()
            if self.context.play_state != "playing":
                continue
            self._apply_action(action)

    def _apply_action(self, action: InputAction) -> None:
        if action == "move_left":
            self.context.active_piece = try_move(self.context.board, self.context.active_piece, -1, 0)
        elif action == "move_right":
            self.context.active_piece = try_move(self.context.board, self.context.active_piece, 1, 0)
        elif action == "soft_drop":
            moved = try_move(self.context.board, self.context.active_piece, 0, 1)
            if moved is not self.context.active_piece:
                self.context.active_piece = moved
                self.context.metrics.score += 1
        elif action == "hard_drop":
            self.context.active_piece = hard_drop(self.context.board, self.context.active_piece)
            self._lock_active_piece()
        elif action == "rotate_cw":
            self.context.active_piece = try_rotate(self.context.board, self.context.active_piece, True)
        elif action == "rotate_ccw":
            self.context.active_piece = try_rotate(self.context.board, self.context.active_piece, False)
        elif action == "hold":
            active_piece, hold_piece, queue, can_hold = apply_hold(
                self.context.active_piece,
                self.context.queue.hold_piece,
                self.context.queue.next_pieces,
                self.context.queue.can_hold,
            )
            self.context.active_piece = active_piece
            self.context.queue.hold_piece = hold_piece
            self.context.queue.next_pieces = queue
            self.context.queue.can_hold = can_hold
        self._refresh_ghost()

    def _update(self, delta_seconds: float) -> None:
        self.context.play_state = self.state_machine.get_state()
        if self.context.play_state != "playing":
            return
        self.drop_accumulator += delta_seconds
        interval: float = fall_interval_seconds(self.context.metrics.level)
        while self.drop_accumulator >= interval:
            self.drop_accumulator -= interval
            moved = try_move(self.context.board, self.context.active_piece, 0, 1)
            if moved is self.context.active_piece:
                self.lock_accumulator += interval
                if self.lock_accumulator >= LOCK_DELAY_SECONDS:
                    self._lock_active_piece()
                    break
            else:
                self.context.active_piece = moved
                self.lock_accumulator = 0.0
        self._refresh_ghost()

    def _lock_active_piece(self) -> None:
        self.context.board = lock_piece(self.context.board, self.context.active_piece)
        self.context.board, cleared = clear_lines(self.context.board)
        self.context.metrics.lines_cleared += cleared
        self.context.metrics.level = compute_level(self.context.metrics.lines_cleared)
        self.context.metrics.score += score_for_clear(cleared, self.context.metrics.level)
        new_piece, queue = spawn_piece(self.context.queue.next_pieces)
        self.context.active_piece = new_piece
        self.context.queue.next_pieces = queue
        self.context.queue.can_hold = True
        if has_collision(self.context.board, self.context.active_piece):
            self.state_machine.game_over()
            self.context.play_state = self.state_machine.get_state()
            if self.context.metrics.score > self.context.metrics.high_score:
                self.context.metrics.high_score = self.context.metrics.score
                write_high_score(self.context.metrics.high_score)
        self.lock_accumulator = 0.0
        self._refresh_ghost()

    def _refresh_ghost(self) -> None:
        ghost: Tetromino = compute_ghost_piece(self.context.board, self.context.active_piece)
        self.context.ghost_piece = clone_piece(ghost)
        self.context.play_state = self.state_machine.get_state()

    def _reset_game(self) -> None:
        seeded_queue = ensure_queue([])
        active_piece, queue = spawn_piece(seeded_queue)
        self.context.board = create_empty_board()
        self.context.active_piece = create_tetromino(active_piece.piece_type)
        self.context.queue = PieceQueue(next_pieces=queue, hold_piece=None, can_hold=True)
        self.context.metrics = replace(
            self.context.metrics,
            score=0,
            level=1,
            lines_cleared=0,
        )
        self.drop_accumulator = 0.0
        self.lock_accumulator = 0.0
        self._refresh_ghost()
