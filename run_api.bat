@echo off

REM Activate virtual environment (Windows style)
call myenv\Scripts\activate.bat

REM Run the Python script
uvicorn main:app