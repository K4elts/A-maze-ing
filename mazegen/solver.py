'''SOLVES THE MAZE WITH THE SHORTEST PATH'''
from .generator import DIRECTIONS


def solve_dfs(
    self,
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] | None = None
) -> list[tuple[int, int]] | None:

    if end is None:
        end = (self.height - 1, self.width - 1)

    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        row, col = stack.pop()

        # ¿Hemos llegado a la salida?
        if (row, col) == end:
            path = []
            current = end

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
            valid_row = 0 <= new_row < self.height
            valid_col = 0 <= new_col < self.width

            if not (valid_row and valid_col):
                continue

            # No atravesar paredes ni visitar celdas repetidas
            if self.maze[row][col] & direction:
                continue

            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = (row, col)
            stack.append(neighbour)

    return None


def solve_bfs(
    self,
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] | None = None
) -> list[tuple[int, int]] | None:

    if end is None:
        end = (self.height - 1, self.width - 1)

    queue = [start]
    index = 0

    visited = {start}
    parent = {start: None}

    while index < len(queue):
        row, col = queue[index]
        index += 1

        # ¿Hemos llegado a la salida?
        if (row, col) == end:
            path = []
            current = end

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
            valid_row = 0 <= new_row < self.height
            valid_col = 0 <= new_col < self.width

            if not (valid_row and valid_col):
                continue

            # No atravesar paredes
            if self.maze[row][col] & direction:
                continue

            # No visitar celdas repetidas
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = (row, col)
            queue.append(neighbour)

    return None
