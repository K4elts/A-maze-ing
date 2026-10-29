'''WRITES THE MAZE TO THE OUTPUT FILE'''


def write_maze(
    path: str,
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    solution: str,
) -> None:
    """Write the maze, its entry, exit and shortest path to a file.

    Args:
        path: Name of the output file.
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (x, y).
        exit_cell: Exit coordinates (x, y).
        solution: Shortest path from entry to exit, e.g. "EESN".
    """
    with open(path, "w", encoding="utf-8") as file:
        for row in maze:
            file.write("".join([format(cell, "X") for cell in row]) + "\n")
        file.write("\n")
        file.write(f"{entry[0]},{entry[1]}\n")
        file.write(f"{exit_cell[0]},{exit_cell[1]}\n")
        file.write(solution + "\n")
