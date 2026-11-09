.PHONY: install run debug clean lint lint-strict

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
APP := a_maze_ing.py
CONFIG := config.txt
SRC := .

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Runs the application
run:
	$(BIN)/python $(APP) $(CONFIG)

# debug with pdb
debug:
	$(BIN)/python -m pdb $(APP) $(CONFIG)

# Removes temporary files and/or caches
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .flake8_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

# Check style and types
lint:
	$(BIN)/flake8 $(SRC) --exclude $(VENV)
	$(BIN)/mypy $(SRC) --exclude '\$(VENV)' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(BIN)/flake8 $(SRC) --exclude $(VENV)
	$(BIN)/mypy $(SRC) --exclude '\$(VENV)' --strict
