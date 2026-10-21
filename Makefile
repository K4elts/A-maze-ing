.PHONY: install run debug clean lint

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip
APP := main.py
SRC := .

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install flake8 mypy

# Runs the application
run:
	$(BIN)/python $(APP)

# debug with pdb
debug:
	$(BIN)/python -m pdb $(APP)

# Removes temporaty files and/or caches
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .flake8_cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

# Comprobar estilo y tipos
lint:
	$(BIN)/flake8 $(SRC)
	$(BIN)/mypy $(SRC) --warn-return-any --warn-unused-ignores
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(BIN)/flake8 $(SRC)
	$(BIN)/mypy $(SRC) --strict