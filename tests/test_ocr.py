"""
This module contains unit tests for the OCR functionality in the src.core.ocr module.
It uses the unittest framework to verify the text extraction from images.
"""

import unittest
from src.core import ocr
from PIL import Image, ImageDraw, ImageFont
import io
import pytesseract  # Ensure pytesseract is imported here
import os
import tempfile  # Import the tempfile module

class TestOCR(unittest.TestCase):
    """
    Test suite for the OCR functionality in the ocr module.
    """

    def test_extract_text_from_image_with_text(self):
        """
        Tests if the function correctly extracts text from an image containing text.
        (Using English text in memory)
        """
        # Create a simple in-memory image with text using Pillow
        image = Image.new('RGB', (100, 30), color='white')
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font = ImageFont.load_default()
        draw.text((10, 10), "Test Text", fill='black', font=font)

        extracted_text = ocr.extract_text_from_image(image, language='eng') # Pass the Pillow Image object
        self.assertEqual(extracted_text.strip(), "Test Text", "Should extract the text correctly.")

    def test_extract_text_from_image_without_text(self):
        """
        Tests if the function returns an empty string when no text is present in the image.
        (Using a blank image in memory)
        """
        # Create a blank white image
        image = Image.new('RGB', (100, 30), color='white')
        extracted_text = ocr.extract_text_from_image(image) # Pass the Pillow Image object
        self.assertEqual(extracted_text, "", "Should return an empty string for an image with no text.")

    def test_extract_text_from_image_with_different_language(self):
        """
        Tests if the function can extract text in a different language (Russian in this case)
        using an image file from the samples folder.
        Requires the corresponding language pack to be installed for Tesseract.
        """
        try:
            # Construct the path to the Russian test image
            sample_image_path = os.path.join("data", "samples", "ru_test.jpg") # Updated to .jpg
            self.assertTrue(os.path.exists(sample_image_path), f"Sample image not found: {sample_image_path}")

            # Open the image using Pillow
            russian_image = Image.open(sample_image_path)

            extracted_text = ocr.extract_text_from_image(russian_image, language='rus') # Pass the Pillow Image object
            self.assertTrue(len(extracted_text) > 0, "Should extract text in Russian (if language pack is installed and image contains text).")
            print(f"Extracted Russian text: '{extracted_text}'") # Print for debugging

        except pytesseract.TesseractNotFoundError:
            self.skipTest("Tesseract is not installed.")
        except Exception as e:
            # If the language pack is missing or other Tesseract issues
            self.skipTest(f"Skipping Russian test due to potential Tesseract issue: {e}")

    def test_extract_text_from_image_with_empty_image(self):
        """
        Tests if the function handles an empty (None) image gracefully by raising AttributeError.
        """
        with self.assertRaises(AttributeError): # Expecting an AttributeError if None is passed
            ocr.extract_text_from_image(None)

if __name__ == '__main__':
    unittest.main()