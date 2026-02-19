#!/bin/bash
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment."
fi

source venv/bin/activate
pip install --upgrade pip
pip install chromadb requests
echo "Setup complete. Virtual environment is ready."
