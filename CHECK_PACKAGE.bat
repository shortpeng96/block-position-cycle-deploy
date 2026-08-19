@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Block Position Cycle - Package Check
set "FAILED=0"

call :check_file "streamlit_app.py"
call :check_file "requirements.txt"
call :check_file "AGENTS.md"
call :check_file "CODEX_START_PROMPT.txt"
call :check_folder "data"
call :check_folder "outputs"
call :check_folder "Docs"
call :check_folder "Data of Ship Block Scheduling in English"

if "%FAILED%"=="1" goto failed

echo.
echo [OK] All required project files and folders exist.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import streamlit,pandas,numpy,matplotlib,seaborn,plotly,sklearn,joblib,openpyxl; print('[OK] Python libraries can be imported.')"
) else (
    echo [INFO] The virtual environment has not been created yet.
    echo Run START_APP.bat once.
)
goto end

:check_file
if exist "%~1" (
    echo [OK] %~1
) else (
    echo [MISSING] %~1
    set "FAILED=1"
)
exit /b

:check_folder
if exist "%~1\" (
    echo [OK] %~1\
) else (
    echo [MISSING] %~1\
    set "FAILED=1"
)
exit /b

:failed
echo.
echo [ERROR] Some required files are missing. Extract the entire ZIP again.

:end
echo.
pause
