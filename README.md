*This project has been created as part of the 42 curriculum by aliao-tr & plopez-l*

# Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, generates a random maze, finds the shortest path between the entry and
the exit, writes the result to an output file and shows it in the terminal
with an interactive menu.

Two kinds of maze can be generated:

- **Perfect** (`PERFECT=True`): there is exactly one path between any two
  cells, so there are no loops.
- **Pac-Man board** (`PERFECT=False`): some extra walls are opened after
  generation, so there are loops and several possible routes.

Every maze has its outer border closed and coherent walls between
neighbouring cells: if a cell has its East wall closed, the cell on its right
has its West wall closed too.

<!-- TODO before submission: describe the "42" pattern here once it is done. -->

# Instructions

## Requirements

- Python 3.10 or later

## Installation

```
make install
```

This creates a virtual environment in `.venv` and installs the dependencies
listed in `requirements.txt` (`pydantic`, `flake8`, `mypy` and `build`).

## Usage

```
make run
```

or, with any configuration file:

```
python3 a_maze_ing.py config.txt
```

## Interactive menu

| Option | Action |
|---|---|
| 1 | Generate a new maze with the same configuration |
| 2 | Show / hide the shortest path |
| 3 | Change the wall colour |
| 4 | Change the path colour |
| 5 | Quit |

## Other Makefile rules

| Rule | Action |
|---|---|
| `make debug` | Run the program with the `pdb` debugger |
| `make lint` | Check the code with `flake8` and `mypy` |
| `make lint-strict` | Same check, with `mypy --strict` |
| `make build` | Build the reusable `mazegen` package (`.whl`) |
| `make clean` | Remove caches and build leftovers |

# Configuration file

The configuration file has one `KEY=VALUE` pair per line. Empty lines and
lines starting with `#` are ignored.

| Key | Required | Description | Example |
|---|---|---|---|
| `WIDTH` | yes | Maze width in cells (at least 1) | `WIDTH=20` |
| `HEIGHT` | yes | Maze height in cells (at least 1) | `HEIGHT=15` |
| `ENTRY` | yes | Entry coordinates `x,y` (column, row) | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `x,y`, different from the entry | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` for a perfect maze, `False` for a Pac-Man board | `PERFECT=True` |
| `SEED` | no | Random seed: the same seed always gives the same maze | `SEED=42` |

Example:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
#SEED=50
```

The file is validated with Pydantic. If the file is missing, a line is not
`KEY=VALUE`, a key is unknown or missing, a value has the wrong type, or the
entry/exit is outside the maze or both are the same cell, the program prints
a clear error message and exits without crashing.

## Output file

Each cell is written as one hexadecimal digit, where each bit is a closed
wall: North = 1, East = 2, South = 4, West = 8 (`F` means all four walls are
closed). The maze is written row by row, followed by an empty line, the entry
`x,y`, the exit `x,y` and the shortest path as letters `N`, `E`, `S`, `W`.

# Maze generation algorithm

## Perfect maze: iterative depth-first search

We use the **recursive backtracker** algorithm (a randomized depth-first
search), written with an explicit stack instead of recursion:

1. Every cell starts with its four walls closed.
2. Start at the first cell, mark it as visited and push it on the stack.
3. Look at the cell on top of the stack. If it has unvisited neighbours,
   choose one at random, open the wall between both cells (on both sides),
   mark the neighbour as visited and push it.
4. If it has no unvisited neighbours, pop it (go back one step).
5. Repeat until the stack is empty.

Every cell is visited exactly once and each new cell is joined to the maze
through exactly one opened wall, so the result is a **spanning tree**: there
is one and only one path between any two cells.

**Why this algorithm?**

- It always produces a perfect maze, which is what the subject asks for by
  default.
- It is short and easy to understand and debug.
- It creates long, winding corridors, which look good and make the maze
  interesting to solve.
- Using a stack instead of recursion avoids Python's recursion limit on big
  mazes.

## Pac-Man mode

