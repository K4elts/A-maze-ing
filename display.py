'''DRAWS THE MAZE IN THE TERMINAL'''
from typing import Callable

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8
ALL_WALLS: int = 15

RESET: str = "\033[0m"
CLEAR_SCREEN: str = "\033[2J\033[H"
ENTRY_COLOR: str = "\033[1;92m"  # bold green
EXIT_COLOR: str = "\033[1;91m"  # bold red

WALL_COLORS: list[str] = [
    "\033[92m",  # green
    "\033[97m",  # white
    "\033[96m",  # cyan
    "\033[95m",  # magenta
    "\033[91m",  # red
]

PATH_COLORS: list[str] = [
    "\033[105m",  # magenta
    "\033[103m",  # yellow
    "\033[102m",  # green
    "\033[106m",  # cyan
]


def path_cells(
    entry: tuple[int, int],
    solution: str,
) -> set[tuple[int, int]]:
    """Return the cells the path goes through, following its letters.

    Args:
        entry: Entry coordinates (row, col), where the path starts.
        solution: Path as letters N, E, S, W, e.g. "EES".

    Returns:
        The set of (row, col) cells visited after each step.
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
    path_color: str = PATH_COLORS[0],
) -> None:
    """Draw the maze walls, entry, exit and path in the terminal.

    Each cell draws only its north and west walls, so shared walls are
    drawn once. The last column adds its east wall and the last row its
    south wall. Fully closed cells (the "42" pattern) are filled with the
    wall colour. All coordinates use (row, col).

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (row, col), drawn as a green "E".
        exit_cell: Exit coordinates (row, col), drawn as a red "X".
        path: Cells of the path, drawn with a coloured background;
            an empty set hides it.
        wall_color: ANSI code used to colour the walls.
        path_color: ANSI code used as background for the path.
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
                top += corner + path_color + "   " + RESET
            else:
                top += corner + "   "
        print(top + corner)

        middle = ""

        for col_idx, cell in enumerate(row):
            position = (row_idx, col_idx)

            if position == entry:
                label = ENTRY_COLOR + " E "
            elif position == exit_cell:
                label = EXIT_COLOR + " X "
            elif cell == ALL_WALLS:
                label = wall_color + "███"
            else:
                label = "   "

            if position in on_path:
                inside = path_color + label + RESET
            else:
                inside = label + RESET

            if cell & WEST:
                middle += wall_v + inside
            elif (
                position in on_path
                and (row_idx, col_idx - 1) in on_path
            ):
                middle += path_color + " " + RESET + inside
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


def maze_info(maze: list[list[int]], solution: str, perfect: bool) -> str:
    """Return a short line with the maze size, its type and path length."""
    height = len(maze)
    width = len(maze[0])
    kind = "perfect" if perfect else "Pac-Man"
    return f"{width}x{height} | {kind} | path: {len(solution)} steps"


MENU: str = """
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Rotate the path colour
5. Quit"""


def run_menu(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    solution: str,
    regenerate: Callable[[], tuple[list[list[int]], str]],
    perfect: bool = True,
    notice: str = "",
) -> None:
    """Draw the maze and let the user interact with it until they quit.

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (row, col).
        exit_cell: Exit coordinates (row, col).
        solution: Shortest path from entry to exit, e.g. "EES".
        regenerate: Function that builds a new maze and returns it
            together with its solution.
        perfect: Whether the maze is perfect, shown in the info line.
        notice: Optional extra line shown under the info line.
    """
    show_path = False
    color_index = 0
    path_color_index = 0
    message = ""

    while True:
        print(CLEAR_SCREEN, end="")
        if show_path:
            path = path_cells(entry, solution)
        else:
            path = set()
        draw_maze(
            maze, entry, exit_cell, path,
            WALL_COLORS[color_index], PATH_COLORS[path_color_index],
        )
        print()
        print(maze_info(maze, solution, perfect))
        if notice:
            print(notice)
        print(MENU)
        if message:
            print(message)
            message = ""

        try:
            choice = input("Choice? (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "1":
            try:
                maze, solution = regenerate()
                message = "New maze generated."
            except (OSError, RuntimeError) as error:
                message = f"Error: {error}"
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            path_color_index = (path_color_index + 1) % len(PATH_COLORS)
        elif choice == "5":
            break
        else:
            message = "Invalid choice: please type a number from 1 to 5."


if __name__ == "__main__":
    test_maze = [[9, 5, 3], [12, 5, 6], [15, 15, 15]]

    def same_maze() -> tuple[list[list[int]], str]:
        """Return the same test maze, to try the menu without a generator."""
        return test_maze, "EES"

    run_menu(test_maze, (0, 0), (1, 2), "EES", same_maze)
