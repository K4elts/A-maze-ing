'''GENERATES THE MAZE WITH MazeGenerator'''
import random

from .pattern import pattern_cells

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

ALL_WALLS: int = NORTH | EAST | SOUTH | WEST

DIRECTIONS = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}

OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST
}


class MazeGenerator:
    def __init__(
            self,
            height: int,
            width: int,
            perfect: bool,
            seed: int | None = None
    ):
        self.height: int = height
        self.width: int = width
        self.perfect: bool = perfect
        self.rng = random.Random(seed)
        self.maze: list[list[int]] = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]
        # celdas del 42 (vacío si el laberinto es demasiado pequeño)
        self.pattern: set[tuple[int, int]] = (
            pattern_cells(height, width) or set()
        )

    def generate(self) -> list[list[int]]:
        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        # el 42 cuenta como visitado: el DFS no entra y queda cerrado
        for row, col in self.pattern:
            visited[row][col] = True
        stack = [(0, 0)]
        visited[0][0] = True

        while stack:
            row, col = stack[-1]
            neighbours = []
            # comprueba que las celdas vecinas buscadas estan disponibles
            for direction, (dir_row, dir_col) in DIRECTIONS.items():
                new_row = row + dir_row
                new_col = col + dir_col
                if (
                    0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and not visited[new_row][new_col]
                ):
                    neighbours.append((direction, new_row, new_col))

            if neighbours:
                direction, new_row, new_col = self.rng.choice(neighbours)
                self.maze[row][col] &= ~direction
                self.maze[new_row][new_col] &= ~OPPOSITE[direction]
                visited[new_row][new_col] = True
                stack.append((new_row, new_col))
            else:
                stack.pop()

        if not self.perfect:
            self.remove_extra_walls()

        return self.maze

    def remove_extra_walls(self, probability: float = 0.2) -> None:
        for row in range(self.height):
            for col in range(self.width):
                # Comprobar la pared este
                if col < self.width - 1:
                    if (
                        self.maze[row][col] & EAST
                        and (row, col) not in self.pattern
                        and (row, col + 1) not in self.pattern
                        and self.rng.random() < probability
                    ):
                        self.maze[row][col] &= ~EAST
                        self.maze[row][col + 1] &= ~WEST

                # Comprobar la pared sur
                if row < self.height - 1:
                    if (
                        self.maze[row][col] & SOUTH
                        and (row, col) not in self.pattern
                        and (row + 1, col) not in self.pattern
                        and self.rng.random() < probability
                    ):
                        self.maze[row][col] &= ~SOUTH
                        self.maze[row + 1][col] &= ~NORTH
