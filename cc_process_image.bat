@echo off
REM Check if a file was dragged and dropped
if "%~1"=="" (
    echo Please drag and drop an image file onto this script.
    pause
    exit /b 1
)

set dir=%~dp0

set image_path=%~1

REM Prompt for custom palette usage
set /p use_palette="Use custom palette? (yes/no): "

REM Default palette value
set "palette="

REM Enable delayed expansion
setlocal enabledelayedexpansion

REM If the user chooses to use a custom palette, prompt for input and validate it
if /i "%use_palette%"=="yes" (
    :palette_input
    set /p custom_palette="Enter the custom palette (96 hex characters): "
    
    REM Validate the custom palette input
    echo %custom_palette% | findstr /r "^[0-9a-fA-F]\{96\}$" >nul
    if %errorlevel% neq 0 (
        echo Invalid palette. Please enter a string of exactly 96 hexadecimal characters.
        goto palette_input
    )
    set palette=%custom_palette%
) else (
    REM Use a temporary file to capture the output of image_palette.py
    for /f %%i in ('python3 "%dir%image_palette.py" "%image_path%"') do (
        set "palette=%%i"
    )

    REM Print the generated palette if not using custom palette
    echo Generated palette: !palette!
)

REM Prompt for chunk size
set /p chunk_size="Enter the chunk size (format WxH): "

REM Run image_convert.py with the provided arguments
python3 "%dir%image_convert.py" "%image_path%" "%palette%" "%chunk_size%"

REM End delayed expansion
endlocal

pause
