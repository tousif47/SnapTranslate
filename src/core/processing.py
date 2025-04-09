# src/core/processing.py

"""
This module contains the core logic for processing images, including performing
Optical Character Recognition (OCR) and translating the extracted text.
"""

from PIL import Image
from . import ocr
from . import translator

import asyncio

async def process_image_and_translate(image: Image.Image, target_language: str = 'en', source_language: str = None) -> str:
    """
    Performs OCR on the input image to extract text and then translates
    the extracted text to the specified target language.

    Args:
        image: A PIL Image object representing the image to process.
        target_language: The ISO 639-1 code of the target language for translation.
                         Defaults to 'en' (English).
        source_language: The ISO 639-1 code of the source language.
                         Defaults to None, allowing the translator to potentially auto-detect the language.

    Returns:
        A string containing the translated text. Returns "No text found in the image." if
        no text is extracted. Returns an empty string if translation fails.
    """

    extracted_text = ocr.extract_text_from_image(image, language=source_language)

    if not extracted_text:
        return "No text found in the image."
    else:
        translated_text = await translator.translate_text(extracted_text, dest_lang=target_language, src_lang=source_language)

        return translated_text
    # This return statement seems redundant as the 'if' condition covers all cases.
    # If no text, it returns "No text found...". If text, it returns translated text.
    # If translation fails in translator.py, it returns an error message.
    # So, this line might not be necessary. But it's good practice to have it.

    return ""

if __name__ == '__main__':

    async def main():
        # This block will only run if this script is executed directly (not imported)
        # It serves as an example of how to use the process_image_and_translate function

        from PIL import ImageDraw, ImageFont

        # Create a new white RGB image with a size of 200x50 pixels
        img = Image.new('RGB', (200, 50), color=(255, 255, 255))

        # Create a drawing object to draw on the image
        d = ImageDraw.Draw(img)

        # Try to load an Arial font, if not found, use a default font
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
            
        # Draw the Russian text "Привет Мир" (Hello World) on the image in black color
        d.text((10, 10), "Привет Мир", fill=(0, 0, 0), font=font)

        # Call the process_image_and_translate function to translate the Russian text to English
        translated_english = await process_image_and_translate(img, target_language='en', source_language='ru')
        print(f"Translated to English: '{translated_english}'")

    # Run the main asynchronous function using asyncio
    asyncio.run(main())