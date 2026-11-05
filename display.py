'''DRAWS THE MAZE IN THE TERMINAL'''

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

RESET: str = "\033[0m"
PATH_COLOR: str = "\033[103m"
CLEAR_SCREEN: str = "\033[2J\033[H"

WALL_COLORS: list[str] = [
    "\033[97m",  # white
    "\033[96m",  # cyan
    "\033[95m",  # magenta
    "\033[92m",  # green
    "\033[91m",  # red
]


def path_cells(
    entry: tuple[int, int],
    solution: str,
) -> set[tuple[int, int]]:
    """Return the cells the path goes through, following its letters.

    Args:
        entry: Entry coordinates (x, y), where the path starts.
        solution: Path as letters N, E, S, W, e.g. "EES".

    Returns:
        The set of (x, y) cells visited after each step.
    """
    cells: set[tuple[int, int]] = set()
    row, col = entry
    for letter in solution:
        if letter == "N":
            row -= 1
        elif letter == "S":
            row += 1
        elif letter == "E":
            col += 1
        elif letter == "W":
            col -= 1
        cells.add((row, col))
    return cells


def draw_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: set[tuple[int, int]],
    wall_color: str,
) -> None:
    """Draw the maze walls, entry, exit and path in the terminal.

    All coordinates use (row, column).
    """
    corner = wall_color + "+" + RESET
    wall_h = wall_color + "+---" + RESET
    wall_v = wall_color + "|" + RESET

    if path:
        on_path = path | {entry}
    else:
        on_path = set()

    for row_idx, row in enumerate(maze):
        top = ""

        for col_idx, cell in enumerate(row):
            if cell & NORTH:
                top += wall_h
            elif (
                (row_idx, col_idx) in on_path
                and (row_idx - 1, col_idx) in on_path
            ):
                top += corner + PATH_COLOR + "   " + RESET
            else:
                top += corner + "   "
        print(top + corner)

        middle = ""

        for col_idx, cell in enumerate(row):
            position = (row_idx, col_idx)

            if position == entry:
                label = " E "
            elif position == exit_cell:
                label = " X "
            else:
                label = "   "

            if position in on_path:
                inside = PATH_COLOR + label + RESET
            else:
                inside = label

            if cell & WEST:
                middle += wall_v + inside
            elif (
                position in on_path
                and (row_idx, col_idx - 1) in on_path
            ):
                middle += PATH_COLOR + " " + RESET + inside
            else:
                middle += " " + inside

        if row[-1] & EAST:
            middle += wall_v
        else:
            middle += " "
        print(middle)

    bottom = ""

    for cell in maze[-1]:
        if cell & SOUTH:
            bottom += wall_h
        else:
            bottom += corner + "   "
    print(bottom + corner)


MENU: str = """
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit"""


def run_menu(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    solution: str,
) -> None:
    """Draw the maze and let the user interact with it until they quit.

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (x, y).
        exit_cell: Exit coordinates (x, y).
        solution: Shortest path from entry to exit, e.g. "EES".
    """
    show_path = False
    color_index = 0
    message = ""

    while True:
        print(CLEAR_SCREEN, end="")
        if show_path:
            path = path_cells(entry, solution)
        else:
            path = set()
        draw_maze(maze, entry, exit_cell, path, WALL_COLORS[color_index])
        print(MENU)
        if message:
            print(message)
            message = ""

        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1":
            message = "Re-generating is not available yet."
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            message = "Invalid choice: please type 1, 2, 3 or 4."


if __name__ == "__main__":
    test_maze = [[9, 5, 3], [12, 5, 6]]
    run_menu(test_maze, (0, 0), (2, 1), "EES")
