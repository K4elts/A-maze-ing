import random
import sys

from pydantic import ValidationError

from config_parser import MazeParameters, read_config
from display import run_menu
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_bfs
from output_writer import path_to_directions, write_maze

if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py <config_file>")
    sys.exit(1)

config_path = sys.argv[1]

try:
    params = MazeParameters.model_validate(read_config(config_path))
except OSError as error:
    print(f"Error: cannot read '{config_path}': {error.strerror}")
    sys.exit(1)
except ValidationError as error:
    print("Error: invalid configuration")
    print(error)
    sys.exit(1)
except ValueError as error:
    print(f"Error: {error}")
    sys.exit(1)

if params.SEED is not None:
    random.seed(params.SEED)

entry = (params.ENTRY[1], params.ENTRY[0])
exit_cell = (params.EXIT[1], params.EXIT[0])

generator = MazeGenerator(height=params.HEIGHT, width=params.WIDTH)
maze = generator.generate()

cells = solve_bfs(generator, entry, exit_cell)
if cells is None:
    print("Error: no path from the entry to the exit")
    sys.exit(1)
solution = path_to_directions(cells)

try:
    write_maze(params.OUTPUT_FILE, maze, entry, exit_cell, solution)
except OSError as error:
    print(f"Error: cannot write '{params.OUTPUT_FILE}': {error.strerror}")
    sys.exit(1)

run_menu(maze, entry, exit_cell, solution)