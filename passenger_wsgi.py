import sys
import os

# Add the directory containing this script to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI application from chat_api.py
from chat_api import app
from a2wsgi import ASGIMiddleware

# Wrap the ASGI app (FastAPI) to WSGI for Phusion Passenger compatibility in cPanel
application = ASGIMiddleware(app)
