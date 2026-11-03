'''SOLVES THE MAZE WITH THE SHORTEST PATH'''
from generator import DIRECTIONS


def solve_dfs(
    self,
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] | None = None
) -> list[tuple[int, int]] | None:

    if end is None:
        end = (self.width - 1, self.height - 1)

    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        col, row = stack.pop()

        # ¿Hemos llegado a la salida?
        if (col, row) == end:
            path = []
            current = end

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        # Explorar las celdas vecinas
        for direction, (dir_col, dir_row) in DIRECTIONS.items():
            new_col = col + dir_col
            new_row = row + dir_row
            neighbour = (new_col, new_row)

            # Comprobar límites
            valid_col = 0 <= new_col < self.width
            valid_row = 0 <= new_row < self.height
            if not (valid_col and valid_row):
                continue

            # No atravesar paredes ni visitar celdas repetidas
            if self.maze[col][row] & direction:
                continue

            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = (col, row)
            stack.append(neighbour)

    return None


def solve_bfs(
    self,
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] | None = None
) -> list[tuple[int, int]] | None:

    if end is None:
        end = (self.width - 1, self.height - 1)

    queue = [start]
    index = 0

    visited = {start}
    parent = {start: None}

    while index < len(queue):
        col, row = queue[index]
        index += 1

        # ¿Hemos llegado a la salida?
        if (col, row) == end:
            path = []
            current = end

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        # Explorar las celdas vecinas
        for direction, (dir_col, dir_row) in DIRECTIONS.items():
            new_col = col + dir_col
            new_row = row + dir_row
            neighbour = (new_col, new_row)

            # Comprobar límites
            valid_col = 0 <= new_col < self.width
            valid_row = 0 <= new_row < self.height

            if not (valid_col and valid_row):
                continue

            # No atravesar paredes
            if self.maze[col][row] & direction:
                continue

            # No visitar celdas repetidas
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = (col, row)
            queue.append(neighbour)

    return None
