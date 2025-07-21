#!/bin/bash
set -e

VENV_DIR="venv"
REQUIREMENTS="requirements.txt"

# Default to main.py if no argument is passed
PYTHON_SCRIPT="main.py"
BOOK_URL="$1"

echo "Recreating virtual environment..."

if [ -d "$VENV_DIR" ]; then
    echo "Removing existing venv..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip

if [ -f "$REQUIREMENTS" ]; then
    echo "Installing dependencies from $REQUIREMENTS..."
    pip install -r "$REQUIREMENTS"
else
    echo "$REQUIREMENTS not found."
    deactivate
    exit 1
fi

echo "Environment setup complete."
echo "Running $PYTHON_SCRIPT..."

python3 "$PYTHON_SCRIPT" "$BOOK_URL"

deactivate
