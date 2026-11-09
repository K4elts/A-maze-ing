'''MAIN PROGRAM: READS THE CONFIG, BUILDS THE MAZE AND SHOWS IT'''
import random
import sys

from config_parser import MazeParameters, load_config
from display import run_menu
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_bfs
from output_writer import path_to_directions, write_maze


def build_maze(
    params: MazeParameters,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
) -> tuple[list[list[int]], str]:
    """Generate a maze, solve it and write it to the output file.

    Args:
        params: The validated configuration.
        entry: Entry coordinates (row, col).
        exit_cell: Exit coordinates (row, col).

    Returns:
        The maze (a list of rows) and its shortest path as letters.

    Raises:
        RuntimeError: If there is no path from the entry to the exit.
        OSError: If the output file cannot be written.
    """
    generator = MazeGenerator(
        height=params.HEIGHT,
        width=params.WIDTH,
        perfect=params.PERFECT
    )
    maze = generator.generate()

    cells = solve_bfs(generator, entry, exit_cell)
    if cells is None:
        raise RuntimeError("no path from the entry to the exit")
    solution = path_to_directions(cells)

    write_maze(params.OUTPUT_FILE, maze, entry, exit_cell, solution)
    return maze, solution


if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py <config_file>")
    sys.exit(1)

config_path = sys.argv[1]

try:
    params = load_config(config_path)
except OSError as error:
    print(f"Error: cannot read '{config_path}': {error.strerror}")
    sys.exit(1)
except ValueError as error:
    print(f"Error: {error}")
    sys.exit(1)

if params.SEED is not None:
    random.seed(params.SEED)

entry = (params.ENTRY[1], params.ENTRY[0])
exit_cell = (params.EXIT[1], params.EXIT[0])


def regenerate() -> tuple[list[list[int]], str]:
    """Build a new maze with the same configuration."""
    return build_maze(params, entry, exit_cell)


try:
    maze, solution = regenerate()
except OSError as error:
    print(f"Error: cannot write '{params.OUTPUT_FILE}': {error.strerror}")
    sys.exit(1)
except RuntimeError as error:
    print(f"Error: {error}")
    sys.exit(1)


run_menu(maze, entry, exit_cell, solution, regenerate, params.PERFECT)
