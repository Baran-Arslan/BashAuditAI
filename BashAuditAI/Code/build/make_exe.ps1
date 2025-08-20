#requires -Version 5
param(
    [switch]$NoVenv
)
if (-not $NoVenv) {
    python -m venv .venv
    . .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
} else {
    . .\.venv\Scripts\Activate.ps1
}
pyinstaller --noconfirm --onefile --windowed --name "ShellAnalyzer" main.py
Write-Host "EXE hazır: dist\ShellAnalyzer.exe"
