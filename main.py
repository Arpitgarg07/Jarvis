#!/usr/bin/env python3
"""
Jarvis - Just A Rather Very Intelligent System
Main entry point for the voice assistant
"""

import sys
import os

# Force Python 3.11 — PyAudio and all deps are only installed there
if sys.version_info[:2] != (3, 11):
    import subprocess
    py311 = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs", "Python", "Python311", "python.exe"
    )
    if os.path.exists(py311):
        result = subprocess.run([py311] + sys.argv)
        sys.exit(result.returncode)
    else:
        print("ERROR: Python 3.11 not found. Please run: py -3.11 main.py")
        sys.exit(1)

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from core.Jarvismain import run

if __name__ == "__main__":
    run()