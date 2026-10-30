'''DRAWS THE MAZE IN THE TERMINAL'''

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


def draw_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
) -> None:
    """Draw the maze walls, entry and exit in the terminal.

    Each cell draws only its north and west walls, so shared walls are
    drawn once. The last column adds its east wall and the last row its
    south wall.

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (x, y), drawn as "E".
        exit_cell: Exit coordinates (x, y), drawn as "X".
    """
    for y, row in enumerate(maze):
        top = ""
        for cell in row:
            if cell & NORTH:
                top += "+---"
            else:
                top += "+   "
        print(top + "+")

        middle = ""
        for x, cell in enumerate(row):
            if (x, y) == entry:
                inside = " E "
            elif (x, y) == exit_cell:
                inside = " X "
            else:
                inside = "   "
            if cell & WEST:
                middle += "|" + inside
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
    draw_maze(test_maze, (0, 0), (2, 1))
