@echo off
title CSC & ANSO Scholarship Outreach Agent
echo ========================================================
echo   Launching CSC & ANSO Scholarship Outreach Agent
echo   Field: Agriculture - Agronomy (GPA: 3.52)
echo ========================================================
echo.

cd /d "%~dp0"

:: Check for python or py launcher
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYCMD=python
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set PYCMD=py
    ) else (
        echo ERROR: Python is not installed or not in PATH!
        echo Please install Python from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo Using Python command: %PYCMD%
echo Checking requirements...
%PYCMD% -m pip install -r requirements.txt

echo.
echo Launching Web Dashboard in your browser...
echo.

%PYCMD% -m streamlit run app.py

pause
