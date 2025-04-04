"""
This module contains the functionality for translating text using the googletrans library (async).
"""

from googletrans import Translator
import logging
import asyncio

# Configure logging to display any potential errors or warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def translate_text(text: str, src_lang: str = 'ru', dest_lang: str = 'en') -> str:
    """
    Translates the given text from the source language to the destination language
    using the Google Translate API via the googletrans library (async).

    Args:
        text: The string of text to be translated.
        src_lang: The ISO 639-1 code of the source language (e.g., 'ru' for Russian).
                  Defaults to 'ru'.
        dest_lang: The ISO 639-1 code of the destination language (e.g., 'en' for English).
                   Defaults to 'en'.

    Returns:
        A string containing the translated text. Returns an empty string if the input
        text is empty or if an error occurs during translation.
    """
    if not text.strip():
        return ""

    async with Translator() as translator:
        try:
            translation = await translator.translate(text, src=src_lang, dest=dest_lang)
            return translation.text
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return ""

if __name__ == '__main__':
    # Example usage (this will run only if this script is executed directly)
    async def main():
        russian_text = "Привет мир"
        english_translation = await translate_text(russian_text, src_lang='ru', dest_lang='en')
        print(f"Original Russian text: '{russian_text}'")
        print(f"Translated English text: '{english_translation}'")

        english_text = "Hello world"
        russian_translation = await translate_text(english_text, src_lang='en', dest_lang='ru')
        print(f"\nOriginal English text: '{english_text}'")
        print(f"Translated Russian text: '{russian_translation}'")

    asyncio.run(main())