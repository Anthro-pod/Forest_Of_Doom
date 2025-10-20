# Forest of Doom

Small text-adventure refactored into modules for better testing and maintenance.

Run the game:

```
python forest_of_doom/main.py
```

Or run in fast mode (no pauses):

```
python -m forest_of_doom.main --fast --seed 0
```

Run tests:

```
/home/eca/Documents/Forest_Of_Doom/.venv/bin/python -m pytest -q
```
# Forest_Of_Doom
This is a Python-based text adventure game inspired by "The Forest of Doom" by Ian Livingstone

## Run (cross-platform)

Short helper scripts are provided to make running the game and tests easy across shells and IDEs.

PowerShell (Windows)
```powershell
cd 'C:\Users\erica\OneDrive\Documents\Forest_Of_Doom'
.\run_game.ps1               # create venv if needed, install reqs, run game interactively
.\run_game.ps1 -Fast -Seed 0 # fast mode, deterministic seed
.\run_game.ps1 -Tests        # run tests (pytest)
```

cmd.exe (Windows)
```cmd
cd C:\Users\erica\OneDrive\Documents\Forest_Of_Doom
run_game.bat                 # create venv, install reqs, run game
run_game.bat --tests         # run tests
```

bash / WSL / macOS / Linux
```bash
cd /path/to/Forest_Of_Doom
./run_game.sh                # create venv, install reqs, run game
./run_game.sh --tests        # run tests
```

VS Code

Open the project in VS Code and use the Run and Debug pane. Configurations are in `.vscode/launch.json` and include:

 - "Run Forest of Doom (module)" — runs `forest_of_doom.main` in the integrated terminal
- "Run Forest of Doom (fast)" — runs with `--fast --seed 0`
- "Run Forest of Doom (load/save)" — example run that uses `${workspaceFolder}\player.json` for load/save
- "Run Tests (pytest)" — runs pytest

Notes:
- The game itself only uses the Python standard library. `requirements.txt` contains `pytest` for tests.
- If PowerShell blocks running scripts, run with `-ExecutionPolicy Bypass` or use the `Activate.ps1` pattern shown in the PowerShell commands above.

