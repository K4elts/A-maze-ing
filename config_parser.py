'''READS AND VALIDATES CONFIG.TXT'''
from pydantic import BaseModel, Field
from typing import Optional


class MazeParameters(BaseModel):
    WIDTH: int = Field(..., ge=1)
    HEIGHT: int = Field(..., ge=1)
    ENTRY: tuple[int, int] = Field(...)
    EXIT: tuple[int, int] = Field(...)
    OUTPUT_FILE: str = Field(...)
    PERFECT: bool = Field(...)
    SEED: Optional[int] = Field(None)
