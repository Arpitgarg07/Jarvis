#!/usr/bin/env python3
"""
Jarvis - Just A Rather Very Intelligent System
Main entry point for the voice assistant
"""

import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main Jarvis application
from core.Jarvismain import *

if __name__ == "__main__":
    print("Starting Jarvis...")
    # The main execution is already handled in Jarvismain.py
