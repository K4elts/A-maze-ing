from display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_dfs

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
draw_maze(result, start, end, set(path or []), WALL_COLORS[0])
