*This project has been created as part of the 42 curriculum by aliao-tr, plopez-l*

# Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, generates a random maze, finds the shortest path between the entry and
the exit, writes the result to an output file and shows it in the terminal
with an interactive menu.

Two kinds of maze can be generated:

- **Perfect** (`PERFECT=True`): there is exactly one path between any two
  cells, so there are no loops.
- **Pac-Man board** (`PERFECT=False`): a board usable by a Pac-Man-like
  game, with many independent routes and almost no dead ends.

Every maze has its outer border closed and coherent walls between
neighbouring cells: if a cell has its East wall closed, the cell on its right
has its West wall closed too.

When the maze is big enough (at least 9 columns and 7 rows), a **"42"** is
drawn in its centre with fully closed cells. If it does not fit, the maze is
generated without it and a message is shown.

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

## Display and interactive menu

The maze is drawn in the terminal with ASCII characters and ANSI colours:

- walls in pink by default, the entry `E` in white and the exit `X` in red;
- the "42" cells filled in yellow;
- the shortest path, when shown, with a green background by default;
- an info line with the size, the type of maze and the length of the path,
  e.g. `20x15 | perfect | path: 47 steps`.

| Option | Action |
|---|---|
| 1 | Generate a new maze with the same configuration |
| 2 | Show / hide the shortest path |
| 3 | Change the wall colour |
| 4 | Change the path colour |
| 5 | Quit |

`Ctrl+C` and `Ctrl+D` also quit cleanly, with the message
`Stopped by the user`.

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
lines starting with `#` are ignored. Keys can be written in upper or lower
case (`WIDTH` or `width`).

| Key | Required | Description | Example |
|---|---|---|---|
| `WIDTH` | yes | Maze width in cells, from 1 to 70 | `WIDTH=20` |
| `HEIGHT` | yes | Maze height in cells, from 1 to 70 | `HEIGHT=15` |
| `ENTRY` | yes | Entry coordinates `x,y` (column, row) | `ENTRY=0,0` |
| `EXIT` | yes | Exit coordinates `x,y`, different from the entry | `EXIT=19,14` |
| `OUTPUT_FILE` | yes | Name of the output file (`.txt`, not `config.txt`) | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | yes | `True` for a perfect maze, `False` for a Pac-Man board | `PERFECT=False` |
| `SEED` | no | Random seed: the same seed always gives the same mazes | `SEED=42` |

The maximum size of 70 keeps the maze readable in a terminal and quick to
generate.

Example (the default `config.txt`):

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
#SEED=42
```

The file is validated with Pydantic. The program prints a clear error message
and exits without crashing if:

- the file does not exist or cannot be read;
- a line is not `KEY=VALUE`, or a key appears more than once;
- a key is unknown, or a required key is missing;
- a value has the wrong type or range (e.g. `WIDTH=hello`, `WIDTH=0`,
  `HEIGHT=100`, `PERFECT=maybe`, `ENTRY=0`);
- the entry or the exit is outside the maze, inside the "42", or both are
  the same cell;
- the output file is not a `.txt` file, is `config.txt`, or cannot be written.

When several values are wrong, all the errors are shown at once.

## Output file

Each cell is written as one hexadecimal digit, where each bit is a closed
wall: North = 1, East = 2, South = 4, West = 8 (`F` means all four walls are
closed). The maze is written row by row (`HEIGHT` lines of `WIDTH`
characters), followed by an empty line, the entry `x,y`, the exit `x,y` and
the shortest path as letters `N`, `E`, `S`, `W`.

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
is one and only one path between any two cells, and every cell is reachable.

**Why this algorithm?**

- It always produces a perfect maze.
- It is short and easy to understand and debug.
- It creates long, winding corridors, which look good and make the maze
  interesting to solve.
- Using a stack instead of recursion avoids Python's recursion limit on big
  mazes.

## The "42" pattern

The shape of the "42" is drawn as text in `mazegen/pattern.py` (`#` is a
closed cell), so it is easy to read and to change. It is placed in the centre
of the maze, with at least one free cell around it.

Before the depth-first search starts, the "42" cells are marked as
**already visited**. The algorithm never enters them, so they keep their four
walls closed, and the rest of the maze is built around them. The free cells
inside the "42" all have an exit, so no part of the maze is cut off.

## Pac-Man mode

When `PERFECT=False`, the perfect maze is generated first and then:

