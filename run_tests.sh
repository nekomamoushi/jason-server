#!/usr/bin/env bash

# kill the current script and all the background processes.
trap "kill 0" EXIT

jason-server --port 8100 watch tests/data/big_database.json &
pytest --disable-warnings -s tests/test_app.py

