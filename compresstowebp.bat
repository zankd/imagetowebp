@echo off
chcp 65001 > nul
title WebP Image Converter

echo Checking requirements...

python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

echo Checking dependencies...

python -c "import torch" > nul 2>&1
if errorlevel 1 (
    echo Installing PyTorch...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    if errorlevel 1 (
        echo Error installing PyTorch.
        pause
        exit /b
    )
)

python -c "from PIL import Image" > nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    pip install Pillow
    if errorlevel 1 (
        echo Error installing Pillow.
        pause
        exit /b
    )
)

echo All dependencies are installed successfully.
echo.
echo Starting conversion process...
echo.

python "%~dp0to_webp.py"
if errorlevel 1 (
    echo.
    echo An error occurred during conversion.
    echo Please check the error messages above.
    pause
    exit /b
)

pause
