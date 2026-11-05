'''WRITES THE MAZE TO THE OUTPUT FILE'''


def path_to_directions(path: list[tuple[int, int]]) -> str:
    """
    Converts a list of maze path coordinates into a string of movement
    directions.

    Each consecutive pair of coordinates is compared to determine the movement:
        - N: North (up)
        - E: East (right)
        - S: South (down)
        - W: West (left)

    Args:
        path (list[tuple[int, int]]): List of (row, col) coordinates
            representing the solution path through the maze.

    Returns:
        str: A string containing the movement directions (N, E, S, W)
            required to follow the path. Returns an empty string if the
            path contains fewer than two coordinates.

    Example:
        >>> path_to_directions([(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)])
        'EESS'
    """
    directions = {
        (-1, 0): "N",
        (0, 1): "E",
        (1, 0): "S",
        (0, -1): "W"
    }

    moves = ""

    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]

        diff_row = row2 - row1
        diff_col = col2 - col1

        moves += directions[(diff_row, diff_col)]

    return moves


def write_maze(
    path: str,
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    solution: str,
) -> None:
    """Write the maze, its entry, exit and shortest path to a file.

    Inside the program coordinates are (row, col), but the output file
    uses "x,y" (column first), so they are written the other way round.

    Args:
        path: Name of the output file.
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (row, col).
        exit_cell: Exit coordinates (row, col).
        solution: Shortest path from entry to exit, e.g. "EESN".
    """
    with open(path, "w", encoding="utf-8") as file:
        for row in maze:
            file.write("".join([format(cell, "X") for cell in row]) + "\n")
        file.write("\n")
        file.write(f"{entry[1]},{entry[0]}\n")
        file.write(f"{exit_cell[1]},{exit_cell[0]}\n")
        file.write(solution + "\n")
