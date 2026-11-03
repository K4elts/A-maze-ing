from display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator

maze = MazeGenerator(height=20, width=10).generate()
print(len(maze), "rows x", len(maze[0]), "columns")
draw_maze(maze, (0, 0), (len(maze[0]) - 1, len(maze) - 1), set(), WALL_COLORS[0])
