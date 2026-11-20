*This project has been created as part of the 42 curriculum by aliao-tr, plopez-l.*

# A-Maze-ing

## Description

**A-Maze-ing** is a maze generator written in Python 3.10+. The program reads a configuration file, generates a random but reproducible maze, computes the shortest path between the entry and the exit, saves the result to a text file and displays it in the terminal with an interactive menu.

The project supports two generation modes:

- **`PERFECT=True`**: a perfect maze, meaning there is exactly one path between the entry and the exit and no loops (equivalent to a spanning tree).
- **`PERFECT=False`** (default mode): a playable Pac-Man-like board, with all corridors connected, open corners and centre, at least two independent routes and few dead ends.

In addition, the maze contains the "42" pattern drawn with fully closed cells whenever the size allows it; if it does not fit, a message is printed to the console. The generation logic lives in a reusable package (`mazegen`) that can be installed with `pip` in future projects.

## Instructions

### Requirements

- Python 3.10 or newer.
- Development tools: `flake8`, `mypy` and `build` (installed automatically by `make install`).
- Working inside a virtual environment is recommended (`make install` creates `.venv`).

### Installation

```bash
make install
```

This command creates `.venv`, upgrades `pip` and installs the dependencies from `requirements.txt`.

To install the already generated reusable package in another environment:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Usage

With the configuration file included in the repository (`config.txt`):

```bash
python3 a_maze_ing.py config.txt
```

Or, using the project's virtual environment:

```bash
make run
```

You can also pass any other valid configuration file as the only argument. The program validates the configuration and prints clear error messages if the file is missing, a mandatory key is absent, a line does not follow the `KEY=VALUE` format, numbers are invalid, coordinates are outside the maze or the parameters are inconsistent. It never terminates unexpectedly because of invalid input.

### Interactive menu

Once the maze has been generated and displayed, the terminal menu offers:

1. Regenerate a new maze (the sequence is reproducible if `SEED` is configured).
2. Show/hide the shortest path from the entry to the exit.
3. Rotate the wall colours.
4. Rotate the path colour (extra interaction).
5. Quit.

The ASCII representation distinguishes the entry (`E`, white), the exit (`X`, red), the cells of the "42" pattern (yellow blocks), the walls and, when enabled, the highlighted solution path.

### Code quality and packaging

```bash
make lint          # flake8 + mypy with the required options
make lint-strict   # flake8 + mypy --strict
make clean         # removes caches and temporary artefacts
make debug         # runs a_maze_ing.py with pdb
make build         # rebuilds mazegen-1.0.0-py3-none-any.whl
```

The repository includes `.gitignore`, `LICENSE.md` (MIT licence, which explicitly allows reuse and distribution) and all the sources needed to rebuild the package with `python -m build` from a clean environment.

## Configuration file

The configuration file is plain text. Every non-empty line follows the `KEY=VALUE` format; lines starting with `#` are comments. Keys are case-insensitive, cannot be repeated and unknown keys are not allowed.

Example configuration file included (`config.txt`):

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
#SEED=42
```

| Key | Type | Required | Description | Constraints |
|---|---|---|---|---|
| `WIDTH` | integer | yes | Maze width in cells (columns). | `1 <= WIDTH <= 70` |
| `HEIGHT` | integer | yes | Maze height in cells (rows). | `1 <= HEIGHT <= 70` |
| `ENTRY` | `x,y` | yes | Entry coordinates, column first and row second. | Inside the maze; different from `EXIT`; cannot overlap the "42" pattern. |
| `EXIT` | `x,y` | yes | Exit coordinates, column first and row second. | Inside the maze; different from `ENTRY`; cannot overlap the "42" pattern. |
| `OUTPUT_FILE` | string | yes | Name of the output file. | Must end in `.txt`; cannot be `config.txt`. |
| `PERFECT` | boolean | yes | `True` generates a perfect maze; `False` generates a Pac-Man-like board. | Valid boolean values (`True`/`False`). |
| `SEED` | integer | no | Seed used to reproduce exactly the same maze. | If omitted, each run is random. |

Notes on coordinates: the configuration uses `(x, y)` (column, row), while internally and in the `mazegen` package `(row, col)` (row, column) is used. The conversion is done in `a_maze_ing.py`.

## Output file

The file specified by `OUTPUT_FILE` contains:

1. `HEIGHT` lines, each with exactly `WIDTH` hexadecimal digits (one per cell).
2. An empty line.
3. The entry coordinates in `x,y` format.
4. The exit coordinates in `x,y` format.
5. The shortest path as a sequence of the letters `N`, `E`, `S`, `W`.

All lines end with `\n`. Each hexadecimal digit encodes which walls are **closed**:

| Bit | Value | Direction |
|---|---|---|
| 0 (LSB) | `1` | North |
| 1 | `2` | East |
| 2 | `4` | South |
| 3 | `8` | West |

For example, `3` (`0011`) means North and East are closed while South and West are open, and `A` (`1010`) has East and West closed. Shared walls are encoded consistently by both neighbouring cells and the outer border remains closed.

The `maze_analyzer.py` script included with the subject can be used to check the resulting file:

```bash
python3 maze_analyzer.py maze.txt
```

## Generation algorithm

The algorithm used is **randomized Depth-First Search (DFS)**, also known as *recursive backtracker*, implemented iteratively with an explicit stack:

1. Every cell starts with all four walls closed (`15` / `F`).
2. The cells of the "42" pattern are marked as already visited and left closed.
3. Starting from `(0, 0)`, an unvisited neighbour is chosen at random, the shared wall is removed and the traversal moves forward; if there are no neighbours, it backtracks through the stack.
4. With `PERFECT=True` the process ends here: a spanning tree is obtained, so all accessible cells are connected and there are no loops.
5. With `PERFECT=False`, extra walls are removed with probability `0.2` to create loops, and dead ends are then reduced to a maximum of 2. Before opening each wall, the generator checks that no fully open `3x3` area appears.

**Why this algorithm?**

- By construction it guarantees full connectivity and, in perfect mode, the absence of loops.
- It is simple to implement, efficient (each cell is visited once) and easy to explain and defend.
- It uses its own `random.Random(seed)`, so the same seed reproduces exactly the same maze without depending on the global state of `random`.
- The initial tree is a clean base on which to add controlled loops for Pac-Man mode while keeping the corridor-size and "42" pattern constraints.

The shortest path is computed separately with **BFS** (`solve_bfs`), which visits cells layer by layer and therefore returns the first route found to the exit with the minimum number of steps.

## Reusable module (`mazegen`)

The reusable logic is isolated in the `mazegen` package, made up of:

- `mazegen/generator.py`: the `MazeGenerator` class and wall constants.
- `mazegen/solver.py`: the `solve_bfs` function.
- `mazegen/pattern.py`: the `pattern_cells` function.
- `mazegen/__init__.py`: exports the public API.
- `mazegen/README.md`: short documentation for the package.

Basic usage example:

```python
from mazegen import MazeGenerator, solve_bfs

