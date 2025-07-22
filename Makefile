VENV ?= .venv
PYTHON ?= python3
PIP ?= $(VENV)/bin/pip

.PHONY: install test lint build clean venv
build: install lint test

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install .

test:
	$(VENV)/bin/pytest -v

lint:
	$(VENV)/bin/flake8 task_tracker

clean:
	rm -f tasks.json tasks.json.bak
	rm -rf $(VENV)
	rm -rf .pytest_cache *.egg-info
