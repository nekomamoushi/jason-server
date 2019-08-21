#!/usr/bin/env bash

# kill the current script and all the background processes.
trap "kill 0" EXIT

# run unit tests
pytest --disable-warnings tests/unit/

# run integration tests
jason-server -q --port 8100 watch tests/data/big_database.json &
pytest --disable-warnings tests/integration/test_app.py
