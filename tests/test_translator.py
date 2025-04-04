"""
This module contains unit tests for the translation functionality in the src.core.translator module (async).
It uses the unittest framework to verify the text translation.
"""

import unittest
from src.core import translator
import asyncio

class TestTranslator(unittest.TestCase):
    """
    Test suite for the translation functionality in the translator module (async).
    """

    def test_translate_russian_to_english(self):
        """
        Tests if the function correctly translates Russian text to English (async).
        """
        async def run_test():
            russian_text = "Это тест."
            expected_english_translation = "This is a test." # Approximate translation
            actual_english_translation = await translator.translate_text(russian_text, src_lang='ru', dest_lang='en')
            self.assertEqual(actual_english_translation.lower(), expected_english_translation.lower(), "Should translate Russian to English correctly.")
        asyncio.run(run_test())

    def test_translate_english_to_russian(self):
        """
        Tests if the function correctly translates English text to Russian (async).
        """
        async def run_test():
            english_text = "Hello."
            expected_russian_translation = "Привет." # Approximate translation
            actual_russian_translation = await translator.translate_text(english_text, src_lang='en', dest_lang='ru')
            self.assertEqual(actual_russian_translation.lower(), expected_russian_translation.lower(), "Should translate English to Russian correctly.")
        asyncio.run(run_test())

    def test_translate_empty_string(self):
        """
        Tests if the function returns an empty string when given an empty string as input (async).
        """
        async def run_test():
            empty_text = ""
            translated_text = await translator.translate_text(empty_text)
            self.assertEqual(translated_text, "", "Should return an empty string for an empty input.")
        asyncio.run(run_test())

    def test_translate_whitespace_string(self):
        """
        Tests if the function returns an empty string when given a string with only whitespace (async).
        """
        async def run_test():
            whitespace_text = "   "
            translated_text = await translator.translate_text(whitespace_text)
            self.assertEqual(translated_text, "", "Should return an empty string for whitespace input.")
        asyncio.run(run_test())

    def test_translate_with_different_language_pair(self):
        """
        Tests if the function can translate between other language pairs (e.g., English to Spanish) (async).
        """
        async def run_test():
            english_text = "Thank you."
            expected_spanish_translation = "Gracias." # Approximate translation
            actual_spanish_translation = await translator.translate_text(english_text, src_lang='en', dest_lang='es')
            self.assertEqual(actual_spanish_translation.lower(), expected_spanish_translation.lower(), "Should translate English to Spanish correctly.")
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()