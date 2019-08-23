PACKAGE_NAME:=jason_server
PIPENV:=pipenv
PYTHON:=python
PYTEST:=pytest
TWINE:=twine

.PHONY: help cleany install

help:
	@echo "Please use 'make <target>' with available <target>"
	@echo "  init             to install all your dev dependencies"
	@echo "  venv             to create the venc with pipenv"
	@echo "  install          to install your dependencies"
	@echo "    install-dev    to install also your dev-dependencies"
	@echo "    editable       to make your package installable and testable"
	@echo "  clean            to clean them all"
	@echo "  build            to build sdist and wheel"
	@echo "    build-sdist    to build a source distribution"
	@echo "    build-wheel    to build a wheel (see setup.cfg for universal wheel)"
	@echo "  tests            to launch tests with pytest"
	@echo "  coverage         to coverage your code"
	@echo "  upload-pypi      to upload your package to testpypi.org"
	@echo "  upload-test      to upload your package to pypi.org"

# --------------------------------------------------------------------------- #
# Init Environment
# --------------------------------------------------------------------------- #
venv:
	$(PIPENV) --three

install:
	$(PIPENV) install

install-dev:
	$(PIPENV) install --dev

editable:
	$(PIPENV) install -e .

# --------------------------------------------------------------------------- #
# Clean Environment
# --------------------------------------------------------------------------- #
clean: clean-build clean-test

clean-python: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf src/*egg-info/

clean-test:
	@rm -rf .pytest_cache
	@rm -rf .tox/
	@rm -rf .coverage
	@rm -rf htmlcov

# --------------------------------------------------------------------------- #
# Build Environment
# --------------------------------------------------------------------------- #

build:
	$(PYTHON) setup.py sdist bdist_wheel

# Source distribution
build-sdist:
	$(PYTHON) setup.py sdist

# Pure Python Wheel
build-wheel:
	$(PYTHON) setup.py bdist_wheel

# --------------------------------------------------------------------------- #
# Test Environment
# --------------------------------------------------------------------------- #

# Make sure pytest is installed
tests: editable
	@bash run_tests.sh

# Code Coverage (make sur pytest-cov is installed)
coverage:
	$(PYTEST) --cov=$(PACKAGE_NAME) tests/unit

# --------------------------------------------------------------------------- #
# Upload Environment
# --------------------------------------------------------------------------- #

# Make sure twine is installed
upload-pypi:
	$(TWINE) upload --repository pypi dist/*

upload-test:
	$(TWINE) upload --repository testpypi dist/*
