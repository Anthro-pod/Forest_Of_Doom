@echo off
REM run_game.bat - helper to create venv, install deps, run game or tests (Windows cmd)
REM Usage:
REM   run_game.bat                 - create venv (if needed) and run game
REM   run_game.bat --fast          - run game in fast mode
REM   run_game.bat --seed 0        - run game with deterministic seed
REM   run_game.bat --load player.json --save player.json
REM   run_game.bat --tests         - run pytest

SETLOCAL ENABLEDELAYEDEXPANSION
SET SCRIPT_DIR=%~dp0
CD /D %SCRIPT_DIR%
IF NOT EXIST .venv (
    echo Creating virtual environment at .venv
    python -m venv .venv
)
.venv\Scripts\activate.bat
IF EXIST requirements.txt (
    echo Installing requirements from requirements.txt
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

REM Check for --tests flag
SET TESTFLAG=0
FOR %%A IN (%*) DO (
    IF /I "%%~A"=="--tests" SET TESTFLAG=1
)
IF "%TESTFLAG%"=="1" (
    .venv\Scripts\python.exe -m pytest -q
    GOTO :EOF
)

REM Run the game
.venv\Scripts\python.exe -m forest_of_doom.main %*
