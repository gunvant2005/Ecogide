#!/usr/bin/env python
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
