"""Grid Escape: a small terminal game for a Coding with AI class.

Phase 1 keeps the project intentionally simple:
- The player moves around a small grid.
- Walls block movement.
- The goal is to reach the exit.

The code is organized into beginner-friendly functions so future students
can extend the game with new mechanics later.
"""


def create_map():
    """Create and return the starting game map as a 2D list of characters."""
    return [
        list("########"),
        list("#P   # #"),
        list("# ##   #"),
        list("#  ##  #"),
        list("#   # E#"),
        list("########"),
    ]



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

    Returns True if the move happened.
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

    # Move the player to the new space.
    # If the new tile is the exit, we still place P there so the map reflects
    # the player's final position before the game ends.
    game_map[current_row][current_col] = " "
    game_map[new_row][new_col] = "P"
    return True



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

    print("Welcome to Grid Escape!")
    print("Reach the exit (E) without walking through walls (#).")
    print("Use w = up, a = left, s = down, d = right.")

    while True:
        print_map(game_map)
        command = input("Enter your move (w/a/s/d): ").strip().lower()

        # Basic input validation helps keep the game beginner-friendly.
        if command not in {"w", "a", "s", "d"}:
            print("Invalid command. Please use only w, a, s, or d.")
            continue

        moved = move_player(game_map, command)
        if not moved:
            print("You bumped into a wall. Try a different direction.")
            continue

        if check_win(game_map):
            print_map(game_map)
            print("You escaped the grid. You win!")
            break


if __name__ == "__main__":
    main()
