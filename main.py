#!/usr/bin/env python3
"""
Jarvis - Just A Rather Very Intelligent System
Main entry point for the voice assistant
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from core.Jarvismain import run

if __name__ == "__main__":
    run()