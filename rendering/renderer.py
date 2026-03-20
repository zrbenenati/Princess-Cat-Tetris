"""Dedicated rendering module for board and UI drawing."""

import pygame

from entities.tetromino import SHAPES
from game.types import GameContext, Tetromino, TetrominoType
from utils.constants import BOARD_HEIGHT, BOARD_WIDTH, TILE_SIZE

PREVIEW_CELL: int = 7
PREVIEW_SLOT_W: int = 56
PREVIEW_SLOT_H: int = 40

COLORS: dict[str, tuple[int, int, int]] = {
    "I": (170, 217, 255),
    "O": (255, 241, 166),
    "T": (223, 176, 255),
    "S": (189, 245, 212),
    "Z": (255, 186, 210),
    "J": (180, 198, 255),
    "L": (255, 208, 170),
}

CAT_FUR_COLORS: dict[str, tuple[int, int, int]] = {
    "I": (224, 236, 255),
    "O": (255, 245, 204),
    "T": (238, 216, 255),
    "S": (224, 255, 236),
    "Z": (255, 220, 232),
    "J": (220, 232, 255),
    "L": (255, 228, 208),
}

CAT_OUTLINE_COLORS: dict[str, tuple[int, int, int]] = {
    "I": (120, 142, 186),
    "O": (173, 153, 92),
    "T": (140, 106, 175),
    "S": (104, 163, 130),
    "Z": (179, 110, 133),
    "J": (102, 126, 176),
    "L": (176, 122, 96),
}


