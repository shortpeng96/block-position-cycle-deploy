@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Block Position Cycle - Streamlit
set "PIP_DISABLE_PIP_VERSION_CHECK=1"
set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"
set "PY_CMD="

py -3.10 --version >nul 2>&1
if not errorlevel 1 set "PY_CMD=py -3.10"

if not defined PY_CMD (
    py -3.11 --version >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py -3.11"
)

if not defined PY_CMD (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 set "PY_CMD=py -3.12"
)

if not defined PY_CMD (
    python -c "import sys; raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1)" >nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)

if not defined PY_CMD goto no_python

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Python virtual environment is being created.
    %PY_CMD% -m venv ".venv"
    if errorlevel 1 goto setup_error
)

if not exist ".venv\setup_complete.txt" (
    echo [2/3] Required libraries are being installed.
    echo The first installation may take several minutes.
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    if errorlevel 1 goto setup_error
    ".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
    if errorlevel 1 goto setup_error
    echo ready> ".venv\setup_complete.txt"
)

echo [3/3] Streamlit is starting.
echo Keep this window open while using the dashboard.
".venv\Scripts\python.exe" -m streamlit run "streamlit_app.py"
goto end

:no_python
echo.
echo [ERROR] Python 3.10 or 3.11 was not found.
echo Install 64-bit Python 3.10, 3.11, or 3.12 and select Add Python to PATH.
goto failed

:setup_error
echo.
echo [ERROR] The Python environment or libraries could not be installed.
echo Check the internet connection, then delete the .venv folder and try again.
goto failed

:failed
echo.
pause
exit /b 1

:end
pause
