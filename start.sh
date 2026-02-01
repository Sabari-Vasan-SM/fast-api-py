#!/bin/bash

# Quick Start Script for Todo App (macOS/Linux)

echo ""
echo "========================================"
echo "Todo App - Quick Start"
echo "========================================"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "[1] Starting PostgreSQL with Docker Compose..."
    docker-compose up -d
    echo "✓ PostgreSQL started on port 5432"
    echo "✓ pgAdmin available at http://localhost:5050"
    sleep 3
else
    echo "[!] Docker not found. Make sure PostgreSQL is running locally."
fi

echo ""
echo "[2] Setting up Backend..."
cd server

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠ Please update .env with your database credentials"
fi

echo "Initializing database..."
python database/init_db.py

echo ""
echo "[3] Starting FastAPI Server..."
echo "✓ API will be available at http://localhost:8000"
echo "✓ API Docs at http://localhost:8000/docs"
python main.py
