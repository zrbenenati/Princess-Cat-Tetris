"""Game loop entry and runtime orchestration."""

import pygame

from game.tetris_game import TetrisGame
from input.input_handler import handle_events
from rendering.renderer import Renderer
from utils.constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH


def run_game() -> None:
    """Run the main game loop.

    The loop follows the standard:
    handle_input -> update(delta_time) -> render
    """
    pygame.init()
    pygame.display.set_caption("Princess Cat Tetris")
    surface: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    renderer: Renderer = Renderer(surface)
    game: TetrisGame = TetrisGame()
    running: bool = True
    while running:
        actions, should_quit = handle_events()
        if should_quit:
            running = False
            continue
        delta_seconds: float = clock.tick(FPS) / 1000.0
        game.frame_update(delta_seconds, actions)
        renderer.render(game.context)
    pygame.quit()
