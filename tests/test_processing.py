"""
This module contains unit tests for the image processing and translation functionality.
"""

import unittest
from PIL import Image, ImageDraw, ImageFont
from src.core import processing
import asyncio

class TestImageProcessing(unittest.TestCase):
    """
    Tests the image processing and translation functionality.
    """

    def test_process_russian_image_to_english(self):
        """
        Tests if an image with Russian text is correctly OCRed and translated to English.
        """
        async def run_test():
            image = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
            draw.text((10, 10), "Привет Мир", fill='black', font=font)

            translated_text = await processing.process_image_and_translate(image, target_language='en')
            self.assertIsNotNone(translated_text, "Should return a translation.")
            self.assertNotEqual(translated_text.strip(), "", "Translated text should not be empty.")
            # We can't assert the exact translation as it might vary slightly.

        asyncio.run(run_test())

    def test_process_english_image_to_russian(self):
        """
        Tests if an image with English text is correctly OCRed and translated to Russian.
        """
        async def run_test():
            image = Image.new('RGB', (150, 30), color='white')
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except IOError:
                font = ImageFont.load_default()
            draw.text((10, 10), "Hello World", fill='black', font=font)

            translated_text = await processing.process_image_and_translate(image, target_language='ru')
            self.assertIsNotNone(translated_text, "Should return a translation.")
            self.assertNotEqual(translated_text.strip(), "", "Translated text should not be empty.")

        asyncio.run(run_test())

    def test_process_image_with_no_text(self):
        """
        Tests if an image with no text results in an empty translation.
        """
        async def run_test():
            image = Image.new('RGB', (100, 30), color='white')
            translated_text = await processing.process_image_and_translate(image)
            self.assertEqual(translated_text, "", "Should return an empty string for an image with no text.")

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()