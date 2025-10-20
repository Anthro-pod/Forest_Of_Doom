#!/usr/bin/env bash
# run_game.sh - create venv, install deps, run game or tests (bash / WSL / macOS / Linux)
# Usage:
#   ./run_game.sh                 # create venv (if needed) and run game
#   ./run_game.sh --fast          # run game in fast mode
#   ./run_game.sh --seed 0        # run game with deterministic seed
#   ./run_game.sh --load player.json --save player.json
#   ./run_game.sh --tests         # run pytest

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
VENV="$SCRIPT_DIR/.venv"
PY="$VENV/bin/python"

if [ ! -d "$VENV" ]; then
  echo "Creating virtual environment at $VENV..."
  python3 -m venv "$VENV" || python -m venv "$VENV"
fi

if [ -f "$VENV/bin/activate" ]; then
  # shellcheck source=/dev/null
  . "$VENV/bin/activate"
fi

if [ -f requirements.txt ]; then
  echo "Installing requirements from requirements.txt..."
  "$PY" -m pip install --upgrade pip >/dev/null
  "$PY" -m pip install -r requirements.txt
fi

if [ "${1-}" = "--tests" ] || [ "${1-}" = "-Tests" ]; then
  shift
  "$PY" -m pytest -q "$@"
  exit
fi

# Run the game (module form works well across environments)
exec "$PY" -m Forrest_of_Doom.main "$@"
