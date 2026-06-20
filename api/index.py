"""
Vercel serverless function handler for EcoGuide Flask app.
This file serves as the entry point for Vercel's serverless environment.
"""
import sys
import os

# Ensure the backend module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app

# Export the app as a handler for Vercel
handler = app

# For direct invocation
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
