@echo off
REM ----------------------------------------
REM Batch script to hash generated code and trigger build if hash matches
REM ----------------------------------------

REM 1. Preset hash to compare
set PRESET_HASH=f25c607390e41c41aad982985d690d884762af97e7f62be81fac498dad25c6d3

REM 2. Path to generated folder (default _builds/_out)
set GEN_FOLDER=_builds\_out

REM 3. Run hashgen.py
echo [INFO] Running hashgen.py on %GEN_FOLDER%
python hashgen.py %GEN_FOLDER%
if errorlevel 1 (
    echo [ERROR] hashgen.py failed
    exit /b 1
)

REM 4. Read hash from _hashgen\hash.txt
setlocal enabledelayedexpansion
set HASH_FILE=_hashgen\hash.txt
set CURRENT_HASH=

for /f "usebackq delims=" %%A in ("%HASH_FILE%") do (
    set CURRENT_HASH=%%A
)

REM 5. Compare hash
if "!CURRENT_HASH!"=="%PRESET_HASH%" (
    echo [INFO] Hash matches preset value. Running do_clean_build.bat...
    call do_clean_build.bat
) else (
    echo [INFO] Hash does not match preset value. Skipping build.
)

endlocal
