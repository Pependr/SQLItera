#!/bin/bash

uv init $1
git init

mkdir tests/
cd tests/
mkdir example/
cd example/
touch test_example.py
printf "def test_example() -> None:\n\tassert True\n" >> test_example.py
cd ..
cd ..

uv venv
source .venv/bin/activate

uv python install $2

uv add ruff pytest pytest-cov --dev
uv sync --dev

unlink init.sh
