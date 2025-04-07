"""
This module integrates OCR and translation functionalities.
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
        image: A PIL Image object.
        target_language: The ISO 639-1 code of the target language for translation.
                         Defaults to 'en' (English).
        source_language: The ISO 639-1 code of the source language.
                         Defaults to None.

    Returns:
        A string containing the translated text. Returns an empty string if
        no text is extracted or if translation fails.
    """
    extracted_text = ocr.extract_text_from_image(image, language=source_language)
    if extracted_text:
        translated_text = await translator.translate_text(extracted_text, dest_lang=target_language, src_lang=source_language)
        return translated_text
    return ""

if __name__ == '__main__':
    async def main():
        # Example usage: Create a dummy image with Russian text
        from PIL import ImageDraw, ImageFont
        img = Image.new('RGB', (200, 50), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        d.text((10, 10), "Привет Мир", fill=(0, 0, 0), font=font)

        translated_english = await process_image_and_translate(img, target_language='en')
        print(f"Translated to English: '{translated_english}'")

        translated_spanish = await process_image_and_translate(img, target_language='es')
        print(f"Translated to Spanish: '{translated_spanish}'")

    asyncio.run(main())