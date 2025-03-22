# tests/test_ocr.py

import pytest
import os

from src.core.ocr import detect_text, OCRException


def test_detect_text_valid_image():
    # Test with a sample image containing text

    test_image = os.path.join(os.path.dirname(__file__), "../data/samples/test_text.png")
    text, boxes = detect_text(test_image)

    assert isinstance(text, str)
    assert len(text) > 0
    assert isinstance(boxes, list)
    assert all('text' in box and 'bbox' in box for box in boxes)


def test_detext_text_invalid_path():
    # Test with non-existent image path

    with pytest.raises(OCRException):
        detect_text("non_existent_image.jpg")


def test_detect_text_no_text():
    # Test with an image containing no text

    test_image = os.path.join(os.path.dirname(__file__), "../data/samples/blank.png")
    text, boxes = detect_text(test_image)

    assert text == ""
    assert len(boxes) == 0