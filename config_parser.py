'''READS AND VALIDATES CONFIG.TXT'''
from typing import Any, Optional

from pydantic import (
    BaseModel, ConfigDict, Field, field_validator, model_validator
)


class MazeParameters(BaseModel):
    model_config = ConfigDict(extra='forbid')

    WIDTH: int = Field(..., ge=1)
    HEIGHT: int = Field(..., ge=1)
    ENTRY: tuple[int, int] = Field(...)
    EXIT: tuple[int, int] = Field(...)
    OUTPUT_FILE: str = Field(..., min_length=1)
    PERFECT: bool = Field(...)
    SEED: Optional[int] = Field(None)

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def split_coordinates(cls, value: Any) -> Any:
        """Turn the text 'x,y' into the pair ('x', 'y')."""
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
        """Check that ENTRY and EXIT are inside the maze and different."""
        for name, (x, y) in (("ENTRY", self.ENTRY), ("EXIT", self.EXIT)):
            if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
                raise ValueError(
                    f"{name} {x},{y} is outside the maze "
                    f"(x from 0 to {self.WIDTH - 1}, "
                    f"y from 0 to {self.HEIGHT - 1})"
                )
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")
        return self


def read_config(path: str) -> dict[str, str]:
    """Read the config file and return its KEY=VALUE pairs as text."""
    data: dict[str, str] = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data
