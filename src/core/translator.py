# src/core/translator.py

"""
This module contains the functionality for translating text using the googletrans library (async).
"""

from googletrans import Translator

import logging
import asyncio
import requests
import httpx

# Configure logging to display any potential errors or warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def translate_text(text: str, src_lang: str = 'ru', dest_lang: str = 'en') -> str:
    """
    Translates the given text from the source language to the destination language
    using the Google Translate API via the googletrans library (async).

    Args:
        text: The string of text to be translated.
        src_lang: The ISO 639-1 code of the source language (e.g., 'ru' for Russian).
                    Defaults to 'ru' (Russian).
        dest_lang: The ISO 639-1 code of the destination language (e.g., 'en' for English).
                    Defaults to 'en' (English).

    Returns:
        A string containing the translated text. Returns an empty string if the input
        text is empty. Returns an error message if an error occurs during translation.
    """

    # Check if the input text is empty or contains only whitespace
    if not text.strip():
        return ""

    # Create an asynchronous Translator instance to interact with the Google Translate API
    async with Translator() as translator:
        try:
            # Perform the translation asynchronously
            translation = await translator.translate(text, src=src_lang, dest=dest_lang)
            
            return translation.text

        # Catch specific httpx.ConnectError for network connection issues (like no internet)
        except httpx.ConnectError as e:
            error_message = f"Translation network error (httpx): {e}"
            logging.error(error_message)

            return "Translation Error: A network error has occurred. Please check your internet connection."

        # Catch requests.exceptions.RequestException for other potential network-related errors
        except requests.exceptions.RequestException as e:
            error_message = f"Translation network error (requests): {e}"
            logging.error(error_message)

            return "Translation Error: A network error has occurred. Please check your internet connection."

        # Catch any other unexpected exceptions that might occur during translation
        except Exception as e:
            error_message = f"An unexpected translation error occurred: {e}"
            logging.error(error_message)

            return f"Translation Error: {error_message}"

if __name__ == '__main__':
    # This block will only run if this script is executed directly (not imported)
    # It serves as an example of how to use the translate_text function

    async def main():
        # Example: Translate Russian text to English
        russian_text = "Привет мир"
        english_translation = await translate_text(russian_text, src_lang='ru', dest_lang='en')
        print(f"Original Russian text: '{russian_text}'")
        print(f"Translated English text: '{english_translation}'")

        # Example: Translate English text to Russian. Not used in app but test the API functionality.
        english_text = "Hello world"
        russian_translation = await translate_text(english_text, src_lang='en', dest_lang='ru')
        print(f"\nOriginal English text: '{english_text}'")
        print(f"Translated Russian text: '{russian_translation}'")

    asyncio.run(main())