generator = MazeGenerator(height=15, width=20, perfect=True, seed=42)
maze = generator.generate()          # maze[row][col], value 0..15
path = solve_bfs(generator, (0, 0), (14, 19))  # list of (row, col) or None
print(maze[0][0], path)
```

Custom parameters:

- `height` and `width`: grid dimensions.
- `perfect`: `True` for a perfect maze, `False` for Pac-Man mode.
- `seed`: optional integer; the same value always produces the same maze. If it is `None`, generation is random.

Access to the structure and the solution:

- `generator.maze` (or the value returned by `generate()`) is a `maze[row][col]` matrix; each value is a bitmask of closed walls (for example, `15` is a fully closed cell).
- `solve_bfs(generator, start, end)` returns the list of `(row, col)` cells of the shortest path, including both endpoints, or `None` if no route exists.
- `pattern_cells(height, width)` returns the cells occupied by the "42" pattern, or `None` if the maze is too small.

All coordinates in this package use `(row, col)`. The output file format is different: it uses one hexadecimal digit per cell per line and `(x, y)` coordinates, and is produced in `output_writer.py`.

To rebuild and install the package:

```bash
make build
pip install mazegen-1.0.0-py3-none-any.whl
```

The MIT licence in `LICENSE.md` allows this generator to be reused, modified and distributed in later projects.

## Resources

Classic references and documentation consulted on the topic:

- [Maze generation algorithms (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm): overview of DFS, Prim, Kruskal, etc.
- [Depth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Depth-first_search): basis of the *recursive backtracker* used here.
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search): justification for computing the shortest path.
- [Random — Python documentation](https://docs.python.org/3/library/random.html): use of an isolated `random.Random` for seed-based reproducibility.
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/): docstring style for functions and classes.
- [typing / mypy](https://mypy.readthedocs.io/) and [flake8](https://flake8.pycqa.org/): type annotations and style checking.
- [Pydantic](https://docs.pydantic.dev/): declarative validation of the configuration file.
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) and [setuptools](https://setuptools.pypa.io/): building the `mazegen` package.
- `maze_analyzer.py` (included with the subject): verification of wall consistency, perfect/Pac-Man mode and dead ends.

**AI usage:** AI was used as support for drafting and structuring documentation (including this README), reviewing docstrings, suggesting style and type checks, and clarifying packaging and algorithm concepts. All generated or suggested code was read, tested and understood by the team, and design decisions were reviewed by both members before being included. Understanding of the generator's logic and the defensibility of the project was never delegated to AI.

## Team and project management

**Team:** aliao-tr and plopez-l.

### Roles

- **aliao-tr**: design and implementation of the generator (`mazegen/generator.py`, `pattern.py`, `solver.py`) and of the seed-based reproducibility logic.
- **plopez-l**: configuration parsing and validation (`config_parser.py`), output file writing (`output_writer.py`), display and menu (`display.py`) and packaging (`pyproject.toml`, `Makefile`).
- **Both**: integration in `a_maze_ing.py`, manual testing with `maze_analyzer.py`, review of `flake8`/`mypy`, documentation and defense preparation.

### Planning

The initial plan was to build a minimal perfect generator first and then add the configuration layer, hexadecimal output and display. During development the scope grew to include strict validation with Pydantic, an optional seed, control of fully open `3x3` areas, dead-end reduction, a menu with wall and path colours, and packaging as a wheel. The "42" pattern was integrated from the start as closed cells that the DFS treats as already visited.

### What worked well and what could be improved

- Worked well: separating generation from the rest of the program made the package reusable and allowed both modes to be tested with the analyzer; automatic style and type checks caught errors before the defense.
- Could be improved: add formal unit tests with `pytest`, simplify the `3x3` area check (it currently copies the matrix for every candidate wall) and explore the bonuses for multiple algorithms or generation animation.

### Tools

Git, virtual environments, `make`, `flake8`, `mypy`, `pydantic`, `build`, `maze_analyzer.py`, the ASCII menu with ANSI escape codes and AI assistants for documentation and review.

## License

This project is distributed under the MIT licence. See [`LICENSE.md`](LICENSE.md) for the full terms.
