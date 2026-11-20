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
    """
    Generates a maze as a grid of cells, each one a bitmask of closed walls.

    Uses a randomized depth-first search; in Pac-Man mode (perfect=False)
    it then adds loops and removes dead ends without creating 3x3 open areas.
    """

    def __init__(
            self,
            height: int,
            width: int,
            perfect: bool,
            seed: int | None = None
    ):
        """
        Creates a grid of the given size with all the walls closed.

        Args:
            height (int): Number of rows.
            width (int): Number of columns.
            perfect (bool): True for a perfect maze, False for Pac-Man mode.
            seed (int | None): Random seed; None gives a random maze.
        """
        self.height: int = height
        self.width: int = width
        self.perfect: bool = perfect
        self.rng = random.Random(seed)
        self.maze: list[list[int]] = [
            [ALL_WALLS for _ in range(width)]
            for _ in range(height)
        ]
        self.pattern: set[tuple[int, int]] = (
            pattern_cells(height, width) or set()
        )

    def generate(self) -> list[list[int]]:
        """
        Generates a maze using a randomized depth-first search algorithm.

        The algorithm explores the maze starting from the top-left cell (0, 0),
        using a stack to perform depth-first traversal. At each step, it
        randomly selects an unvisited neighbouring cell and removes the wall
        between them.
        Backtracking occurs when no unvisited neighbours remain.

        If the maze is not required to be perfect, additional walls are removed
        and dead ends are reduced after the initial generation.

        Returns:
            list[list[int]]: A 2D matrix representing the generated maze,
            where each cell encodes its remaining walls as a bitmask.
        """
        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]
        for row, col in self.pattern:
            visited[row][col] = True
        stack = [(0, 0)]
        visited[0][0] = True

        while stack:
            row, col = stack[-1]
            neighbours = []

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
            self.reduce_dead_ends(2)

        return self.maze

    def remove_extra_walls(
            self,
            probability: float = 0.2
    ) -> None:
        """
        Removes additional walls from the maze to create alternative paths
        and increase connectivity.

        Iterates through all cells and randomly removes walls between adjacent
        cells based on the given probability. Walls separating cells that
        belong to the predefined pattern are preserved. Additionally, walls are
        only removed if doing so does not create an excessively large open
        space.

        Args:
            probability (float): Probability of removing each eligible wall.
                Defaults to 0.2.

        Returns:
            None
        """
        for row in range(self.height):
            for col in range(self.width):

                if col < self.width - 1:
                    if (
                        self.maze[row][col] & EAST
                        and (row, col) not in self.pattern
                        and (row, col + 1) not in self.pattern
                        and self.rng.random() < probability
                        and not self.creates_large_open_space(row, col, EAST)
                    ):
                        self.maze[row][col] &= ~EAST
                        self.maze[row][col + 1] &= ~WEST

                if row < self.height - 1:
                    if (
                        self.maze[row][col] & SOUTH
                        and (row, col) not in self.pattern
                        and (row + 1, col) not in self.pattern
                        and self.rng.random() < probability
                        and not self.creates_large_open_space(row, col, SOUTH)
                    ):
                        self.maze[row][col] &= ~SOUTH
                        self.maze[row + 1][col] &= ~NORTH

    def creates_large_open_space(
        self,
        row: int,
        col: int,
        direction: int
    ) -> bool:
        """
        Checks whether removing a wall between two adjacent cells creates
        a fully open 3x3 area anywhere in the maze.

        Creates a temporary copy of the maze and removes the specified wall
        without modifying the original maze. It then checks all possible 3x3
        blocks to determine whether any of them becomes completely open,
        with no remaining internal walls.

        Args:
            row (int): Row index of the cell containing the wall.
            col (int): Column index of the cell containing the wall.
            direction (int): Direction of the wall to be removed.

        Returns:
            bool: True if a fully open 3x3 area is found, False otherwise.
        """
        temp = [line[:] for line in self.maze]

        dir_row, dir_col = DIRECTIONS[direction]
        new_row = row + dir_row
        new_col = col + dir_col

        temp[row][col] &= ~direction
        temp[new_row][new_col] &= ~OPPOSITE[direction]

        for r in range(self.height - 2):
            for c in range(self.width - 2):

                open_space = True

                for dr in range(3):
                    for dc in range(3):
                        current = temp[r + dr][c + dc]

                        if dc < 2 and current & EAST:
                            open_space = False

                        if dr < 2 and current & SOUTH:
                            open_space = False

                if open_space:
                    return True

        return False

    def count_dead_ends(self) -> int:
        """
        Counts the number of dead ends in the maze, excluding cells belonging
        to the predefined pattern.

        Iterates through all cells and counts those with exactly one open
        passage, identifying them as dead ends.

        Returns:
            int: Total number of dead ends in the maze.
        """
        dead_ends = 0

        for row in range(self.height):
            for col in range(self.width):

                if (row, col) in self.pattern:
                    continue

                walls = self.maze[row][col]
                exits = 4 - bin(walls).count("1")

                if exits == 1:
                    dead_ends += 1

        return dead_ends

    def reduce_dead_ends(self, max_dead_ends: int = 2) -> None:
        """
        Reduces the number of dead ends in the maze by removing selected walls
        adjacent to dead-end cells, creating alternative passages.

        The method repeatedly searches for dead-end cells that do not belong to
        the predefined pattern and identifies adjacent cells separated by a
        wall.
        Candidates are randomly shuffled, and the first wall whose removal does
        not create an excessively large open space is removed. Both cells are
        updated to maintain wall consistency between neighbouring cells.

        The process continues until the number of dead ends is less than or
        equal to the specified maximum, or no valid wall removals are possible.

        Args:
            max_dead_ends (int): Maximum number of dead ends allowed in the
                maze. Defaults to 2.

        Returns:
            None
        """
        while self.count_dead_ends() > max_dead_ends:

            candidates = []

            for row in range(self.height):
                for col in range(self.width):

                    if (row, col) in self.pattern:
                        continue

                    walls = self.maze[row][col]
                    exits = 4 - bin(walls).count("1")

                    if exits == 1:
                        for direction, (
                            row_offset,
                            col_offset
                        ) in DIRECTIONS.items():
                            neighbour_row = row + row_offset
                            neighbour_col = col + col_offset

                            if (
                                0 <= neighbour_row < self.height
                                and 0 <= neighbour_col < self.width
                                and self.maze[row][col] & direction
                                and (neighbour_row, neighbour_col) not in
                                self.pattern
                            ):
                                candidates.append(
                                    (
                                        row,
                                        col,
                                        direction,
                                        neighbour_row,
                                        neighbour_col
                                    )
                                )

            self.rng.shuffle(candidates)
            for (
                row,
                col,
                direction,
                neighbour_row,
                neighbour_col
            ) in candidates:
                if not self.creates_large_open_space(row, col, direction):
                    self.maze[row][col] &= ~direction
                    self.maze[neighbour_row][neighbour_col] &= (
                        ~OPPOSITE[direction]
                    )
                    break
            else:
                break
