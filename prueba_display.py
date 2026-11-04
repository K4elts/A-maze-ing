from display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_dfs


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
        path (list[tuple[int, int]]): List of (x, y) coordinates representing
            the solution path through the maze.

    Returns:
        str: A string containing the movement directions (N, E, S, W)
            required to follow the path. Returns an empty string if the
            path contains fewer than two coordinates.

    Example:
        >>> path_to_directions([(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)])
        'EESS'
    """
    directions = {
        (0, -1): "N",
        (1, 0): "E",
        (0, 1): "S",
        (-1, 0): "W"
    }

    moves = ""

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        dx = x2 - x1
        dy = y2 - y1

        moves += directions[(dx, dy)]

    return moves


#maze = MazeGenerator(height=20, width=10).generate()
maze = MazeGenerator(height=10, width=20)
result = maze.generate()
print(len(result[0]), "rows x", len(result), "columns")
start = (0, 0)
end = (maze.width - 1, maze.height - 1)
draw_maze(result, start, end, set(), WALL_COLORS[0])
print()
path = solve_dfs(maze, start, end)
print(f"Path: {path}")
movements = path_to_directions(path)
print(f"Movements: {movements}")
print(f"Number of Movements: {len(movements)}")
draw_maze(result, start, end, set(path or []), WALL_COLORS[0])
