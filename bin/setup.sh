#!/bin/bash

set -e

echo "****************************************"
echo " Setting up Capstone Environment"
echo "****************************************"

# Check Python 3.14
echo "Checking Python version..."

if command -v python3.14 >/dev/null 2>&1; then
    PYTHON=python3.14
elif command -v python >/dev/null 2>&1 && python --version | grep -q "3.14"; then
    PYTHON=python
else
    echo "ERROR: Python 3.14 is not installed."
    exit 1
fi

$PYTHON --version

# Create virtual environment
echo "Creating Python virtual environment..."

$PYTHON -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip and wheel..."

python -m pip install --upgrade pip wheel setuptools

# Install dependencies
echo "Installing Python dependencies..."

python -m pip install -r requirements.txt

# Optional PostgreSQL Docker setup
if [ "${START_DATABASE:-0}" = "1" ]; then
    echo "Starting PostgreSQL Docker container..."
    make db
    docker ps
else
    echo "Skipping PostgreSQL Docker setup."
    echo "Set START_DATABASE=1 to enable it."
fi

echo "****************************************"
echo " Capstone Environment Setup Complete"
echo "****************************************"

echo ""
echo "Activate environment using:"
echo "source .venv/bin/activate"
echo ""