1. `remove_extra_walls` opens inner walls at random (20 % of them), which
   creates many loops, so there are several independent routes. Before
   opening a wall, `creates_large_open_space` checks that it would not
   create an open area of 3x3 cells.
2. `reduce_dead_ends` opens one more wall in each dead end (a cell with
   three closed walls), until at most 2 dead ends are left.

The outer border and the "42" cells are never opened. With the default
size, the result usually has no dead end at all, which `maze_analyzer.py`
reports as "bonus-grade".

## Randomness and seed

Each `MazeGenerator` has its own random generator (`random.Random(seed)`),
and all the randomness comes from it, so the same seed always gives the same
maze.

In the program, the first maze uses the `SEED` of the configuration file.
For option 1 of the menu, `create_regenerate` creates a second random
generator from the same `SEED`, which gives a new seed for each regenerated
maze. So the same `SEED` always shows the same sequence of mazes, and every
maze of the sequence is different. Without `SEED`, every maze is random.

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

| File | Content |
|---|---|
| `mazegen/__init__.py` | Exposes `MazeGenerator`, `solve_bfs` and `pattern_cells` |
| `mazegen/generator.py` | `MazeGenerator` class |
| `mazegen/solver.py` | `solve_bfs`, the shortest path |
| `mazegen/pattern.py` | The "42" shape and its position |
| `mazegen/README.md` | Documentation of the package |

Build the package:

```
make build
```

The `.whl` file includes the code, the documentation (`mazegen/README.md`)
and the license.

Install it:

```
pip install mazegen-1.0.0-py3-none-any.whl
```

Use it:

```python
from mazegen import MazeGenerator, solve_bfs

generator = MazeGenerator(height=15, width=20, perfect=True, seed=42)
maze = generator.generate()      # list of rows; each cell is 0-15
path = solve_bfs(generator, (0, 0), (14, 19))  # list of (row, col) cells
```

Parameters: `height` and `width` (size in cells), `perfect` (`True` or
`False`) and `seed` (optional; `None` gives a different maze every time).

Inside the package, coordinates are `(row, col)`. The configuration file
uses `x,y` (column, row); the conversion is done once in `a_maze_ing.py`.

# Team and project management

## Roles

- **aliao-tr**: maze generator (`mazegen/generator.py`), first solver,
  Pac-Man mode, seed in the generator, package interface
  (`mazegen/__init__.py`), first version of the Makefile.
- **plopez-l**: configuration parsing and validation (`config_parser.py`),
  error handling, main program (`a_maze_ing.py`), output file
  (`output_writer.py`), terminal display and menu (`display.py`), BFS solver,
  "42" pattern (`mazegen/pattern.py`), packaging (`pyproject.toml`) and
  README.

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
- Testing every kind of wrong configuration file showed some error messages
  that were hard to read, so we made them clearer, and we added checks for
  repeated keys, lowercase keys, a maximum size and an entry or exit inside
  the "42".
- When the seed was added to the generator, option 1 of the menu started
  showing always the same maze. We fixed it with a second random generator,
  created from the same seed, that gives a new seed to each regenerated
  maze.
- Pressing `Ctrl+D` in the menu made the program crash, so we handle it like
  `Ctrl+C`.

## What worked well and what could be improved

- **Worked well**: small modules with clear interfaces, so each one could be
  tested on its own; Pydantic for validation, which gave clear error
  messages with little code; checking every change with `make lint`; testing
  the output with `maze_analyzer.py`.
- **Could be improved**: agreeing on conventions (like the coordinate order)
  at the very beginning, writing more descriptive commit messages, running
  the linters before every commit instead of after, and telling each other
  before editing the same file.

## Tools

Git and GitHub, VS Code, vim, `flake8`, `mypy`, Pydantic, `pdb`, `build`,
and the `maze_analyzer.py` script from the subject to check the generated
mazes.

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
  `mypy` errors, and helping find bugs such as the coordinate mix-up, the
  grid built by columns, the seed repeating the same maze and the `Ctrl+D`
  crash.
- **Testing**: suggesting wrong configuration files to try, and checking
  the results with `maze_analyzer.py`.
- **Code suggestions**: proposing implementations, step by step, for parts
  such as the config validation, the output writer, the terminal display and
  menu, the "42" pattern and the packaging files. We read, adapted, tested
  and integrated them ourselves.
- **Documentation**: helping write the docstrings and this README.

Every change was reviewed and tested by us before being committed, and we
can explain all the code in the project.
