'''DRAWS THE MAZE IN THE TERMINAL'''

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

RESET: str = "\033[0m"
PATH_COLOR: str = "\033[103m"


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
    x, y = entry
    for letter in solution:
        if letter == "N":
            y -= 1
        elif letter == "S":
            y += 1
        elif letter == "E":
            x += 1
        elif letter == "W":
            x -= 1
        cells.add((x, y))
    return cells


def draw_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: set[tuple[int, int]],
) -> None:
    """Draw the maze walls, entry, exit and path in the terminal.

    Each cell draws only its north and west walls, so shared walls are
    drawn once. The last column adds its east wall and the last row its
    south wall.

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (x, y), drawn as "E".
        exit_cell: Exit coordinates (x, y), drawn as "X".
        path: Cells of the path, drawn with a coloured background;
            an empty set hides it.
    """
    if path:
        on_path = path | {entry}
    else:
        on_path = set()

    for y, row in enumerate(maze):
        top = ""
        # CAMBIO 2: enumerate() para saber la columna (x) de cada celda.
        for x, cell in enumerate(row):
            if cell & NORTH:
                top += "+---"
            elif (x, y) in on_path and (x, y - 1) in on_path:
                top += "+" + PATH_COLOR + "   " + RESET
            else:
                top += "+   "
        print(top + "+")

        middle = ""
        for x, cell in enumerate(row):
            if (x, y) == entry:
                label = " E "
            elif (x, y) == exit_cell:
                label = " X "
            else:
                label = "   "
            if (x, y) in on_path:
                inside = PATH_COLOR + label + RESET
            else:
                inside = label

            if cell & WEST:
                middle += "|" + inside
            elif (x, y) in on_path and (x - 1, y) in on_path:
                middle += PATH_COLOR + " " + RESET + inside
            else:
                middle += " " + inside
        if row[-1] & EAST:
            middle += "|"
        else:
            middle += " "
        print(middle)

    bottom = ""
    for cell in maze[-1]:
        if cell & SOUTH:
            bottom += "+---"
        else:
            bottom += "+   "
    print(bottom + "+")


if __name__ == "__main__":
    test_maze = [[9, 5, 3], [12, 5, 6]]
    test_path = path_cells((0, 0), "EES")
    draw_maze(test_maze, (0, 0), (2, 1), test_path)
    print()
    draw_maze(test_maze, (0, 0), (2, 1), set())
