'''DRAWS THE MAZE IN THE TERMINAL'''

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8


def draw_maze(maze: list[list[int]]) -> None:
    """Draw the maze walls in the terminal with ASCII characters.

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
    """
    for row in maze:
        top = ""
        for cell in row:
            if cell & NORTH:
                top += "+---"
            else:
                top += "+   "
        print(top + "+")

        middle = ""
        for cell in row:
            if cell & WEST:
                middle += "|   "
            else:
                middle += "    "
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
    draw_maze(test_maze)
