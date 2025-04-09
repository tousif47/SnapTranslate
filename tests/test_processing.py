# tests/test_processing.py

"""
This module contains unit tests for the image processing and translation functionality.
"""

import unittest
import asyncio

from PIL import Image, ImageDraw, ImageFont
from src.core import processing

class TestImageProcessing(unittest.TestCase):
    """
    Tests the image processing and translation functionality in the src.core.processing module.
    """

    def test_process_russian_image_to_english(self):
        """
        Tests if an image with Russian text is correctly OCRed and translated to English.
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            # Create a new white RGB image with a size of 200x50 pixels
            image = Image.new('RGB', (200, 50), color='white')
            # Create a drawing object to draw on the image
            draw = ImageDraw.Draw(image)

            # Try to load an Arial font, if not found, use a default font
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            # Draw the Russian text "Привет Мир" (Hello World) on the image in black color
            draw.text((10, 10), "Привет Мир", fill='black', font=font)

            # Call the process_image_and_translate function to translate the Russian text to English
            translated_text = await processing.process_image_and_translate(image, target_language='en')
            # Assert that the returned translation is not None
            self.assertIsNotNone(translated_text, "Should return a translation.")
            # Assert that the translated text is not an empty string after removing leading/trailing whitespace
            self.assertNotEqual(translated_text.strip(), "", "Translated text should not be empty.")
            # We can't assert the exact translation as it might vary slightly based on the translation service.

        # Run the asynchronous test function using asyncio
        asyncio.run(run_test())

    def test_process_english_image_to_russian(self):
        """
        Tests if an image with English text is correctly OCRed and translated to Russian.
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """

            # Create a new white RGB image with a size of 150x30 pixels
            image = Image.new('RGB', (150, 30), color='white')
            # Create a drawing object to draw on the image
            draw = ImageDraw.Draw(image)

            # Try to load an Arial font, if not found, use a default font
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                font = ImageFont.load_default()

            # Draw the English text "Hello World" on the image in black color
            draw.text((10, 10), "Hello World", fill='black', font=font)

            # Call the process_image_and_translate function to translate the English text to Russian
            translated_text = await processing.process_image_and_translate(image, target_language='ru')
            # Assert that the returned translation is not None
            self.assertIsNotNone(translated_text, "Should return a translation.")
            # Assert that the translated text is not an empty string after removing leading/trailing whitespace
            self.assertNotEqual(translated_text.strip(), "", "Translated text should not be empty.")

        # Run the asynchronous test function using asyncio
        asyncio.run(run_test())

    def test_process_image_with_no_text(self):
        """
        Tests if an image with no text results in the expected "No text found" message.
        """

        async def run_test():
            """
            Asynchronous function to execute the test.
            """
            
            # Create a new white RGB image with a size of 100x30 pixels (no text drawn)
            image = Image.new('RGB', (100, 30), color='white')
            # Call the process_image_and_translate function on an image with no text
            translated_text = await processing.process_image_and_translate(image)
            # Assert that the returned text is the expected message for no text found
            self.assertEqual(translated_text, "No text found in the image.", "Should return the 'No text found' message for an image with no text.")

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()