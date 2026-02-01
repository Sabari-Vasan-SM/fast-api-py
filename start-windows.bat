@echo off
REM Quick Start Script for Todo App (Windows)

echo.
echo ========================================
echo Todo App - Quick Start
echo ========================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [1] Starting PostgreSQL with Docker Compose...
    docker-compose up -d
    echo ✓ PostgreSQL started on port 5432
    echo ✓ pgAdmin available at http://localhost:5050
    timeout /t 3
) else (
    echo [!] Docker not found. Make sure PostgreSQL is running locally.
)

echo.
echo [2] Setting up Backend...
cd server
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ⚠ Please update .env with your database credentials
)

echo Initializing database...
python database/init_db.py

echo.
echo [3] Starting FastAPI Server...
echo ✓ API will be available at http://localhost:8000
echo ✓ API Docs at http://localhost:8000/docs
python main.py