When `PERFECT=False`, the perfect maze is generated first and then some
inner walls (East and South) are opened at random. This creates loops, so
there is more than one route between cells.

## Shortest path: breadth-first search

The solver uses **BFS** (breadth-first search). It explores the maze level by
level from the entry and remembers where each cell was reached from, so the
first time it reaches the exit, the path rebuilt backwards is the shortest
one. We first had a depth-first solver, but in a maze with loops DFS finds
*a* path, not always the *shortest* one, so we changed it to BFS.

# Reusable code

The maze generator and solver are in the `mazegen` package, which can be
installed in any other project. It does not depend on the configuration
file or on the display.

Build the package:

```
make build
```

Install it:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

Use it:

```python
from mazegen.generator import MazeGenerator
from mazegen.solver import solve_bfs

generator = MazeGenerator(height=15, width=20, perfect=True)
maze = generator.generate()      # list of rows; each cell is 0-15
path = solve_bfs(generator, (0, 0), (14, 19))  # list of (row, col) cells
```

Inside the package, coordinates are `(row, col)`. The configuration file
uses `x,y` (column, row); the conversion is done once in `a_maze_ing.py`.

# Team and project management

## Roles

- **aliao-tr**: maze generator (`mazegen/generator.py`), first solver,
  Pac-Man mode, first version of the Makefile.
- **plopez-l**: configuration parsing and validation (`config_parser.py`),
  error handling, main program (`a_maze_ing.py`), output file
  (`output_writer.py`), terminal display and menu (`display.py`), BFS solver,
  packaging (`pyproject.toml`) and README.

## Planning

We started by reading the subject together and splitting it into
independent modules with clear inputs and outputs: config → generator →
solver → output file → display. Each of us took a group of modules, and we
used a shared GitHub repository to put them together.

How the plan changed:

- When we connected the modules we found that the generator and the rest of
  the code used coordinates in a different order. We agreed to use
  `(row, col)` everywhere inside the program and convert from `x,y` only
  when reading the config and writing the output file.
- We found a bug where the grid was built by columns instead of by rows. We
  wrote the needed changes in a shared note and fixed it.
- We replaced the DFS solver with BFS to always get the shortest path.
- The `make lint` rule was checking the virtual environment too, so we
  excluded `.venv`.

## What worked well and what could be improved

- **Worked well**: small modules with clear interfaces, so each one could be
  tested on its own; Pydantic for validation, which gave clear error
  messages with little code; checking every change with `make lint`.
- **Could be improved**: agreeing on conventions (like the coordinate order)
  at the very beginning, writing more descriptive commit messages, and
  running the linters before every commit instead of after.

## Tools

Git and GitHub, VS Code, vim, `flake8`, `mypy`, Pydantic, `pdb`, and the
`maze_analyzer.py` script to check the generated mazes.

# Resources

- [Python documentation](https://docs.python.org/3/) (`random`, `typing`,
  `sys`)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Maze generation algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Maze generation: recursive backtracking (Jamis Buck)](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Breadth-first search (Wikipedia)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes (Wikipedia)](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [mypy documentation](https://mypy.readthedocs.io/) and
  [flake8 documentation](https://flake8.pycqa.org/)

## Use of AI

We used an AI assistant (Claude, by Anthropic) as a study and review tool
during the project:

- **Understanding**: explaining the subject, and concepts such as Pydantic
  validation, walls stored as bits, hexadecimal output, BFS vs DFS, ANSI
  colour codes, Makefiles, virtual environments and Python packaging.
- **Reviewing and debugging**: reading our code, explaining `flake8` and
  `mypy` errors, and helping find bugs such as the coordinate mix-up and the
  grid built by columns.
- **Code suggestions**: proposing implementations, step by step, for parts
  such as the config validation, the output writer, the terminal display and
  menu, and the packaging files. We read, adapted, tested and integrated
  them ourselves.
- **Documentation**: helping write the docstrings and this README.

Every change was reviewed and tested by us before being committed, and we
can explain all the code in the project.
