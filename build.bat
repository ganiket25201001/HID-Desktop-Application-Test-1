@echo off
echo ========================================
echo Device Monitor Pro - Build Tool
echo ========================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install pyinstaller winshell pywin32

echo.
echo ========================================
echo Step 1: Building Executable
echo ========================================
echo.
echo This may take a few minutes...
echo.

REM Build the executable with proper customtkinter support
.venv\Scripts\python.exe -m PyInstaller --name="DeviceMonitorPro" ^
    --onefile ^
    --windowed ^
    --icon=app_icon.ico ^
    --hidden-import=customtkinter ^
    --hidden-import=wmi ^
    --hidden-import=pythoncom ^
    --hidden-import=win32com.client ^
    --noupx ^
    --clean ^
    run_dashboard.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo Build Failed!
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Executable Build Complete!
echo ========================================
echo.
echo Your executable is located at:
echo dist\DeviceMonitorPro.exe
echo.
echo.

REM Ask user if they want to create shortcuts
choice /C YN /M "Do you want to create Desktop and Start Menu shortcuts"

if errorlevel 2 goto :ask_installer
if errorlevel 1 (
    echo.
    echo Creating shortcuts...
    .venv\Scripts\python.exe create_shortcuts.py
)

:ask_installer
echo.
echo ========================================
echo Step 2: Professional Installer (Optional)
echo ========================================
echo.
choice /C YN /M "Do you want to build a professional Windows installer"

if errorlevel 2 goto :end
if errorlevel 1 goto :build_installer

:build_installer
REM Check if Inno Setup is installed
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo.
    echo ERROR: Inno Setup not found!
    echo.
    echo Please download and install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    echo.
    goto :end
)

REM Create installer directory
if not exist "installer" mkdir installer

echo.
echo Building installer with Inno Setup...
echo.

REM Compile the installer
"%INNO_PATH%" "installer_script.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Installer Build Complete!
    echo ========================================
    echo.
    echo Your installer is located at:
    echo installer\DeviceMonitorPro_Setup_v1.0.0.exe
    echo.
    echo You can now distribute this installer to users!
    echo.
) else (
    echo.
    echo ========================================
    echo Installer Build Failed!
    echo ========================================
    echo.
)

:end
echo.
echo ========================================
echo All Done!
echo ========================================
echo.
pause
