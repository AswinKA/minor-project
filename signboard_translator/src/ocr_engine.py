"""
OCR Engine Module

This module handles text extraction from images using Tesseract OCR.
It provides:
- Text recognition from preprocessed images
- Confidence scoring for recognized text
- Support for multiple languages
- Text region detection
"""

import cv2
import numpy as np
import pytesseract
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class OCRResult:
    """Container for OCR recognition results."""
    text: str
    confidence: float
    language: Optional[str] = None
    bounding_boxes: Optional[List[Dict]] = None


class OCREngine:
    """Handles OCR operations using Tesseract."""
    
    def __init__(self, languages: List[str] = ['eng'], 
                 psm_mode: int = 3, oem_mode: int = 3):
        """
        Initialize the OCR engine.
        
        Args:
            languages: List of language codes for OCR (e.g., ['eng', 'nep'])
            psm_mode: Page Segmentation Mode (default: 3 - Fully automatic)
            oem_mode: OCR Engine Mode (default: 3 - Default, based on what's available)
        """
        self.languages = languages
        self.lang_string = '+'.join(languages)
        self.psm_mode = psm_mode
        self.oem_mode = oem_mode
        
        # Verify tesseract is available
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR not found: {e}")
    
    def extract_text(self, image: np.ndarray, 
                    lang: Optional[List[str]] = None) -> OCRResult:
        """
        Extract text from an image.
        
        Args:
            image: Input image (numpy array)
            lang: Optional language override
            
        Returns:
            OCRResult containing extracted text and confidence
        """
        lang_list = lang if lang else self.languages
        lang_str = '+'.join(lang_list)
        
        # Configure Tesseract
        config = f'--oem {self.oem_mode} --psm {self.psm_mode}'
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang=lang_str, config=config)
        
        # Get confidence data
        data = pytesseract.image_to_data(image, lang=lang_str, 
                                        output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence
        confidences = [c for c in data['conf'] if c > -1]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(
            text=text.strip(),
            confidence=avg_confidence,
            language=lang_str
        )
    
    def extract_text_with_boxes(self, image: np.ndarray,
                               lang: Optional[List[str]] = None) -> OCRResult:
        """
        Extract text with bounding box information.
        
        Args:
            image: Input image
            lang: Optional language override
            
        Returns:
            OCRResult with bounding box data
        """
        lang_list = lang if lang else self.languages
        lang_str = '+'.join(lang_list)
        
        config = f'--oem {self.oem_mode} --psm {self.psm_mode}'
        
        # Get detailed OCR data
        data = pytesseract.image_to_data(image, lang=lang_str,
                                        output_type=pytesseract.Output.DICT)
        
        # Extract text and bounding boxes
        text_parts = []
        boxes = []
        
        n_boxes = len(data['level'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > -1:  # Valid detection
                text = data['text'][i].strip()
                if text:
                    text_parts.append(text)
                    boxes.append({
                        'text': text,
                        'confidence': int(data['conf'][i]),
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
        
        full_text = ' '.join(text_parts)
        
        # Calculate average confidence
        confidences = [b['confidence'] for b in boxes]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(
            text=full_text,
            confidence=avg_confidence,
            language=lang_str,
            bounding_boxes=boxes
        )
    
    def detect_text_regions(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Detect text regions in an image using contours.
        
        Args:
            image: Input image (preferably preprocessed)
            
        Returns:
            List of cropped text region images
        """
        # Ensure image is grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Threshold to get binary image
        _, binary = cv2.threshold(gray, 0, 255, 
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter small regions
            if w > 20 and h > 10:
                # Extract region with some padding
                padding = 5
                x1 = max(0, x - padding)
                y1 = max(0, y - padding)
                x2 = min(image.shape[1], x + w + padding)
                y2 = min(image.shape[0], y + h + padding)
                
                region = image[y1:y2, x1:x2]
                text_regions.append(region)
        
        return text_regions
    
    def recognize_from_regions(self, text_regions: List[np.ndarray],
                              lang: Optional[List[str]] = None) -> str:
        """
        Recognize text from multiple detected regions.
        
        Args:
            text_regions: List of cropped text region images
            lang: Optional language override
            
        Returns:
            Combined recognized text
        """
        all_text = []
        
        for region in text_regions:
            result = self.extract_text(region, lang)
            if result.text:
                all_text.append(result.text)
        
        return '\n'.join(all_text)
    
    def set_languages(self, languages: List[str]):
        """
        Update the language configuration.
        
        Args:
            languages: New list of language codes
        """
        self.languages = languages
        self.lang_string = '+'.join(languages)
    
    def get_available_languages(self) -> List[str]:
        """
        Get list of available Tesseract languages.
        
        Returns:
            List of available language codes
        """
        try:
            langs = pytesseract.get_languages(config='')
            return langs
        except Exception:
            return self.languages


def extract_text_from_image(image_path: str, 
                           languages: List[str] = ['eng']) -> OCRResult:
    """
    Convenience function to extract text from an image file.
    
    Args:
        image_path: Path to the image file
        languages: List of language codes
        
    Returns:
        OCRResult with extracted text
    """
    import cv2
    from .image_preprocessor import ImagePreprocessor
    
    # Load and preprocess image
    preprocessor = ImagePreprocessor()
    image = preprocessor.load_image(image_path)
    processed = preprocessor.preprocess(image)
    
    # Extract text
    engine = OCREngine(languages=languages)
    return engine.extract_text(processed)


if __name__ == "__main__":
    # Example usage
    import sys
    
    print("Available Tesseract languages:")
    engine = OCREngine()
    print(engine.get_available_languages())
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = extract_text_from_image(image_path, languages=['eng', 'nep'])
        print(f"\nExtracted Text:\n{result.text}")
        print(f"\nConfidence: {result.confidence:.2f}%")
    else:
        print("\nUsage: python ocr_engine.py <image_path>")
