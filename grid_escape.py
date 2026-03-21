"""Grid Escape: a small terminal game for a Coding with AI class.

Phase 1 keeps the project intentionally simple:
- The player moves around a small grid.
- Walls block movement.
- The goal is to reach the exit.

The code is organized into beginner-friendly functions so future students
can extend the game with new mechanics later.
"""

import random


def create_map(width=15, height=9):
    """Create a randomized map with a guaranteed path from P to E.

    Uses recursive backtracking to carve a maze, then places
    the player in the top-left open area and the exit in the
    bottom-right open area.

    Width and height must be odd numbers so the maze grid works properly.
    """
    # Ensure odd dimensions for the maze algorithm.
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # Start with everything as walls.
    game_map = [["#"] * width for _ in range(height)]

    # Carve passages using recursive backtracking (DFS).
    def carve(r, c):
        game_map[r][c] = " "
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr < height - 1 and 1 <= nc < width - 1 and game_map[nr][nc] == "#":
                # Knock out the wall between current cell and neighbor.
                game_map[r + dr // 2][c + dc // 2] = " "
                carve(nr, nc)

    carve(1, 1)

    # Remove some extra walls to create alternative paths (loops in the maze).
    inner_walls = []
    for r in range(2, height - 2):
        for c in range(2, width - 2):
            if game_map[r][c] == "#":
                # Check if this wall sits between two open passages.
                if (game_map[r - 1][c] == " " and game_map[r + 1][c] == " " and
                        game_map[r][c - 1] == "#" and game_map[r][c + 1] == "#"):
                    inner_walls.append((r, c))
                elif (game_map[r][c - 1] == " " and game_map[r][c + 1] == " " and
                      game_map[r - 1][c] == "#" and game_map[r + 1][c] == "#"):
                    inner_walls.append((r, c))
    random.shuffle(inner_walls)
    walls_to_remove = max(1, len(inner_walls) // 4)
    for r, c in inner_walls[:walls_to_remove]:
        game_map[r][c] = " "

    # Place player top-left, exit bottom-right.
    game_map[1][1] = "P"

    # Find the bottom-right-most open cell for the exit.
    exit_row, exit_col = height - 2, width - 2
    game_map[exit_row][exit_col] = "E"

    return game_map



def place_enemies(game_map, count=1):
    """Place a number of enemies (X) on random empty spaces in the map."""
    player_pos = find_player(game_map)
    empty_cells = []
    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            if cell == " ":
                if player_pos and abs(row_index - player_pos[0]) + abs(col_index - player_pos[1]) <= 2:
                    continue
                empty_cells.append((row_index, col_index))
    random.shuffle(empty_cells)
    for row_index, col_index in empty_cells[:count]:
        game_map[row_index][col_index] = "X"


def find_enemies(game_map):
    """Return a list of (row, col) positions for all enemies on the map."""
    enemies = []
    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            if cell == "X":
                enemies.append((row_index, col_index))
    return enemies


DIRECTION_MARKERS = {"^", "v", "<", ">"}


def clear_markers(game_map):
    """Remove all direction markers from the map."""
    for row in game_map:
        for col_index, cell in enumerate(row):
            if cell in DIRECTION_MARKERS:
                row[col_index] = " "


def move_enemies(game_map, planned_moves=None):
    """Move each enemy to its planned cell, or a random adjacent one.

    Enemies must move every turn — they cannot stay on their current tile.
    If an enemy has no valid moves, it stays put as a last resort.
    Returns True if any enemy lands on the player.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    clear_markers(game_map)
    enemies = find_enemies(game_map)
    caught_player = False

    # Build a lookup from current position to planned destination.
    plan = {}
    if planned_moves:
        for (er, ec), (nr, nc) in planned_moves:
            plan[(er, ec)] = (nr, nc)

    for row, col in enemies:
        # Use the planned move if available and still valid.
        target = plan.get((row, col))
        if target:
            nr, nc = target
            cell = game_map[nr][nc]
            if cell in (" ", "P"):
                new_row, new_col = nr, nc
            else:
                target = None

        if not target:
            valid_moves = []
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                cell = game_map[nr][nc]
                if cell in (" ", "P"):
                    valid_moves.append((nr, nc))
            if not valid_moves:
                continue
            new_row, new_col = random.choice(valid_moves)

        if game_map[new_row][new_col] == "P":
            caught_player = True

        game_map[row][col] = " "
        game_map[new_row][new_col] = "X"

    return caught_player


def plan_enemy_moves(game_map):
    """Pre-decide where each enemy will move next and place dots on the map.

    Returns a list of ((current_row, current_col), (next_row, next_col)) tuples.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    enemies = find_enemies(game_map)
    planned = []

    for row, col in enemies:
        valid_moves = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            cell = game_map[nr][nc]
            if cell in (" ", "P", "E") or cell in DIRECTION_MARKERS:
                valid_moves.append((nr, nc))

        if not valid_moves:
            continue

        next_row, next_col = random.choice(valid_moves)
        planned.append(((row, col), (next_row, next_col)))

        # Show a directional arrow on empty spaces.
        dr = next_row - row
        dc = next_col - col
        arrow = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">"}[(dr, dc)]
        if game_map[next_row][next_col] == " ":
            game_map[next_row][next_col] = arrow

    return planned


def check_enemy(game_map, new_row, new_col):
    """Return True if the target cell contains an enemy (X)."""
    return game_map[new_row][new_col] == "X"


def find_player(game_map):
    """Find the player's current row and column in the map."""
    for row_index, row in enumerate(game_map):
        for col_index, cell in enumerate(row):
            if cell == "P":
                return row_index, col_index
    return None



def print_map(game_map):
    """Print the current map state to the terminal."""
    print()
    for row in game_map:
        print("".join(row))
    print()



def is_valid_move(game_map, new_row, new_col):
    """Return True if the player can move into the target cell."""
    target_cell = game_map[new_row][new_col]
    return target_cell != "#"



def move_player(game_map, direction):
    """Try to move the player in the chosen direction.

    Returns "moved" if the move happened normally.
    Returns "enemy" if the player stepped on an enemy.
    Returns False if the move was blocked by a wall.
    """
    player_position = find_player(game_map)
    if player_position is None:
        return False

    current_row, current_col = player_position

    # Translate keyboard commands into row/column movement.
    direction_changes = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }

    row_change, col_change = direction_changes[direction]
    new_row = current_row + row_change
    new_col = current_col + col_change

    if not is_valid_move(game_map, new_row, new_col):
        return False

    hit_enemy = check_enemy(game_map, new_row, new_col)

    # Move the player to the new space.
    game_map[current_row][current_col] = " "
    game_map[new_row][new_col] = "P"

    if hit_enemy:
        return "enemy"
    return "moved"



