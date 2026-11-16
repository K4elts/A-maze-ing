PATTERN: list[str] = [
    "#...###",
    "#.....#",
    "###.###",
    "..#.#..",
    "..#.###",
]


def pattern_offsets() -> set[tuple[int, int]]:
    """
    Calculates and returns the coordinates of all '#' characters in PATTERN.

    Each coordinate is represented as a (row, col) tuple, with positions
    measured relative to the top-left corner of the pattern.

    Returns:
        set[tuple[int, int]]: A set containing the (row, col) coordinates
        of every '#' character found in PATTERN.
    """
    offsets: set[tuple[int, int]] = set()
    for row, line in enumerate(PATTERN):
        for col, char in enumerate(line):
            if char == "#":
                offsets.add((row, col))
    return offsets


def pattern_cells(height: int, width: int) -> set[tuple[int, int]] | None:
    """
    Calculates the maze coordinates occupied by the pattern when centred
    within the given maze dimensions.

    Ensures that the pattern has at least one free cell of space around
    it and does not touch the maze borders.

    Args:
        height (int): The height of the maze in rows.
        width (int): The width of the maze in columns.

    Returns:
        set[tuple[int, int]] | None: A set of (row, col) coordinates
        occupied by the pattern, or None if the maze is too small
        to fit the pattern with the required spacing.
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
