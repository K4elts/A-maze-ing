import sys

from config_parser import MazeParameters, load_config
from mazegen import MazeGenerator, pattern_cells, solve_bfs
from display import run_menu
from output_writer import path_to_directions, write_maze


def build_maze(
    params: MazeParameters,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    seed: int | None,
) -> tuple[list[list[int]], str]:
    """
    Generates a maze, finds the shortest path between the entry and
    exit using Breadth-First Search (BFS), and saves the result
    to the configured output file.

    The maze is generated according to the provided configuration
    parameters and random seed. Once generated, the shortest path
    is calculated and converted into a sequence of direction letters.

    Args:
        params (MazeParameters): Validated configuration containing
            the maze dimensions, generation type and output file path.
        entry (tuple[int, int]): Starting coordinates (row, col).
        exit_cell (tuple[int, int]): Destination coordinates (row, col).
        seed (int | None): Random seed used for maze generation.
            If None, a random seed is used.

    Returns:
        tuple[list[list[int]], str]: A tuple containing the generated
            maze as a list of rows and its shortest path represented
            as a sequence of direction letters.

    Raises:
        RuntimeError: If no valid path exists between the entry
            and exit.
        OSError: If the generated maze cannot be written
            to the output file.
    """
    generator = MazeGenerator(
        height=params.HEIGHT,
        width=params.WIDTH,
        perfect=params.PERFECT,
        seed=seed
    )
    maze = generator.generate()

    cells = solve_bfs(generator, entry, exit_cell)
    if cells is None:
        raise RuntimeError("No path from the entry to the exit")
    solution = path_to_directions(cells)

    write_maze(params.OUTPUT_FILE, maze, entry, exit_cell, solution)
    return maze, solution


regenerations = 0


def regenerate() -> tuple[list[list[int]], str]:
    """
    Generates the next maze using the same configuration parameters
    as the initial maze.

    With a SEED in the config file, each new maze uses the next seed
    (SEED + 1, SEED + 2...), so the same SEED always gives the same
    sequence of mazes, and every maze of the sequence is different.
    Without SEED, every maze is randomly generated. The new maze is
    also solved and saved to the configured output file.

    Returns:
        tuple[list[list[int]], str]: A tuple containing the newly
            generated maze as a list of rows and its shortest path
            represented as a sequence of direction letters.

    Raises:
        RuntimeError: If no valid path exists between the entry
            and exit.
        OSError: If the generated maze cannot be written
            to the output file.
    """
    global regenerations
    regenerations += 1
    if params.SEED is None:
        seed = None
    else:
        seed = params.SEED + regenerations
    return build_maze(params, entry, exit_cell, seed)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py <config_file>")
            print("or")
            print("Usage: make run")
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

        entry = (params.ENTRY[1], params.ENTRY[0])
        exit_cell = (params.EXIT[1], params.EXIT[0])

        try:
            maze, solution = build_maze(params, entry, exit_cell, params.SEED)
        except OSError as error:
            print(
                f"Error: cannot write '{params.OUTPUT_FILE}': {error.strerror}"
                )
            sys.exit(1)
        except RuntimeError as error:
            print(f"Error: {error}")
            sys.exit(1)

        notice = ""
        if pattern_cells(params.HEIGHT, params.WIDTH) is None:
            notice = "Note: the maze is too small to draw the 42 pattern."

        run_menu(
            maze,
            entry,
            exit_cell,
            solution,
            regenerate,
            params.PERFECT,
            notice
        )
    except (KeyboardInterrupt, EOFError):
        print()
        print("Stopped by the user")
