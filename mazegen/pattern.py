'''THE "42" PATTERN DRAWN INSIDE THE MAZE'''

PATTERN: list[str] = [
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
]


def pattern_offsets() -> set[tuple[int, int]]:
    """Return the (row, col) of every '#' in PATTERN.

    Positions are relative to the top-left corner of the pattern.
    """
    offsets: set[tuple[int, int]] = set()
    for row, line in enumerate(PATTERN):
        for col, char in enumerate(line):
            if char == "#":
                offsets.add((row, col))
    return offsets


def pattern_cells(height: int, width: int) -> set[tuple[int, int]] | None:
    """Return the maze cells (row, col) covered by the centred pattern.

    The pattern needs at least one free cell around it, so it does not
    touch the border.

    Returns:
        The set of cells, or None if the maze is too small for it.
    """
    pattern_height = len(PATTERN)
    pattern_width = len(PATTERN[0])
    if height < pattern_height + 2 or width < pattern_width + 2:
        return None

    top = (height - pattern_height) // 2
    left = (width - pattern_width) // 2

    cells: set[tuple[int, int]] = set()
    for row, col in pattern_offsets():
        cells.add((top + row, left + col))
    return cells
