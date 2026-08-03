import os
import sys

# Prepend parent directory to sys.path to allow imports from app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()
