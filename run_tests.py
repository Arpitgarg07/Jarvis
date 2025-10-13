#!/usr/bin/env python3
"""
Test runner script for Jarvis project
This script runs all tests and code quality checks
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run tests and code quality checks")
    parser.add_argument(
        "--skip-install", action="store_true", help="Skip installing dependencies"
    )
    parser.add_argument(
        "--skip-format", action="store_true", help="Skip code formatting checks"
    )
    parser.add_argument("--skip-lint", action="store_true", help="Skip linting")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument(
        "--skip-security", action="store_true", help="Skip security checks"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Fix formatting issues automatically"
    )

    args = parser.parse_args()

    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    success = True

    # Install dependencies
    if not args.skip_install:
        print("Installing development dependencies...")
        if not run_command(
            "python -m pip install -r requirements-dev.txt",
            "Installing development dependencies",
        ):
            print("Warning: Failed to install some dependencies, continuing...")

    # Code formatting
    if not args.skip_format:
        if args.fix:
            run_command("black .", "Auto-formatting code with Black")
            run_command("isort . --profile black", "Auto-sorting imports with isort")
        else:
            success &= run_command(
                "black --check .", "Checking code formatting with Black"
            )
            success &= run_command(
                "isort --check-only .", "Checking import sorting with isort"
            )

    # Linting
    if not args.skip_lint:
        success &= run_command(
            "flake8 . --exclude=venv,env,.venv,.env,__pycache__ --max-line-length=127",
            "Linting with flake8",
        )

    # Type checking (optional, don't fail on this)
    if not args.skip_lint:
        run_command(
            "mypy . --ignore-missing-imports --exclude='venv|env|\\.venv|\\.env' || true",
            "Type checking with mypy (optional)",
        )

    # Security checks
    if not args.skip_security:
        run_command(
            "bandit -r . --exclude ./venv,./env,./.venv,./.env,./tests || true",
            "Security check with bandit (optional)",
        )

    # Run tests
    if not args.skip_tests:
        success &= run_command(
            "python -m pytest tests/ -v", "Running tests with pytest"
        )

    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    if success:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
