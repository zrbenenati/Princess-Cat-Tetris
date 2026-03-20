"""Convert raw pygame events into domain actions."""

import pygame

from game.types import InputAction

KEYMAP: dict[int, InputAction] = {
    pygame.K_LEFT: "move_left",
    pygame.K_RIGHT: "move_right",
    pygame.K_DOWN: "soft_drop",
    pygame.K_SPACE: "hard_drop",
    pygame.K_UP: "rotate_cw",
    pygame.K_z: "rotate_ccw",
    pygame.K_c: "hold",
    pygame.K_p: "toggle_pause",
    pygame.K_RETURN: "start_game",
    pygame.K_BACKSPACE: "backspace",
}


def handle_events() -> tuple[list[InputAction], str, bool]:
    """Read pygame events and map key presses into actions.

    Returns:
        Tuple of (actions, typed_text, should_quit).
    """
    actions: list[InputAction] = []
    typed_text: str = ""
    should_quit: bool = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_quit = True
        elif event.type == pygame.KEYDOWN:
            action: InputAction | None = KEYMAP.get(event.key)
            if action is not None:
                actions.append(action)
            if (
                event.unicode
                and event.unicode.isprintable()
                and event.key not in (pygame.K_RETURN, pygame.K_BACKSPACE)
            ):
                typed_text += event.unicode
    return (actions, typed_text, should_quit)
