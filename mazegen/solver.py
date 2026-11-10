'''SOLVES THE MAZE WITH THE SHORTEST PATH'''
from .generator import DIRECTIONS, MazeGenerator


def solve_bfs(
    generator: MazeGenerator,
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] | None = None
) -> list[tuple[int, int]] | None:
    """Find the shortest path between two cells with a breadth-first search.

    BFS visits the cells in layers (first those 1 step away, then 2...),
    so the first time it reaches the end it has found a shortest path.

    Args:
        generator: The maze generator, after calling generate().
        start: Start cell (row, col). Defaults to the top-left corner.
        end: End cell (row, col). Defaults to the bottom-right corner.

    Returns:
        The list of (row, col) cells from start to end, both included,
        or None if the end cannot be reached.
    """
    if end is None:
        end = (generator.height - 1, generator.width - 1)

    queue = [start]
    index = 0

    visited = {start}
    parent: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    while index < len(queue):
        row, col = queue[index]
        index += 1

        # ¿Hemos llegado a la salida?
        if (row, col) == end:
            path: list[tuple[int, int]] = []
            current: tuple[int, int] | None = end

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        # Explorar las celdas vecinas
        for direction, (dir_row, dir_col) in DIRECTIONS.items():
            new_row = row + dir_row
            new_col = col + dir_col
            neighbour = (new_row, new_col)

            # Comprobar límites
            valid_row = 0 <= new_row < generator.height
            valid_col = 0 <= new_col < generator.width

            if not (valid_row and valid_col):
                continue

            # No atravesar paredes
            if generator.maze[row][col] & direction:
                continue

            # No visitar celdas repetidas
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = (row, col)
            queue.append(neighbour)

    return None
