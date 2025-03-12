import requests
import json
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.append(str(Path(__file__).parent))

# Base URL of your API
BASE_URL = 'http://localhost:5000/api'

# Test functions remain the same as before