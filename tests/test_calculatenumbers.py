"""
Test cases for Calculatenumbers module
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from Calculatenumbers import Calc, WolfRamAlpha
except ImportError:
    # Skip tests if dependencies are not available
    import pytest

    pytest.skip(
        "Calculatenumbers module dependencies not available", allow_module_level=True
    )


class TestCalculatenumbers(unittest.TestCase):
    """Test cases for calculator functionality"""

    @patch("Calculatenumbers.WolfRamAlpha")
    @patch("Calculatenumbers.Speak")
    def test_calc_basic_operations(self, mock_speak, mock_wolfram):
        """Test basic calculation operations"""
        # Mock WolfRamAlpha to return a result
        mock_wolfram.return_value = "42"

        # Test the Calc function
        Calc("jarvis what is 2 plus 2")

        # Verify WolfRamAlpha was called
        mock_wolfram.assert_called_once()
        # Verify Speak was called with the result
        mock_speak.assert_called_with("42")

    @patch("Calculatenumbers.WolfRamAlpha")
    @patch("Calculatenumbers.Speak")
    def test_calc_term_replacement(self, mock_speak, mock_wolfram):
        """Test that mathematical terms are correctly replaced"""
        mock_wolfram.return_value = "10"

        # Test various term replacements
        Calc("jarvis multiply 2 plus 3")

        # Get the call arguments to WolfRamAlpha
        call_args = mock_wolfram.call_args[0][0]

        # Verify that terms were replaced correctly
        self.assertNotIn("jarvis", call_args)
        self.assertNotIn("multiply", call_args)
        self.assertNotIn("plus", call_args)

    @patch("Calculatenumbers.wolframalpha.Client")
    def test_wolfram_alpha_success(self, mock_client):
        """Test successful WolfRamAlpha query"""
        # Mock the client and result
        mock_result = MagicMock()
        mock_result.text = "42"
        mock_client.return_value.query.return_value.results = iter([mock_result])

        result = WolfRamAlpha("2+2")
        self.assertEqual(result, "42")

    @patch("Calculatenumbers.wolframalpha.Client")
    @patch("Calculatenumbers.Speak")
    def test_wolfram_alpha_failure(self, mock_speak, mock_client):
        """Test WolfRamAlpha query failure"""
        # Mock the client to raise an exception
        mock_client.return_value.query.side_effect = Exception("API Error")

        result = WolfRamAlpha("invalid query")
        self.assertIsNone(result)
        mock_speak.assert_called_with("The value is not answerable")


if __name__ == "__main__":
    unittest.main()
