# mazegen

Reusable maze generator and solver, created as part of the 42 project
A-Maze-ing by aliao-tr and plopez-l.

## Installation

```
pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic example

```python
from mazegen import MazeGenerator, solve_bfs

generator = MazeGenerator(height=15, width=20, perfect=True, seed=42)
maze = generator.generate()

path = solve_bfs(generator, (0, 0), (14, 19))
print(path)
```

## Parameters

`MazeGenerator(height, width, perfect, seed=None)`:

- `height`: number of rows (at least 1).
- `width`: number of columns (at least 1).
- `perfect`: `True` for a perfect maze (exactly one path between any two
  cells), `False` for a Pac-Man-like board with loops and few dead ends.
- `seed`: optional. The same seed always gives the same maze; `None` (the
  default) gives a different maze every time.

## The generated structure

`generate()` returns the maze as a list of rows, `maze[row][col]`. Each cell
is a number from 0 to 15 where each bit is a closed wall:

| Bit | Value | Wall |
|---|---|---|
| 0 | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

For example, `maze[0][0] & 1` is not 0 when the top-left cell has its north
wall closed. A cell with value 15 has all four walls closed: these cells draw
the "42" pattern, when the maze is big enough for it.

## The solution

`solve_bfs(generator, start, end)` returns the shortest path from `start` to
`end` as a list of `(row, col)` cells, both included, or `None` if there is
no path.

All coordinates in this package are `(row, col)`.
