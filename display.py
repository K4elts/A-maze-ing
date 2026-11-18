from typing import Callable

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8
ALL_WALLS: int = 15

RESET: str = "\033[0m"
CLEAR_SCREEN: str = "\033[2J\033[H"
ENTRY_COLOR: str = "\033[1;97m"  # bold white
EXIT_COLOR: str = "\033[1;91m"  # bold red
PATTERN_COLOR: str = "\033[93m"  # yellow, for the "42" cells

WALL_COLORS: list[str] = [
    "\033[95m",  # pink (bright magenta)
    "\033[97m",  # white
    "\033[96m",  # cyan
    "\033[92m",  # green
    "\033[91m",  # red
]

PATH_COLORS: list[str] = [
    "\033[102m",  # green
    "\033[105m",  # pink (bright magenta)
    "\033[103m",  # yellow
    "\033[106m",  # cyan
]


def path_cells(
    entry: tuple[int, int],
    solution: str,
) -> set[tuple[int, int]]:
    """
    Calculates the set of maze cells visited by following a path
    from the given entry point using the specified directions.

    Each letter in the solution represents a movement:
    N (North), S (South), E (East) or W (West).

    Args:
        entry (tuple[int, int]): Starting coordinates (row, col).
        solution (str): Sequence of direction letters describing
            the path to follow (e.g. "EES").

    Returns:
        set[tuple[int, int]]: A set of (row, col) coordinates
        representing all cells visited after each movement.
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
    """
    Draws the maze in the terminal, displaying its walls, entry point,
    exit point and, optionally, the solution path using ANSI colours.

    Each cell draws only its north and west walls, so shared walls are
    drawn once. The last column adds its east wall and the last row its
    south wall. Fully closed cells (the "42" pattern) are filled with
    PATTERN_COLOR. All coordinates use (row, col).

    Args:
        maze (list[list[int]]): The maze represented as a list of rows,
            where each cell is an integer from 0 to 15 indicating
            its surrounding walls.
        entry (tuple[int, int]): Entry coordinates (row, col),
            displayed as a green "E".
        exit_cell (tuple[int, int]): Exit coordinates (row, col),
            displayed as a red "X".
        path (set[tuple[int, int]]): Set of (row, col) coordinates
            belonging to the solution path. An empty set hides the path.
        wall_color (str): ANSI colour code used to draw the maze walls.
        path_color (str): ANSI background colour code used to highlight
            the solution path. Defaults to PATH_COLORS[0].
    Returns:
        None
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
                label = PATTERN_COLOR + "███"
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
    """
    Generates a summary of the maze, including its dimensions, type
    and solution path length.

    Args:
        maze (list[list[int]]): The maze represented as a list of rows.
        solution (str): The solution path represented as a sequence
            of direction letters.
        perfect (bool): Indicates whether the maze is a perfect maze.
            If False, the maze is classified as a Pac-Man maze.

    Returns:
        str: A formatted string containing the maze dimensions
        (width x height), its type and the number of steps
        in the solution path.
    """
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
    """
    Displays the maze in the terminal and provides an interactive menu
    that allows the user to modify its appearance and manage its
    generation until they choose to quit.

    The menu provides options to generate a new maze, toggle the
    solution path, change the wall colour and change the path colour.
    User input is handled interactively, with error messages displayed
    when an invalid option is selected or maze regeneration fails.

    Args:
        maze (list[list[int]]): The maze represented as a list of rows,
            where each cell is an integer from 0 to 15 indicating
            its surrounding walls.
        entry (tuple[int, int]): Entry coordinates (row, col).
        exit_cell (tuple[int, int]): Exit coordinates (row, col).
        solution (str): Shortest path from entry to exit, represented
            as a sequence of direction letters (e.g. "EES").
        regenerate (Callable[[], tuple[list[list[int]], str]]): Function
            that generates a new maze and returns it together with
            its corresponding solution.
        perfect (bool): Indicates whether the maze is perfect.
            Used to display the maze type in the information line.
            Defaults to True.
        notice (str): Optional additional message displayed below
            the maze information line. Defaults to an empty string.

    Returns:
        None
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
            raise

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
