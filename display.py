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

    Args:
        maze: The maze as a list of rows; each cell is a number from 0 to 15.
        entry: Entry coordinates (x, y), drawn as "E".
        exit_cell: Exit coordinates (x, y), drawn as "X".
    """
    # CAMBIO 1: enumerate() da el numero de fila (y) ademas de la fila.
    for y, row in enumerate(maze):
        top = ""
        for cell in row:
            if cell & NORTH:
                top += "+---"
            else:
                top += "+   "
        print(top + "+")

        middle = ""
        # CAMBIO 2: enumerate() da el numero de columna (x) de cada celda.
        for x, cell in enumerate(row):
            # CAMBIO 3: elegir que va DENTRO de la celda.
            if (x, y) == entry:
                inside = " E "
            elif (x, y) == exit_cell:
                inside = " X "
            else:
                inside = "   "
            # CAMBIO 4: la pared Oeste (o un espacio) + lo de dentro.
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
    # CAMBIO 5: ahora hay que pasarle tambien la entrada y la salida.
    draw_maze(test_maze, (0, 0), (2, 1))
