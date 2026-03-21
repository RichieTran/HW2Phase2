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
- Enemies shown with `X`.
- Movement in four directions.
- Enemy movement for next round shown with `^`, `<`, `>`, and `v`.
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

=======================================================================

## Phase 2

### Features

- Larger 31x21 randomly generated maze with multiple possible paths.
- Key (`K`) spawns randomly — pick it up to unlock the door.
- Locked door (`U`) blocks the exit until the key is collected, then becomes `E`.
- Fog of war — only tiles within a radius of 4 around the player are visible; everything else is hidden (`.`).
- 3 enemies (`X`) move each turn — directional arrows (`^`, `v`, `<`, `>`) show where they'll go next.
- Enemies cannot spawn right next to the player.
- Move counter tracks how many moves you've taken.
- Win by reaching the unlocked exit (`E`). Lose if an enemy catches you.

### Functions created in Phase 2

- `place_enemies()` — randomly places enemies on empty cells (not near the player).
- `find_enemies()` — returns all enemy positions on the map.
- `move_enemies()` — moves each enemy to its planned or random adjacent cell.
- `plan_enemy_moves()` — pre-decides each enemy's next move and places directional arrows.
- `check_enemy()` — checks if a cell contains an enemy.
- `clear_markers()` — removes direction arrows from the map before enemies move.

### Ideas for future expansion

If more time were available, the game could be extended with:

- **Multiple levels** — after escaping, load a new, harder maze (larger grid, more enemies).
- **Difficulty scaling** — increase enemy count or speed as levels progress.
- **Multiple keys / doors** — require the player to collect several keys in order.
- **Pathfinding enemies** — smarter enemies that chase the player instead of moving randomly.
- **Traps** — hidden tiles that teleport the player or slow them down.
- **Inventory system** — collect and use multiple items (shield, speed boost, etc.).
