import sys

from pydantic import ValidationError

from config_parser import MazeParameters, read_config

if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py <config_file>")
    sys.exit(1)

config_path = sys.argv[1]

try:
    params = MazeParameters.model_validate(read_config(config_path))
except OSError as error:
    print(f"Error: cannot read '{config_path}': {error.strerror}")
    sys.exit(1)
except ValidationError as error:
    print("Error: invalid configuration")
    print(error)
    sys.exit(1)
except ValueError as error:
    print(f"Error: {error}")
    sys.exit(1)

print(params)
