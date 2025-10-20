<#
run_game.ps1 - helper to create venv, install deps, run game or tests

Usage:
  .\run_game.ps1                 # create venv (if needed) and run game
  .\run_game.ps1 -Fast           # run game in fast mode
  .\run_game.ps1 -Seed 0        # run game with deterministic seed
  .\run_game.ps1 -Load player.json -Save player.json
  .\run_game.ps1 -Tests         # run pytest

This script is intended for PowerShell (Windows).
#>
param(
    [switch]$Fast,
    [int]$Seed = $null,
    [string]$Load = $null,
    [string]$Save = $null,
    [switch]$Tests
)

$scriptPath = $MyInvocation.MyCommand.Path
if ($scriptPath) {
    $projectRoot = Split-Path -Parent $scriptPath
} else {
    # fallback when the script is run interactively or pasted into the shell
    $projectRoot = (Get-Location).Path
}
Push-Location $projectRoot

$venvPath = Join-Path $projectRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

function Ensure-Venv {
    if (-not (Test-Path $venvPath)) {
        Write-Host "Creating virtual environment at $venvPath..."
        python -m venv $venvPath
    }
}

function Install-Reqs {
    if (Test-Path "requirements.txt") {
        Write-Host "Installing requirements from requirements.txt..."
        $pipRunner = $python
        if (-not $pipRunner) { $pipRunner = $pythonExe }
        if (-not $pipRunner) { $pipRunner = "python" }
        & $pipRunner -m pip install --upgrade pip | Out-Null
        & $pipRunner -m pip install -r requirements.txt
    }
}

# Create venv if missing
Ensure-Venv

# Activate the venv for this session
if (Test-Path $activateScript) {
    # Allow invocation policies in-process
    try {
        Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
    } catch {
        # ignore if we can't set execution policy
    }
    . $activateScript
} else {
    Write-Host "Warning: activation script not found. Using system 'python'."
}

# If venv was created, prefer its python
if (Test-Path $pythonExe) {
    $python = $pythonExe
} else {
    $python = "python"
}

# Install requirements using the resolved python (if any)
Install-Reqs

if ($Tests) {
    Write-Host "Running tests (pytest)..."
    & $python -m pytest -q
    Pop-Location
    return
}

# Build the argument list for main.py
$argList = @()
if ($Fast) { $argList += '--fast' }
if ($Seed -ne $null) { $argList += '--seed'; $argList += $Seed }
if ($Load) { $argList += '--load'; $argList += $Load }
if ($Save) { $argList += '--save'; $argList += $Save }

Write-Host "Starting game..."
$mainPy = Join-Path $projectRoot 'forest_of_doom\main.py'
if (-not (Test-Path $mainPy)) {
    Write-Error "Entrypoint $mainPy not found. Are you in the project root?"
    Pop-Location
    return
}

if ($argList.Count -eq 0) {
    # prefer running as module which preserves package imports
    & $python -m forest_of_doom.main
} else {
    & $python -m forest_of_doom.main @argList
}

Pop-Location
