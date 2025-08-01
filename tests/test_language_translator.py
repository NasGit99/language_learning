import unittest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the 'src' directory to the sys.path to make all modules inside it accessible.
## This will be changed later to import from github
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/language_modifier/')))

from src.language_modifier.language_translator import translate_text

class TestTranslateText(unittest.IsolatedAsyncioTestCase):
    async def test_translate(self):
        result = await(translate_text('Hi','French'))
        self.assertTrue(result)

    async def test_bad_translate(self):
        with self.assertRaises(ValueError):
            await translate_text('Hi', 'BadFrench')

if __name__ == '__main__':
    unittest.main()
