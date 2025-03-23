# tests/test_ocr.py

"""
Unit tests for text detection functionality.

Tests cover:
- Successful text detection in valid images
- Error handling for invalid file paths
- Graceful handling of images without text
"""


import pytest
import os

from src.core.ocr import detect_text, OCRException


def test_detect_text_valid_image():
    """Test text detection in an image containing readable text.
    
    Verifies:
    - Returns non-empty string for detected text
    - Returns list of bounding boxes with valid structure
    - Each box contains 'text' and 'bbox' keys
    """

    # Arrange: Get path to test image with text
    test_image = os.path.join(os.path.dirname(__file__), "../data/samples/test_text.jpg")
    
    # Act: Perform text detection
    text, boxes = detect_text(test_image)
    
    # Assert: Validate results
    assert isinstance(text, str), "Detected text should be a string"
    assert len(text) > 0, "Should detect non-empty text in valid image"
    assert isinstance(boxes, list), "Bounding boxes should be in a list"
    assert all('text' in box and 'bbox' in box for box in boxes), ("Each box should contain text and coordinates")


def test_detect_text_invalid_path():
    """Test error handling for non-existent image paths.
    
    Verifies:
    - Proper OCRException is raised
    - Error message indicates failure to load image
    """

    # Arrange & Act/Assert: Check exception for invalid path
    with pytest.raises(OCRException) as exc_info:
        detect_text("non_existent_image.jpg")
    
    # Optional: Verify exception message content
    assert "Failed to load image" in str(exc_info.value)


def test_detect_text_no_text():
    """Test handling of images without readable text.
    
    Verifies:
    - Returns empty string for detected text
    - Returns empty list for bounding boxes
    - No exceptions raised for valid image without text
    """

    # Arrange: Get path to blank test image
    test_image = os.path.join(os.path.dirname(__file__), "../data/samples/blank.jpg")
    
    # Act: Perform text detection
    text, boxes = detect_text(test_image)
    
    # Assert: Validate empty results
    assert text == "", "Should return empty text for image without text"
    assert len(boxes) == 0, "Should return no boxes for image without text"