class Renderer:
    """Draws game board, active pieces, and side panel."""

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 20)
        self.title_font: pygame.font.Font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font: pygame.font.Font = pygame.font.SysFont("Arial", 16)
        self.decor_font: pygame.font.Font = pygame.font.SysFont("Arial", 18, bold=True)

    def render(self, context: GameContext) -> None:
        """Render one frame from game context.

        Args:
            context: Full game state snapshot.
        """
        self.surface.fill((255, 233, 245))
        self._draw_background_decor()
        self._draw_sparkles()
        self._draw_board(context)
        self._draw_piece(context.ghost_piece, (219, 189, 208))
        self._draw_piece(context.active_piece, None)
        self._draw_panel(context)
        self._draw_overlay(context)
        pygame.display.flip()

    def _draw_background_decor(self) -> None:
        """Draw princess-themed decorative accents."""
        pygame.draw.circle(self.surface, (255, 206, 233), (20, 20), 7)
        pygame.draw.circle(self.surface, (255, 206, 233), (60, 48), 6)
        pygame.draw.circle(self.surface, (255, 206, 233), (102, 24), 5)
        pygame.draw.circle(self.surface, (255, 206, 233), (366, 20), 7)
        pygame.draw.circle(self.surface, (255, 206, 233), (436, 48), 6)
        self.surface.blit(self.decor_font.render("Princess Cat Tetris", True, (191, 103, 148)), (10, 2))

    def _draw_sparkles(self) -> None:
        """Draw animated sparkles for a magical theme."""
        ticks: int = pygame.time.get_ticks()
        sparkle_points: list[tuple[int, int, int]] = [
            (18, 84, 0),
            (98, 126, 240),
            (228, 72, 480),
            (142, 232, 720),
            (248, 312, 960),
            (74, 438, 1200),
            (312, 458, 1440),
        ]
        for x, y, phase in sparkle_points:
            pulse: int = (ticks + phase) % 1200
            size: int = 2 + (pulse // 300)
            color: tuple[int, int, int] = (255, 255 - (pulse // 8), 245)
            pygame.draw.line(self.surface, color, (x - size, y), (x + size, y), width=2)
            pygame.draw.line(self.surface, color, (x, y - size), (x, y + size), width=2)

    def _draw_board(self, context: GameContext) -> None:
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                px: int = x * TILE_SIZE
                py: int = y * TILE_SIZE
                pygame.draw.rect(self.surface, (240, 191, 219), (px, py, TILE_SIZE, TILE_SIZE), width=1)
                cell: str | None = context.board[y][x]
                if cell is not None:
                    pygame.draw.rect(
                        self.surface,
                        COLORS.get(cell, (170, 170, 170)),
                        (px + 1, py + 1, TILE_SIZE - 2, TILE_SIZE - 2),
                    )
                    if (x + y) % 2 == 0:
                        pygame.draw.circle(self.surface, (255, 255, 255), (px + TILE_SIZE - 9, py + 9), 3)
                    self._draw_cat_tiara(px, py)

    def _draw_piece(self, piece: Tetromino, fallback: tuple[int, int, int] | None) -> None:
        occupied_tiles: list[tuple[int, int]] = []
        base_color: tuple[int, int, int] = COLORS[piece.piece_type]
        for y, row in enumerate(piece.matrix):
            for x, cell in enumerate(row):
                if cell == 0:
                    continue
                px: int = (piece.position.x + x) * TILE_SIZE
                py: int = (piece.position.y + y) * TILE_SIZE
                color: tuple[int, int, int] = fallback if fallback is not None else base_color
                pygame.draw.rect(self.surface, color, (px + 1, py + 1, TILE_SIZE - 2, TILE_SIZE - 2))
                if fallback is None:
                    occupied_tiles.append((px, py))
        if fallback is None and occupied_tiles:
            self._draw_piece_cat_overlay(occupied_tiles, piece.piece_type)

    def _draw_cat_tiara(self, px: int, py: int) -> None:
        """Draw a tiny cat face with tiara on a block."""
        center_x: int = px + TILE_SIZE // 2
        center_y: int = py + TILE_SIZE // 2 + 1
        ear_color: tuple[int, int, int] = (255, 232, 242)
        face_color: tuple[int, int, int] = (255, 246, 251)
        line_color: tuple[int, int, int] = (156, 88, 118)
        tiara_color: tuple[int, int, int] = (255, 219, 120)

        pygame.draw.polygon(
            self.surface,
            ear_color,
            [(center_x - 6, center_y - 6), (center_x - 2, center_y - 11), (center_x, center_y - 5)],
        )
        pygame.draw.polygon(
            self.surface,
            ear_color,
            [(center_x + 6, center_y - 6), (center_x + 2, center_y - 11), (center_x, center_y - 5)],
        )
        pygame.draw.circle(self.surface, face_color, (center_x, center_y - 1), 5)
        pygame.draw.circle(self.surface, line_color, (center_x - 2, center_y - 2), 1)
        pygame.draw.circle(self.surface, line_color, (center_x + 2, center_y - 2), 1)
        pygame.draw.circle(self.surface, line_color, (center_x, center_y), 1)
        pygame.draw.line(self.surface, line_color, (center_x - 4, center_y), (center_x - 6, center_y + 1), width=1)
        pygame.draw.line(self.surface, line_color, (center_x + 4, center_y), (center_x + 6, center_y + 1), width=1)
        pygame.draw.polygon(
            self.surface,
            tiara_color,
            [(center_x - 6, center_y - 9), (center_x - 2, center_y - 13), (center_x, center_y - 10), (center_x + 2, center_y - 13), (center_x + 6, center_y - 9)],
        )

    def _pick_head_and_body_cells(
        self, grid_cells: set[tuple[int, int]]
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """Pick head cell (top row, near center) and body cell (prefer directly below).

        Args:
            grid_cells: Occupied board cells as (grid_x, grid_y).

        Returns:
            (head_cell, body_cell) as grid coordinates.
        """
        if not grid_cells:
            raise ValueError("grid_cells must not be empty")
        min_gy: int = min(gy for _, gy in grid_cells)
        center_gx: float = sum(gx for gx, _ in grid_cells) / len(grid_cells)
        top_row: list[tuple[int, int]] = [(gx, gy) for gx, gy in grid_cells if gy == min_gy]
        head_cell: tuple[int, int] = min(top_row, key=lambda c: abs(c[0] - center_gx))
        hgx, hgy = head_cell

        below: tuple[int, int] = (hgx, hgy + 1)
        if below in grid_cells:
            return (head_cell, below)

        for dx in (0, -1, 1, 2, -2):
            candidate: tuple[int, int] = (hgx + dx, hgy + 1)
            if candidate in grid_cells:
                return (head_cell, candidate)

        if (hgx + 1, hgy) in grid_cells:
            return (head_cell, (hgx + 1, hgy))
        if (hgx - 1, hgy) in grid_cells:
            return (head_cell, (hgx - 1, hgy))

        others: list[tuple[int, int]] = [c for c in grid_cells if c != head_cell]
        if not others:
            return (head_cell, head_cell)
        body_cell: tuple[int, int] = min(
            others,
            key=lambda c: (c[1] - hgy, abs(c[0] - hgx)),
        )
        return (head_cell, body_cell)

    def _draw_piece_cat_overlay(self, occupied_tiles: list[tuple[int, int]], piece_type: str) -> None:
        """Draw an upright tiara cat: head in one block, body and front paws in the block below."""
        grid_cells: set[tuple[int, int]] = {(px // TILE_SIZE, py // TILE_SIZE) for px, py in occupied_tiles}
        head_cell, body_cell = self._pick_head_and_body_cells(grid_cells)
        head_gc, head_gr = head_cell
        body_gc, body_gr = body_cell

        fur_color: tuple[int, int, int] = CAT_FUR_COLORS.get(piece_type, (255, 243, 250))
        outline_color: tuple[int, int, int] = CAT_OUTLINE_COLORS.get(piece_type, (150, 100, 130))

        head_px: int = head_gc * TILE_SIZE
        head_py: int = head_gr * TILE_SIZE
        body_px: int = body_gc * TILE_SIZE
        body_py: int = body_gr * TILE_SIZE

        head_cx: int = head_px + TILE_SIZE // 2
        head_cy: int = head_py + TILE_SIZE // 3
        head_radius: int = max(6, TILE_SIZE // 3 - 1)

        same_cell: bool = (head_gc, head_gr) == (body_gc, body_gr)
        vertical_stack: bool = (not same_cell) and body_gr > head_gr

        if same_cell:
            head_cy = head_py + TILE_SIZE // 4
            compact_torso: pygame.Rect = pygame.Rect(
                head_px + 4,
                head_py + TILE_SIZE // 2,
                TILE_SIZE - 8,
                TILE_SIZE // 2 - 4,
            )
            pygame.draw.ellipse(self.surface, fur_color, compact_torso)
            pygame.draw.ellipse(self.surface, outline_color, compact_torso, width=2)
            compact_paw_y: int = head_py + TILE_SIZE - 6
            for offset in (-6, 6):
                pr = pygame.Rect(head_cx + offset - 4, compact_paw_y - 3, 8, 5)
                pygame.draw.ellipse(self.surface, fur_color, pr)
                pygame.draw.ellipse(self.surface, outline_color, pr, width=1)
            pygame.draw.line(
                self.surface,
                outline_color,
                (head_cx, head_cy + head_radius - 1),
                (head_cx, compact_torso.top + 2),
                width=2,
            )
        elif vertical_stack:
            # Torso sits in upper-middle of body block; paws at bottom of body block.
            torso_cx: int = body_px + TILE_SIZE // 2
            torso_cy: int = body_py + TILE_SIZE // 3
            torso_w: int = max(12, TILE_SIZE - 10)
            torso_h: int = max(10, TILE_SIZE // 2)
            torso_rect: pygame.Rect = pygame.Rect(0, 0, torso_w, torso_h)
            torso_rect.center = (torso_cx, torso_cy)
            pygame.draw.ellipse(self.surface, fur_color, torso_rect)
            pygame.draw.ellipse(self.surface, outline_color, torso_rect, width=2)

            paw_y: int = body_py + TILE_SIZE - 8
            paw_w: int = max(6, TILE_SIZE // 5)
            paw_h: int = 6
            left_paw: pygame.Rect = pygame.Rect(torso_cx - torso_w // 3 - paw_w // 2, paw_y - paw_h // 2, paw_w, paw_h)
            right_paw: pygame.Rect = pygame.Rect(torso_cx + torso_w // 3 - paw_w // 2, paw_y - paw_h // 2, paw_w, paw_h)
            pygame.draw.ellipse(self.surface, fur_color, left_paw)
            pygame.draw.ellipse(self.surface, fur_color, right_paw)
            pygame.draw.ellipse(self.surface, outline_color, left_paw, width=1)
            pygame.draw.ellipse(self.surface, outline_color, right_paw, width=1)

            neck_bottom: int = head_cy + head_radius - 2
            neck_top: int = torso_rect.top + 2
            pygame.draw.line(
                self.surface,
                outline_color,
                (head_cx, neck_bottom),
                (torso_cx, neck_top),
                width=2,
            )

            tail_cx: int = body_px + TILE_SIZE - 6
            tail_cy: int = body_py + TILE_SIZE // 2
            pygame.draw.arc(
                self.surface,
                outline_color,
                pygame.Rect(tail_cx - 10, tail_cy - 4, 16, 18),
                0.8,
                3.6,
                width=2,
            )
        else:
            # Side-by-side: head in one cell, body+paws in the adjacent cell (e.g. horizontal I).
            torso_cx: int = body_px + TILE_SIZE // 2
            torso_cy: int = body_py + TILE_SIZE // 2 - 2
            torso_w: int = max(10, TILE_SIZE - 8)
            torso_h: int = max(14, TILE_SIZE - 6)
            torso_rect = pygame.Rect(0, 0, torso_w, torso_h)
            torso_rect.center = (torso_cx, torso_cy)
            pygame.draw.ellipse(self.surface, fur_color, torso_rect)
            pygame.draw.ellipse(self.surface, outline_color, torso_rect, width=2)
            paw_y = body_py + TILE_SIZE - 7
            paw_w = max(5, TILE_SIZE // 6)
            for offset in (-8, 8):
                pr = pygame.Rect(torso_cx + offset - paw_w // 2, paw_y - 3, paw_w, 6)
                pygame.draw.ellipse(self.surface, fur_color, pr)
                pygame.draw.ellipse(self.surface, outline_color, pr, width=1)
            hx_edge: int = head_px + TILE_SIZE if body_gc > head_gc else head_px
            tx_edge: int = body_px if body_gc > head_gc else body_px + TILE_SIZE
            pygame.draw.line(
                self.surface,
                outline_color,
                (hx_edge, head_cy + 2),
                (tx_edge, torso_rect.centery),
                width=2,
            )

        pygame.draw.circle(self.surface, fur_color, (head_cx, head_cy), head_radius)
        pygame.draw.circle(self.surface, outline_color, (head_cx, head_cy), head_radius, width=2)

        left_ear: list[tuple[int, int]] = [
            (head_cx - head_radius + 2, head_cy - head_radius + 2),
            (head_cx - 2, head_cy - head_radius - 6),
            (head_cx - 1, head_cy - head_radius + 4),
        ]
        right_ear: list[tuple[int, int]] = [
            (head_cx + head_radius - 2, head_cy - head_radius + 2),
            (head_cx + 2, head_cy - head_radius - 6),
            (head_cx + 1, head_cy - head_radius + 4),
        ]
        pygame.draw.polygon(self.surface, fur_color, left_ear)
        pygame.draw.polygon(self.surface, fur_color, right_ear)
        pygame.draw.polygon(self.surface, outline_color, left_ear, width=2)
        pygame.draw.polygon(self.surface, outline_color, right_ear, width=2)

        eye_offset: int = max(2, head_radius // 3)
        pygame.draw.circle(self.surface, (95, 64, 78), (head_cx - eye_offset, head_cy - 1), 1)
        pygame.draw.circle(self.surface, (95, 64, 78), (head_cx + eye_offset, head_cy - 1), 1)
        pygame.draw.circle(self.surface, (95, 64, 78), (head_cx, head_cy + 1), 1)

        tiara: list[tuple[int, int]] = [
            (head_cx - head_radius, head_cy - head_radius),
            (head_cx - eye_offset, head_cy - head_radius - 5),
            (head_cx, head_cy - head_radius - 2),
            (head_cx + eye_offset, head_cy - head_radius - 5),
            (head_cx + head_radius, head_cy - head_radius),
        ]
        pygame.draw.polygon(self.surface, (255, 220, 130), tiara)
        pygame.draw.polygon(self.surface, (205, 156, 72), tiara, width=1)

    def _draw_mini_shape(
        self,
        piece_type: TetrominoType,
        slot_x: int,
        slot_y: int,
    ) -> None:
        """Draw a small tetromino preview (actual block layout) inside a slot.

        Args:
            piece_type: Which tetromino to draw.
            slot_x: Left of preview slot in screen pixels.
            slot_y: Top of preview slot in screen pixels.
        """
        matrix: list[list[int]] = SHAPES[piece_type]
        rows: int = len(matrix)
        cols: int = len(matrix[0])
        min_r: int = rows
        max_r: int = -1
        min_c: int = cols
        max_c: int = -1
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]:
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
        if max_r < 0:
            return

        cell: int = PREVIEW_CELL
        piece_w: int = (max_c - min_c + 1) * cell
        piece_h: int = (max_r - min_r + 1) * cell
        origin_x: int = slot_x + (PREVIEW_SLOT_W - piece_w) // 2
        origin_y: int = slot_y + (PREVIEW_SLOT_H - piece_h) // 2
        fill: tuple[int, int, int] = COLORS[piece_type]
        border: tuple[int, int, int] = (120, 90, 110)

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if not matrix[r][c]:
                    continue
                px: int = origin_x + (c - min_c) * cell
                py: int = origin_y + (r - min_r) * cell
                pygame.draw.rect(self.surface, fill, (px + 1, py + 1, cell - 2, cell - 2))
                pygame.draw.rect(self.surface, border, (px, py, cell, cell), width=1)

    def _draw_panel(self, context: GameContext) -> None:
        x: int = BOARD_WIDTH * TILE_SIZE + 16
        panel_h: int = 420
        pygame.draw.rect(self.surface, (255, 247, 252), (x - 10, 24, 220, panel_h), border_radius=12)
        pygame.draw.rect(self.surface, (238, 175, 211), (x - 10, 24, 220, panel_h), width=2, border_radius=12)
        self.surface.blit(self.font.render(f"Score: {context.metrics.score}", True, (142, 74, 109)), (x, 36))
        self.surface.blit(self.font.render(f"Level: {context.metrics.level}", True, (142, 74, 109)), (x, 66))
        self.surface.blit(
            self.font.render(f"Lines: {context.metrics.lines_cleared}", True, (142, 74, 109)),
            (x, 96),
        )
        self.surface.blit(
            self.font.render(f"High: {context.metrics.high_score}", True, (142, 74, 109)),
            (x, 126),
        )
        if context.player_name.strip():
            self.surface.blit(
                self.small_font.render(f"Player: {context.player_name}", True, (142, 74, 109)),
                (x, 150),
            )
        self.surface.blit(self.font.render("Next", True, (191, 103, 148)), (x, 172))
        next_start_y: int = 194
        row_step: int = PREVIEW_SLOT_H + 4
        for idx, piece_type in enumerate(context.queue.next_pieces[:3]):
            slot_y: int = next_start_y + idx * row_step
            pygame.draw.rect(
                self.surface,
                (252, 240, 248),
                (x, slot_y, PREVIEW_SLOT_W, PREVIEW_SLOT_H),
                border_radius=6,
            )
            pygame.draw.rect(
                self.surface,
                (220, 180, 205),
                (x, slot_y, PREVIEW_SLOT_W, PREVIEW_SLOT_H),
                width=1,
                border_radius=6,
            )
            self._draw_mini_shape(piece_type, x, slot_y)
        hold_label_y: int = next_start_y + 3 * row_step + 2
        self.surface.blit(self.font.render("Hold", True, (191, 103, 148)), (x, hold_label_y))
        hold_slot_y: int = hold_label_y + 22
        if context.queue.hold_piece is not None:
            pygame.draw.rect(
                self.surface,
                (252, 240, 248),
                (x, hold_slot_y, PREVIEW_SLOT_W, PREVIEW_SLOT_H),
                border_radius=6,
            )
            pygame.draw.rect(
                self.surface,
                (220, 180, 205),
                (x, hold_slot_y, PREVIEW_SLOT_W, PREVIEW_SLOT_H),
                width=1,
                border_radius=6,
            )
            self._draw_mini_shape(context.queue.hold_piece, x, hold_slot_y)
        self.surface.blit(
            self.small_font.render("=^.^= royal cat mode", True, (191, 103, 148)),
            (x - 2, panel_h + 8),
        )

    def _draw_overlay(self, context: GameContext) -> None:
        if context.play_state == "playing":
            return
        overlay: pygame.Surface = pygame.Surface((BOARD_WIDTH * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
        overlay.fill((111, 63, 92, 118))
        self.surface.blit(overlay, (0, 0))
        if context.play_state == "name_entry":
            self.surface.blit(self.title_font.render("Princess Cat Tetris", True, (255, 238, 246)), (24, 60))
            self.surface.blit(self.font.render("Enter your player name:", True, (255, 245, 251)), (24, 110))
            entry: str = context.player_name if context.player_name else "_"
            self.surface.blit(self.font.render(entry, True, (255, 220, 245)), (24, 145))
            self.surface.blit(
                self.small_font.render("Press Enter to start", True, (255, 213, 238)),
                (24, 180),
            )
            self.surface.blit(
                self.small_font.render("Backspace deletes. Max 14 chars.", True, (255, 213, 238)),
                (24, 205),
            )
            return
        if context.play_state == "high_scores":
            self.surface.blit(self.title_font.render("High Scores", True, (255, 238, 246)), (24, 60))
            if not context.high_scores:
                self.surface.blit(self.font.render("No scores yet.", True, (255, 245, 251)), (24, 110))
            for idx, row in enumerate(context.high_scores[:8]):
                text: str = f"{idx + 1:>2}. {row.player_name:<14} {row.score}"
                self.surface.blit(self.small_font.render(text, True, (255, 245, 251)), (24, 105 + idx * 24))
            self.surface.blit(
                self.small_font.render("Press Enter to play again", True, (255, 213, 238)),
                (24, 320),
            )
            return
        if context.play_state == "paused":
            text = "Paused"
            self.surface.blit(self.font.render(text, True, (255, 255, 255)), (24, 240))
            return
        if context.play_state == "game_over":
            self.surface.blit(self.font.render("Game Over", True, (255, 255, 255)), (24, 220))
            self.surface.blit(
                self.small_font.render("Press Enter for High Scores", True, (255, 213, 238)),
                (24, 252),
            )
            return

        self.surface.blit(self.title_font.render("Princess Cat Tetris", True, (255, 238, 246)), (24, 70))
        self.surface.blit(self.small_font.render("Press Enter to continue", True, (255, 245, 251)), (24, 118))
