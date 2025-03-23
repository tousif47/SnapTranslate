# src/core/translator.py

"""
Text translation using Googletrans.
Handles language detection and translation with error handling.
"""


from googletrans import Translator as GoogleTranslator
from googletrans.models import Translated
from typing import Tuple, Optional


class TranslationException(Exception):
    """Custom exception for translation-related errors."""

    pass


class TextTranslator:
    def __init__(self):
        self.translator = GoogleTranslator()
    
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the inpot text.

        Args:
            text: Input text to detect.
        
        Returns:
            TranslationException: If detection fails.
        """

        try:
            detection = self.translator.detect(text)

            return detection.lang, detection.confidence
        
        except Exception as e:
            raise TranslationException(f"Language detection failed: {str(e)}") from e
    

    def translate_text(self, text: str, src_lang: str = "auto", dest_lang: str = "en") -> Translated:
        """
        Translate text from source to destination language.
        
        Args:
            text: Text to translate.
            src_lang: Source language code (default: auto-detect).
            dest_lang: Target language code (default: English).
            
        Returns:
            Translated object with text, source/dest languages, and pronunciation.
            
        Raises:
            TranslationException: If translation fails.
        """

        try:
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)

            if not translated.text:
                raise TranslationException("Translation returned empty text.")
            
            return translated
        
        except Exception as e:
            raise TranslationException(f"Translation failed: {str(e)}") from e