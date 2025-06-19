#!/bin/bash

#Project directory
PROJECT_DIR="."

# Enter venv inside the project directory
source "$PROJECT_DIR/venv/bin/activate"

# Run the Python script
python3 "$PROJECT_DIR/main.py"