# Grid Escape

Grid Escape is a small text-based Python game for the terminal. The player moves through a simple grid map, avoids walls, and tries to reach the exit.

## How to run it

1. Make sure Python 3 is installed.
2. Open a terminal in this project folder.
3. Run:

```bash
python3 grid_escape.py
```

## Controls

- `w` = move up
- `a` = move left
- `s` = move down
- `d` = move right

## Phase 1 features completed

- A 2D grid map built with characters.
- Walls shown with `#`.
- Player shown with `P`.
- Exit shown with `E`.
- Movement in four directions.
- Wall collision so the player cannot move through walls.
- Input validation for invalid commands.
- Win condition when the player reaches the exit.
- Clear functions and comments so another student can continue the project later.

## Project structure

The main game code lives in `grid_escape.py` and is split into small functions:

- `create_map()`
- `find_player()`
- `print_map()`
- `is_valid_move()`
- `move_player()`
- `check_win()`
- `main()`

## Ideas for future expansion

This Phase 1 version is intentionally small so it is easy to grow later. Future versions could add:

- keys and doors
- enemies
- multiple levels
- a timer or score system
