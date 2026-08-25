# Start the backend: create venv, install deps, and run uvicorn
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venvPath = Join-Path $scriptDir '.venv'

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath..."
    python -m venv $venvPath
}

# Use the venv python to install requirements
& "$venvPath\Scripts\python" -m pip install --upgrade pip
& "$venvPath\Scripts\python" -m pip install -r (Join-Path $scriptDir 'requirement.txt')

Write-Host "Starting uvicorn (127.0.0.1:8000)..."
& "$venvPath\Scripts\python" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