def check_win(game_map):
    """Return True when the player has reached the exit.

    At the start of the game the map contains one exit tile, E.
    Once the player moves onto that tile, E is replaced by P.
    That means the exit is no longer visible, which tells us the player won.
    """
    for row in game_map:
        if "E" in row:
            return False
    return True



def main():
    """Run the main game loop."""
    game_map = create_map()
    place_enemies(game_map)
    planned_moves = plan_enemy_moves(game_map)

    print("Welcome to Grid Escape!")
    print("Reach the exit (E) without walking through walls (#).")
    print("Watch out for enemies (X)! Arrows (^v<>) show where they'll move next.")
    print("Use w = up, a = left, s = down, d = right.")

    while True:
        print_map(game_map)
        command = input("Enter your move (w/a/s/d): ").strip().lower()

        # Basic input validation helps keep the game beginner-friendly.
        if command not in {"w", "a", "s", "d"}:
            print("Invalid command. Please use only w, a, s, or d.")
            continue

        result = move_player(game_map, command)
        if not result:
            print("You bumped into a wall. Try a different direction.")
            continue

        if result == "enemy":
            print_map(game_map)
            print("An enemy caught you! Game over!")
            break

        if check_win(game_map):
            print_map(game_map)
            print("You escaped the grid. You win!")
            break

        # Enemies move after the player each turn.
        if move_enemies(game_map, planned_moves):
            print_map(game_map)
            print("An enemy caught you! Game over!")
            break

        # Plan and show where enemies will move next turn.
        planned_moves = plan_enemy_moves(game_map)


if __name__ == "__main__":
    main()
