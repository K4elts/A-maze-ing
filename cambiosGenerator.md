class MazeGenerator:
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        # CAMBIO 1: antes range(height) dentro y range(width) fuera.
        # Ahora la lista de fuera son las FILAS (height) y cada fila
        # tiene tantas celdas como columnas (width).
        self.maze: list[list[int]] = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> list[list[int]]:
        # marca todas las celdas como falso
        # CAMBIO 2: igual que la cuadricula, visited tambien por filas.
        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        stack = [(0, 0)]
        visited[0][0] = True

        while stack:
            # CAMBIO 3: antes "col, row". La pila guarda (fila, columna).
            row, col = stack[-1]
            neighbours = []
            # comprueba que las celdas vecinas buscadas estan disponibles
            # CAMBIO 4: antes "(dir_col, dir_row)". DIRECTIONS esta en
            # (fila, columna): NORTH = (-1, 0) es subir una fila.
            for direction, (dir_row, dir_col) in DIRECTIONS.items():
                # CAMBIO 5: antes "new_col, new_row = col + dir_col, ...".
                new_row, new_col = row + dir_row, col + dir_col
                # CAMBIO 6: la fila se compara con height y la columna
                # con width; y visited se lee [fila][columna].
                if (
                    0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and not visited[new_row][new_col]
                ):
                    # CAMBIO 7: antes (direction, new_col, new_row).
                    neighbours.append((direction, new_row, new_col))
            if neighbours:
                # CAMBIO 8: a partir de aqui, todo en orden [fila][columna].
                direction, new_row, new_col = random.choice(neighbours)
                self.maze[row][col] &= ~direction
                self.maze[new_row][new_col] &= ~OPPOSITE[direction]
                visited[new_row][new_col] = True
                stack.append((new_row, new_col))
            else:
                stack.pop()
        return self.maze
