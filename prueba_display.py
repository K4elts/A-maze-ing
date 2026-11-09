'''TEST: GENERATES, SOLVES AND DRAWS A MAZE'''
import sys

from display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_bfs
from output_writer import path_to_directions, write_maze


maze = MazeGenerator(height=10, width=20, perfect=True)
result = maze.generate()
print(len(result), "rows x", len(result[0]), "columns")
start = (0, 0)
end = (maze.height - 1, maze.width - 1)
draw_maze(result, start, end, set(), WALL_COLORS[0])
print(f"Result: {result}")
print()
path = solve_bfs(maze, start, end)
if path is None:
    print("No path from start to end")
    sys.exit(1)
print(f"Path: {path}")
print()
movements = path_to_directions(path)
print(f"Movements: {movements}")
print(f"Number of Movements: {len(movements)}")
draw_maze(result, start, end, set(path), WALL_COLORS[0])
write_maze("output_file.txt", result, start, end, movements)
