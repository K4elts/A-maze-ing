'''READS AND VALIDATES CONFIG.TXT'''
from typing import Any, Optional

from pydantic import (
    BaseModel, ConfigDict, ValidationError, Field, field_validator,
    model_validator
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
        for number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(
                    f"line {number}: expected KEY=VALUE, got '{line}'"
                )
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> None:
    '''
    -------------------------
        MAIN DE PRUEBA
    -------------------------
    '''
    config_path = "config.txt"

    try:
        # Leer el archivo de configuración
        config_data = read_config(config_path)

        # Validar los datos usando el modelo Pydantic
        params = MazeParameters.model_validate(config_data)

        # Mostrar los parámetros validados
        print("Configuración válida")
        print("-" * 30)
        print(f"WIDTH:       {params.WIDTH}")
        print(f"HEIGHT:      {params.HEIGHT}")
        print(f"ENTRY:       {params.ENTRY}")
        print(f"EXIT:        {params.EXIT}")
        print(f"OUTPUT_FILE: {params.OUTPUT_FILE}")
        print(f"PERFECT:     {params.PERFECT}")
        print(f"SEED:        {params.SEED}")

    except FileNotFoundError:
        print(f"Error: no se encuentra el archivo '{config_path}'.")

    except ValidationError as error:
        print("Error: la configuración no es válida.")
        print(error)

    except (ValueError, OSError) as error:
        print(f"Error al leer la configuración: {error}")


if __name__ == "__main__":
    main()
