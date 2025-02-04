#!/bin/bash

# Change directory to the specified path
cd /path/to/your/project || { echo "Failed to cd to /path/to/your/project"; exit 1; }

# Activate the virtual environment
source .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Run the Python script
python test/run.py || { echo "Failed to run python test/run.py"; exit 1; }