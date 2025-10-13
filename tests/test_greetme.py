"""
Test cases for GreetMe module
"""

import datetime
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from GreetMe import Speak, greetMe
except ImportError:
    # Skip tests if dependencies are not available
    import unittest

    raise unittest.SkipTest("GreetMe module dependencies not available")


class TestGreetMe(unittest.TestCase):
    """Test cases for greeting functionality"""

    @patch("GreetMe.Speak")
    @patch("GreetMe.datetime.datetime")
    def test_greet_morning(self, mock_datetime, mock_speak):
        """Test morning greeting"""
        # Mock datetime to return morning hour
        mock_datetime.now.return_value.hour = 10

        greetMe()

        # Check that the correct greeting was spoken
        calls = mock_speak.call_args_list
        self.assertTrue(any("Good Morning" in str(call) for call in calls))
        self.assertTrue(any("I am Jarvis" in str(call) for call in calls))

    @patch("GreetMe.Speak")
    @patch("GreetMe.datetime.datetime")
    def test_greet_afternoon(self, mock_datetime, mock_speak):
        """Test afternoon greeting"""
        # Mock datetime to return afternoon hour
        mock_datetime.now.return_value.hour = 15

        greetMe()

        # Check that the correct greeting was spoken
        calls = mock_speak.call_args_list
        self.assertTrue(any("Good Afternoon" in str(call) for call in calls))
        self.assertTrue(any("I am Jarvis" in str(call) for call in calls))

    @patch("GreetMe.Speak")
    @patch("GreetMe.datetime.datetime")
    def test_greet_evening(self, mock_datetime, mock_speak):
        """Test evening greeting"""
        # Mock datetime to return evening hour
        mock_datetime.now.return_value.hour = 20

        greetMe()

        # Check that the correct greeting was spoken
        calls = mock_speak.call_args_list
        self.assertTrue(any("Good Evening" in str(call) for call in calls))
        self.assertTrue(any("I am Jarvis" in str(call) for call in calls))

    @patch("GreetMe.Speak")
    @patch("GreetMe.datetime.datetime")
    def test_greet_midnight(self, mock_datetime, mock_speak):
        """Test midnight greeting (should be morning)"""
        # Mock datetime to return midnight hour
        mock_datetime.now.return_value.hour = 0

        greetMe()

        # Check that the correct greeting was spoken
        calls = mock_speak.call_args_list
        self.assertTrue(any("Good Morning" in str(call) for call in calls))

    @patch("GreetMe.pyttsx3.init")
    def test_speak_function(self, mock_pyttsx3):
        """Test the Speak function"""
        # Mock the engine
        mock_engine = MagicMock()
        mock_pyttsx3.return_value = mock_engine

        # Import and test Speak function
        from GreetMe import Speak

        Speak("Test message")

        # Verify engine methods were called
        mock_engine.say.assert_called_with("Test message")
        mock_engine.runAndWait.assert_called_once()


if __name__ == "__main__":
    unittest.main()
