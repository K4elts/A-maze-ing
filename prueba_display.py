from display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_dfs
import output_writer


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
        (-1, 0): "N",
        (0, 1): "E",
        (1, 0): "S",
        (0, -1): "W"
    }

    moves = ""

    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]

        diff_row = row2 - row1
        diff_col = col2 - col1

        moves += directions[(diff_row, diff_col)]

    return moves


maze = MazeGenerator(height=10, width=20)
result = maze.generate()
print(len(result), "rows x", len(result[0]), "columns")
start = (0, 0)
end = (maze.height - 1, maze.width - 1)
draw_maze(result, start, end, set(), WALL_COLORS[0])
print(f"Result: {result}")
print()
path = solve_dfs(maze, start, end)
print(f"Path: {path}")
print()
movements = path_to_directions(path)
print(f"Movements: {movements}")
print(f"Number of Movements: {len(movements)}")
draw_maze(result, start, end, set(path or []), WALL_COLORS[0])
output_writer.write_maze("output_file.txt", result, start, end, movements)
