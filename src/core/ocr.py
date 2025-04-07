"""
This module contains the functionality for performing Optical Character Recognition (OCR)
to extract text from images using the pytesseract library.
"""

from PIL import Image
import pytesseract
import logging
import io
import os

# Explicitly set TESSDATA_PREFIX at the beginning
tessdata_dir = r'F:\Bork\Installed\Tesseract\tessdata'
os.environ['TESSDATA_PREFIX'] = tessdata_dir

# Configure logging to display any potential errors or warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_image(image: Image.Image, language: str = None) -> str:
    """
    Extracts text from a given PIL Image object using Tesseract OCR.

    Args:
        image: A PIL Image object containing the text to be extracted.
        language: The language code for OCR (e.g., 'rus' for Russian, 'eng' for English).
                         Defaults to None.

    Returns:
        A string containing the extracted text. Returns an empty string if no text is found
        or if an error occurs during OCR. Raises AttributeError if the input image is None.
    """
    if image is None:
        raise AttributeError("Input image cannot be None.")
    try:
        # Save the Pillow image to an in-memory byte stream in PNG format.
        # Tesseract often works well with PNG format.
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)   # Reset the buffer's position to the beginning

        # Open the image from the byte stream using PIL again.
        # This might help ensure the format is correctly understood by pytesseract.
        pil_image_from_bytes = Image.open(image_bytes)

        # Perform OCR using pytesseract with the newly opened PIL Image object.
        config = '--oem 3 --psm 3'
        lang_param = language
        if language == 'ru':
            lang_param = 'rus' # Using the three-letter code for Russian

        extracted_text: str = pytesseract.image_to_string(pil_image_from_bytes, lang=lang_param, config=config)
        return extracted_text.strip()   # Remove leading/trailing whitespace
    except pytesseract.TesseractNotFoundError:
        error_message = "Tesseract is not installed or not in your PATH. " \
                        "Please make sure Tesseract OCR is installed and configured correctly."
        logging.error(error_message)
        return ""
    except Exception as e:
        logging.error(f"An error occurred during OCR: {e}")
        return ""

if __name__ == '__main__':
    # Example usage (this will run only if this script is executed directly)
    try:
        # Create a dummy image with some Russian text for testing
        from PIL import ImageDraw, ImageFont
        img = Image.new('RGB', (200, 50), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            # You might need to adjust the font path to a font that supports Russian characters
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        d.text((10,10), "Привет Мир", fill=(0,0,0), font=font)

        # Save the dummy image
        img.save("temp_test_image.png")
        test_image = Image.open("temp_test_image.png")
        extracted_text = extract_text_from_image(test_image, language='rus') # Specify Russian language
        print(f"Extracted text: '{extracted_text}'")
        import os
        os.remove("temp_test_image.png") # Clean up the temporary image

    except ImportError:
        print("Pillow is not installed. Please install it to run the example.")
    except pytesseract.TesseractNotFoundError:
        print("Tesseract is not installed or not in your PATH.")