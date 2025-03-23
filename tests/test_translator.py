# tests/test_translator.py

"""
Unit tests for the TextTranslator class.

Tests cover:
- Successful translations
- Language auto-detection
- Error handling for invalid inputs
- Language detection confidence
"""


import pytest

from src.core.translator import TextTranslator, TranslationException


def test_translate_text_success():
    """Test successful translation of text from English to Spanish."""

    translator = TextTranslator()
    result = translator.translate_text("Hello", dest_lang="es")

    # Verify translated text and target language
    assert result.text == "Hola"
    assert result.dest == "es"


def test_translate_text_auto_detect():
    """Test translation with automatic source language detection (French to English)."""

    translator = TextTranslator()
    result = translator.translate_text("Bonjour", src_lang="auto", dest_lang="en")

    # Verify translation and auto-detected source language
    assert result.text == "Hello"
    assert result.dest == "fr"


def test_translate_invalid_language():
    """Test that invalid target language raise TranslationException"""

    translator = TextTranslator()

    with pytest.raises(TranslationException):
        # Attempt translation with invalid language code
        translator.translate_text("Hello", dest_lang="invalid_lang_code")


def test_detect_language():
    """Test language detection accuracy for Spanish text."""

    translator = TextTranslator()
    lang, confidence = translator.detect_language("Hola")

    # Verify detected language and confidence score
    assert lang == "es"
    assert confidence > 0.5 # Confidence should be reasonably high


def test_detect_language_empty_text():
    """Test that empty text input raises TranslationException during detection."""

    translator = TextTranslator()

    with pytest.raises(TranslationException):
        # Attempt detection with empty string
        translator.detect_language("")