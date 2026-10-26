'''GENERATES THE MAZE WITH MazeGenerator'''
import random

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
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.maze: list[list[int]] = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> list[list[int]]:
        # marca todas las celdas como falso
        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        stack = [(0, 0)]
        visited[0][0] = True

        while stack:
            row, col = stack[-1]
            neighbours = []
            # comprueba que las celdas vecinas buscadas estan disponibles
            for direction, (dir_row, dir_col) in DIRECTIONS.items():
                new_row, new_col = row + dir_row, col + dir_col
                if (
                    0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and not visited[new_row][new_col]
                ):
                    neighbours.append((direction, new_row, new_col))
            if neighbours:
                direction, new_row, new_col = random.choice(neighbours)
                self.maze[row][col] &= ~direction
                self.maze[new_row][new_col] &= ~OPPOSITE[direction]
                visited[new_row][new_col] = True
                stack.append((new_row, new_col))
            else:
                stack.pop()
        return self.maze


# ---------------- CHECK -----------------------
def print_maze(maze: list[list[int]]) -> None:
    height = len(maze)
    width = len(maze[0])

    for row in range(height):
        # Paredes superiores de las celdas
        top = ""
        for col in range(width):
            top += "+"
            top += "---" if maze[row][col] & NORTH else "   "
        top += "+"
        print(top)

        # Paredes laterales y contenido de las celdas
        middle = ""
        for col in range(width):
            middle += "|" if maze[row][col] & WEST else " "
            middle += "   "
        middle += "|" if maze[row][width - 1] & EAST else " "
        print(middle)

    # Paredes inferiores de la última fila
    bottom = ""
    for col in range(width):
        bottom += "+"
        bottom += "---" if maze[height - 1][col] & SOUTH else "   "
    bottom += "+"
    print(bottom)


if __name__ == "__main__":
    maze = MazeGenerator(15, 15)
    result = maze.generate()
#    for row in result:
#        print(" ".join(f"{num:2}" for num in row))
    print_maze(result)
