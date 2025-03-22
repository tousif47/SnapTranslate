# src/core/ocr.py

"""
Text detection using Tesseract OCR.
Handles image loading, text detection and error handling.
"""


import cv2
import pytesseract
import numpy as np

from typing import Tuple, List, Dict, Optional


# Configure Tesseract path (if not in system PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class OCRException(Exception):
    """Custom exception for OCR-related errors."""

    pass


def detect_text(image_path: str) -> Tuple[str, List[Dict[str, Tuple[int, int, int, int]]]]:
    """
    Detect text and their bounding boxes in an image.
    
    Args:
        image_path: Path to the input image.
        
    Returns:
        Tuple containing:
        - Combined detected text (str)
        - List of dictionaries with 'text' and 'bbox' (x, y, w, h)
        
    Raises:
        OCRException: If image loading or text detection fails.
    """

    try:
        # Load image using OpenCV
        image = cv2.imread(image_path)

        if image is None:
            raise OCRException(f"Failed to load image: {image_path}")
        
        # Convert to RGB (Tesseract expects RGB format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Use Tesseract to detect text and bounding boxes
        data = pytesseract.image_to_data(image_rgb, output_type=pytesseract.Output.DICT)

        # Extract text and bounding boxes
        combined_text = []
        boxes = []

        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 60:   # Confidence threshold
                text = data['text'][i].strip()

                if text:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    combined_text.append(text)
                    boxes.append({
                        'text': text,
                        'bbox': (x, y, x + w, y + h)
                    })
        
        return ' '.join(combined_text), boxes
    
    except pytesseract.TesseractError as e:
        raise OCRException(f"Tesseract error: {str(e)}") from e
    except Exception as e:
        raise OCRException(f"Unexpected error: {str(e)}") from e