#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VIRTUALENV_DIR := "venv"
PYTHON_INTERPRETER = python3

#################################################################################
# SETUP                                                                         #
#################################################################################

## Set up python interpreter environment 
create_environment:
	$(PYTHON_INTERPRETER) -m venv $(VIRTUALENV_DIR)
	@echo ">>> New virtualenv created. Activate with:\nsource $(VIRTUALENV_DIR)/bin/activate"

## Install all Python Dependencies
install: requirements_dev requirements

## Install Python Dependencies for development tools
requirements_dev: 
	$(PYTHON_INTERPRETER) -m pip install -r requirements-dev.txt

## Install Python Dependencies for application
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

.PHONY: create_environment install requirements_dev requirements

#################################################################################
# DEVELOPMENT COMMANDS                                                          #
#################################################################################

## Delete all compiled Python files

clean: clean_py clean_cdk

clean_py:
	find . -type f -name '._*' -delete
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Format using Black
format: 
	isort src --profile black
	black src

## Type check using mypy
typecheck:
	mypy --no-incremental --ignore-missing-imports src

## Lint using flake8
lint:
	flake8 src

## Run tests using pytest
test:
	pytest tests/

.PHONY: clean clean_py format lint test

