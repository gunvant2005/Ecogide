#!/usr/bin/env python
"""
Vercel serverless function for EcoGuide backend.
This allows Flask to run as a serverless function on Vercel.
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app

# Export the Flask app for Vercel
export = app
