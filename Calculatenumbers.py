"""
Compatibility wrapper for tests.
Re-exports symbols from features.utilities.Calculatenumbers so that
`import Calculatenumbers` works from the project root.
"""

from features.utilities.Calculatenumbers import *  # noqa: F401,F403
