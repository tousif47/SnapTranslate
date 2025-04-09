# tests/test_translator.py

"""
This module contains unit tests for the translation functionality in the src.core.translator module (async).
It uses the unittest framework to verify the text translation.
"""

import unittest
import asyncio

from src.core import translator

class TestTranslator(unittest.TestCase):
    """
    Test suite for the translation functionality in the translator module (async).
    """

    def test_translate_russian_to_english(self):
        """
        Tests if the function correctly translates Russian text to English (async).
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            russian_text = "Это тест."
            expected_english_translation = "This is a test."
            actual_english_translation = await translator.translate_text(russian_text, src_lang='ru', dest_lang='en')

            # Assert that the actual translation, converted to lowercase, is equal to the expected translation (lowercase)
            self.assertEqual(actual_english_translation.lower(), expected_english_translation.lower(), "Should translate Russian to English correctly.")
        
        asyncio.run(run_test())

    def test_translate_english_to_russian(self):
        """
        Tests if the function correctly translates English text to Russian (async).
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            english_text = "Hello."
            expected_russian_translation = "Привет."
            actual_russian_translation = await translator.translate_text(english_text, src_lang='en', dest_lang='ru')

            # Assert that the actual translation, converted to lowercase, is equal to the expected translation (lowercase)
            self.assertEqual(actual_russian_translation.lower(), expected_russian_translation.lower(), "Should translate English to Russian correctly.")

        asyncio.run(run_test())

    def test_translate_empty_string(self):
        """
        Tests if the function returns an empty string when given an empty string as input (async).
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            # Define an empty string as input
            empty_text = ""
            translated_text = await translator.translate_text(empty_text)

            # Assert that the returned translation is an empty string
            self.assertEqual(translated_text, "", "Should return an empty string for an empty input.")
        
        asyncio.run(run_test())

    def test_translate_whitespace_string(self):
        """
        Tests if the function returns an empty string when given a string with only whitespace (async).
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            # Define a string containing only whitespace as input
            whitespace_text = "   "
            translated_text = await translator.translate_text(whitespace_text)

            # Assert that the returned translation is an empty string
            self.assertEqual(translated_text, "", "Should return an empty string for whitespace input.")
        
        asyncio.run(run_test())

    def test_translate_with_different_language_pair(self):  # Just for texting, not used in app
        """
        Tests if the function can translate between other language pairs (e.g., English to Spanish) (async).
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            english_text = "Thank you."
            # Define the expected Spanish translation (approximate)
            expected_spanish_translation = "Gracias."
            # Call the translate_text function with English as source and Spanish as destination
            actual_spanish_translation = await translator.translate_text(english_text, src_lang='en', dest_lang='es')
            # Assert that the actual translation, converted to lowercase, is equal to the expected translation (lowercase)
            self.assertEqual(actual_spanish_translation.lower(), expected_spanish_translation.lower(), "Should translate English to Spanish correctly.")
        
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()