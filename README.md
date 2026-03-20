# Princess Cat Tetris

Modular Tetris implementation in Python with `pygame-ce` (princess cat theme).

## Structure

- `game/` core loop, state machine, context
- `entities/` tetromino models
- `systems/` movement, collision, rotation, spawn, hold, scoring
- `rendering/` drawing and HUD
- `input/` event-to-action mapping
- `utils/` constants and random queue helpers
- `tests/` pure logic tests

## Run

```bash
python3 -m pip install -r requirements.txt
python3 run.py
```

## Test

```bash
python3 -m pytest -q
```

## Web deployment note

This is Python-first. For browser delivery, package with `pygbag`:

```bash
python3 -m pip install pygbag
pygbag .
```
