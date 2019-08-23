#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Which version part to bump
PART=$1

# Update Version
bumpversion ${PART}

# Push to remote
git push

# Build package
make build

# Upload package via Twine
make upload-pypi

