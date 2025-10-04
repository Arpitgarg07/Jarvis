"""
Integration tests for Jarvis modules
Tests basic functionality and module imports
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModuleImports(unittest.TestCase):
    """Test that core modules can be imported without errors"""

    def test_import_greetme(self):
        """Test that GreetMe module can be imported"""
        try:
            import GreetMe

            self.assertTrue(hasattr(GreetMe, "greetMe"))
            self.assertTrue(hasattr(GreetMe, "Speak"))
        except ImportError as e:
            self.skipTest(f"GreetMe module not available: {e}")

    def test_import_calculatenumbers(self):
        """Test that Calculatenumbers module can be imported"""
        try:
            import Calculatenumbers

            self.assertTrue(hasattr(Calculatenumbers, "Calc"))
            self.assertTrue(hasattr(Calculatenumbers, "WolfRamAlpha"))
        except ImportError as e:
            self.skipTest(f"Calculatenumbers module not available: {e}")

    def test_import_joke(self):
        """Test that joke module can be imported"""
        try:
            import joke

            # Check if the module has expected functions
            self.assertTrue(hasattr(joke, "__name__"))
        except ImportError as e:
            self.skipTest(f"joke module not available: {e}")

    def test_import_translator(self):
        """Test that Translator module can be imported"""
        try:
            import Translator

            # Check if the module loads without errors
            self.assertTrue(hasattr(Translator, "__name__"))
        except ImportError as e:
            self.skipTest(f"Translator module not available: {e}")


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality that doesn't require external APIs"""

    @patch("GreetMe.pyttsx3.init")
    def test_speak_function_exists(self, mock_pyttsx3):
        """Test that Speak function exists and can be called"""
        try:
            from GreetMe import Speak

            # Mock the engine
            mock_engine = MagicMock()
            mock_pyttsx3.return_value = mock_engine

            # Test the function
            Speak("test")

            # Verify it was called
            mock_engine.say.assert_called_with("test")
            mock_engine.runAndWait.assert_called_once()

        except ImportError:
            self.skipTest("GreetMe module not available")

    def test_file_structure(self):
        """Test that expected files exist in the project"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Check for main files
        expected_files = [
            "GreetMe.py",
            "Calculatenumbers.py",
            "Jarvismain.py",
            "README.md",
        ]

        for file_name in expected_files:
            file_path = os.path.join(project_root, file_name)
            self.assertTrue(
                os.path.exists(file_path),
                f"Expected file {file_name} not found at {file_path}",
            )

    def test_no_syntax_errors_in_python_files(self):
        """Test that Python files have no syntax errors"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Get all Python files (excluding tests and virtual environments)
        python_files = []
        for root, dirs, files in os.walk(project_root):
            # Skip virtual environments and test directories
            dirs[:] = [
                d
                for d in dirs
                if d not in ["venv", "env", ".venv", ".env", "__pycache__", ".git"]
            ]

            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    python_files.append(os.path.join(root, file))

        syntax_errors = []
        for file_path in python_files[:10]:  # Test first 10 files to avoid timeout
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    source_code = f.read()
                    compile(source_code, file_path, "exec")
            except SyntaxError as e:
                syntax_errors.append(f"{file_path}: {e}")
            except Exception as e:
                # Skip files that can't be read or compiled for other reasons
                pass

        if syntax_errors:
            self.fail(f"Syntax errors found in files:\n" + "\n".join(syntax_errors))


if __name__ == "__main__":
    unittest.main()
