from typing import Any, Optional
from pydantic import (
    BaseModel, ConfigDict, Field, ValidationError, field_validator,
    model_validator
)
from mazegen.pattern import pattern_cells


class MazeParameters(BaseModel):
    """
    Defines the configuration parameters required to generate a maze.

    Stores the maze dimensions, entry and exit coordinates, output
    file settings and generation options. Configuration values are
    validated automatically using Pydantic.

    Coordinates are represented as (x, y), with the column first
    and the row second, matching the format used in the config file.

    Attributes:
        WIDTH (int): Width of the maze in columns. Must be at least 1.
        HEIGHT (int): Height of the maze in rows. Must be at least 1.
        ENTRY (tuple[int, int]): Starting coordinates (x, y).
        EXIT (tuple[int, int]): Destination coordinates (x, y).
        OUTPUT_FILE (str): Path or name of the file where the maze
            will be saved. Cannot be empty.
        PERFECT (bool): Determines whether a perfect maze is generated.
            Defaults to False.
        SEED (Optional[int]): Optional random seed used for maze
            generation. Defaults to None.

    Note:
        Extra configuration fields are not allowed.
    """
    model_config = ConfigDict(extra='forbid')

    WIDTH: int = Field(..., ge=1, le=70)
    HEIGHT: int = Field(..., ge=1, le=70)
    ENTRY: tuple[int, int] = Field(...)
    EXIT: tuple[int, int] = Field(...)
    OUTPUT_FILE: str = Field(..., min_length=1)
    PERFECT: bool = Field(...)
    SEED: Optional[int] = Field(None)

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def split_coordinates(cls, value: Any) -> Any:
        """
        Converts coordinate strings into pairs of individual values
        before field validation.

        If the input is a string, splits it using the comma separator
        and removes any surrounding whitespace from each coordinate.
        Non-string values are returned unchanged.

        Args:
            value (Any): The input value to process, typically a coordinate
                string in the format "x,y".

        Returns:
            Any: A tuple containing the two coordinate values as strings,
                or the original value if it is not a string.

        Raises:
            ValueError: If the input string does not contain exactly
                two values separated by a comma.
        """
        if isinstance(value, str):
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError(
                    "must be two numbers separated by a comma, e.g. 0,0"
                )
            return (parts[0].strip(), parts[1].strip())
        return value

    @model_validator(mode="after")
    def check_entry_and_exit(self) -> "MazeParameters":
        """
        Validates the entry and exit positions after the model fields
        have been initialized.

        Ensures that both positions are within the maze boundaries,
        that the entry and exit are different, and that neither position
        overlaps with the 42 pattern when it is present.

        Coordinates are provided as (x, y), but the pattern uses
        (row, col), so positions are converted to (y, x) when checked
        against the pattern.

        Returns:
            MazeParameters: The validated instance.

        Raises:
            ValueError: If either position is outside the maze,
                if the entry and exit are identical, or if either
                position overlaps with the 42 pattern.
        """
        points = (("ENTRY", self.ENTRY), ("EXIT", self.EXIT))
        for name, (x, y) in points:
            if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
                raise ValueError(
                    f"{name} {x},{y} is outside the maze "
                    f"(x from 0 to {self.WIDTH - 1}, "
                    f"y from 0 to {self.HEIGHT - 1})"
                )
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")

        blocked = pattern_cells(self.HEIGHT, self.WIDTH)
        if blocked is not None:
            for name, (x, y) in points:
                if (y, x) in blocked:
                    raise ValueError(
                        f"{name} {x},{y} is inside the 42 pattern"
                    )
        return self


def read_config(path: str) -> dict[str, str]:
    """
    Reads a configuration file and extracts its KEY=VALUE pairs
    into a dictionary of strings.

    Ignores empty lines and comments (lines starting with '#').
    Each non-empty line must contain an '=' separator, and duplicate
    keys are not allowed.

    Args:
        path (str): Path to the configuration file to read.

    Returns:
        dict[str, str]: Dictionary containing the configuration
            keys and their corresponding values as strings.

    Raises:
        OSError: If the file cannot be opened or read.
        ValueError: If a line does not follow the KEY=VALUE format
            or if a configuration key appears more than once.
    """
    data: dict[str, str] = {}
    with open(path, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(
                    f"line {number}: expected KEY=VALUE, got '{line}'"
                )
            key, value = line.split("=", 1)
            key = key.strip().upper()
            if key in data:
                raise ValueError(
                    f"line {number}: '{key}' appears more than once"
                )
            data[key] = value.strip()
    return data


def load_config(path: str) -> MazeParameters:
    """
    Loads and validates the maze configuration from a file.

    Reads the configuration file and validates its contents against
    the MazeParameters model. If the configuration contains invalid
    values, converts the validation errors into a readable ValueError
    message identifying the affected fields.

    Args:
        path (str): Path to the configuration file to load.

    Returns:
        MazeParameters: Validated configuration parameters.

    Raises:
        OSError: If the configuration file cannot be accessed or read.
        ValueError: If the configuration file contains invalid data.
            The error message includes details about the invalid fields.
    """
    try:
        return MazeParameters.model_validate(read_config(path))
    except ValidationError as error:
        lines = ["invalid configuration"]
        for problem in error.errors():
            field = ".".join(str(part) for part in problem["loc"]) or "config"
            message = problem["msg"].removeprefix("Value error, ")
            lines.append(f"  {field}: {message}")
        raise ValueError("\n".join(lines)) from None
