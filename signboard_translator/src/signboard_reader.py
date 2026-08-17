"""
Signboard Reader - Main Pipeline Module

This module integrates all components of the AI-based Signboard Reader and Translator:
- Image preprocessing with OpenCV
- Text extraction with Tesseract OCR
- Language detection
- Text translation

Usage:
    from src.signboard_reader import SignboardReader
    
    reader = SignboardReader(target_language='en')
    result = reader.process_image('path/to/signboard.jpg')
    
    print(f"Original Text: {result['extracted_text']}")
    print(f"Translated Text: {result['translated_text']}")
    print(f"Detected Language: {result['detected_language']}")
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import time

from .image_preprocessor import ImagePreprocessor
from .ocr_engine import OCREngine, OCRResult
from .translator import SignboardTranslator


@dataclass
class SignboardResult:
    """Complete result from signboard processing."""
    
    # Image information
    image_path: str
    processing_time: float
    
    # OCR results
    extracted_text: str
    ocr_confidence: float
    ocr_language: str
    
    # Translation results
    translated_text: str
    detected_language: Optional[str]
    detected_language_name: str
    target_language: str
    translation_success: bool
    
    # Additional metadata
    bounding_boxes: Optional[List[Dict]] = None
    preprocessed_image: Optional[np.ndarray] = None
    error: Optional[str] = None
    
    # Full detailed results
    ocr_result: Optional[OCRResult] = None
    translation_details: Optional[Dict] = None


class SignboardReader:
    """
    Main class for the AI-based Signboard Reader and Translator.
    
    This class orchestrates the complete pipeline:
    1. Load and preprocess image
    2. Extract text using OCR
    3. Detect language
    4. Translate text
    """
    
    def __init__(self, 
                 target_language: str = 'en',
                 ocr_languages: Optional[List[str]] = None,
                 enable_preprocessing: bool = True,
                 verbose: bool = False):
        """
        Initialize the Signboard Reader.
        
        Args:
            target_language: Target language for translation (default: 'en')
            ocr_languages: List of languages for OCR (default: ['eng', 'nep'])
            enable_preprocessing: Whether to enable image preprocessing
            verbose: Print detailed processing information
        """
        self.target_language = target_language
        self.enable_preprocessing = enable_preprocessing
        self.verbose = verbose
        
        # Default OCR languages - can be extended based on installed tesseract models
        if ocr_languages is None:
            ocr_languages = ['eng', 'nep']
        
        # Initialize components
        self.preprocessor = ImagePreprocessor()
        self.ocr_engine = OCREngine(languages=ocr_languages)
        self.translator = SignboardTranslator(default_target_language=target_language)
        
        self._log("SignboardReader initialized")
        self._log(f"Target language: {target_language}")
        self._log(f"OCR languages: {ocr_languages}")
    
    def process_image(self, image_path: str, 
                     custom_target_language: Optional[str] = None) -> SignboardResult:
        """
        Process a signboard image through the complete pipeline.
        
        Args:
            image_path: Path to the signboard image
            custom_target_language: Override default target language
            
        Returns:
            SignboardResult with all processing results
        """
        start_time = time.time()
        target_lang = custom_target_language or self.target_language
        
        try:
            # Step 1: Load image
            self._log(f"Loading image: {image_path}")
            original_image = self.preprocessor.load_image(image_path)
            
            # Step 2: Preprocess image
            preprocessed_image = None
            if self.enable_preprocessing:
                self._log("Preprocessing image...")
                preprocessed_image = self.preprocessor.preprocess(original_image)
                ocr_input = preprocessed_image
            else:
                ocr_input = original_image
            
            # Step 3: Extract text using OCR
            self._log("Extracting text with OCR...")
            ocr_result = self.ocr_engine.extract_text_with_boxes(ocr_input)
            
            self._log(f"OCR Confidence: {ocr_result.confidence:.2f}%")
            self._log(f"Extracted text length: {len(ocr_result.text)} characters")
            
            # Step 4: Detect language and translate
            detected_language = None
            detected_language_name = "Unknown"
            translated_text = ""
            translation_success = False
            translation_details = None
            
            if ocr_result.text.strip():
                self._log("Detecting language and translating...")
                
                # Process text through translator
                translation_details = self.translator.process_text(
                    ocr_result.text,
                    target_language=target_lang
                )
                
                detected_language = translation_details['detected_language']
                detected_language_name = translation_details['detected_language_name']
                translated_text = translation_details['translated_text']
                translation_success = translation_details['translation_success']
                
                self._log(f"Detected language: {detected_language_name}")
                self._log(f"Translation success: {translation_success}")
            else:
                self._log("No text detected in image")
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create result object
            result = SignboardResult(
                image_path=image_path,
                processing_time=processing_time,
                extracted_text=ocr_result.text,
                ocr_confidence=ocr_result.confidence,
                ocr_language=ocr_result.language or str(self.ocr_engine.languages),
                translated_text=translated_text,
                detected_language=detected_language,
                detected_language_name=detected_language_name,
                target_language=target_lang,
                translation_success=translation_success,
                bounding_boxes=ocr_result.bounding_boxes,
                preprocessed_image=preprocessed_image,
                ocr_result=ocr_result,
                translation_details=translation_details
            )
            
            self._log(f"Processing completed in {processing_time:.2f} seconds")
            
            return result
            
        except FileNotFoundError as e:
            processing_time = time.time() - start_time
            return SignboardResult(
                image_path=image_path,
                processing_time=processing_time,
                extracted_text="",
                ocr_confidence=0.0,
                ocr_language="",
                translated_text="",
                detected_language=None,
                detected_language_name="Unknown",
                target_language=target_lang,
                translation_success=False,
                error=f"Image not found: {str(e)}"
            )
        except Exception as e:
            processing_time = time.time() - start_time
            self._log(f"Error during processing: {str(e)}")
            return SignboardResult(
                image_path=image_path,
                processing_time=processing_time,
                extracted_text="",
                ocr_confidence=0.0,
                ocr_language="",
                translated_text="",
                detected_language=None,
                detected_language_name="Unknown",
                target_language=target_lang,
                translation_success=False,
                error=str(e)
            )
    
    def process_images(self, image_paths: List[str],
                      custom_target_language: Optional[str] = None) -> List[SignboardResult]:
        """
        Process multiple signboard images.
        
        Args:
            image_paths: List of image paths
            custom_target_language: Override default target language
            
        Returns:
            List of SignboardResult objects
        """
        results = []
        for path in image_paths:
            result = self.process_image(path, custom_target_language)
            results.append(result)
        return results
    
    def get_ocr_languages(self) -> List[str]:
        """Get currently configured OCR languages."""
        return self.ocr_engine.languages
    
    def set_ocr_languages(self, languages: List[str]):
        """
        Update OCR language configuration.
        
        Args:
            languages: List of language codes
        """
        self.ocr_engine.set_languages(languages)
        self._log(f"OCR languages updated to: {languages}")
    
    def set_target_language(self, language: str):
        """
        Update target translation language.
        
        Args:
            language: Target language code
        """
        self.target_language = language
        self.translator.set_default_target_language(language)
        self._log(f"Target language updated to: {language}")
    
    def _log(self, message: str):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[SignboardReader] {message}")
    
    def print_result(self, result: SignboardResult):
        """
        Pretty print a SignboardResult.
        
        Args:
            result: Result to print
        """
        print("\n" + "="*60)
        print("SIGNBOARD READER RESULT")
        print("="*60)
        print(f"Image: {result.image_path}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print("-"*60)
        
        if result.error:
            print(f"ERROR: {result.error}")
        else:
            print(f"Extracted Text ({result.ocr_language}):")
            print(f"  {result.extracted_text}")
            print(f"\nOCR Confidence: {result.ocr_confidence:.2f}%")
            
            print(f"\nDetected Language: {result.detected_language_name} ({result.detected_language})")
            print(f"Target Language: {result.target_language}")
            
            if result.translation_success:
                print(f"\nTranslated Text:")
                print(f"  {result.translated_text}")
            else:
                print("\nTranslation failed")
        
        print("="*60 + "\n")


def read_signboard(image_path: str, target_language: str = 'en',
                  ocr_languages: Optional[List[str]] = None,
                  verbose: bool = True) -> SignboardResult:
    """
    Convenience function to process a signboard image.
    
    Args:
        image_path: Path to the signboard image
        target_language: Target language for translation
        ocr_languages: Languages for OCR
        verbose: Print processing information
        
    Returns:
        SignboardResult with processing results
    """
    reader = SignboardReader(
        target_language=target_language,
        ocr_languages=ocr_languages,
        verbose=verbose
    )
    return reader.process_image(image_path)


if __name__ == "__main__":
    import sys
    
    print("AI-based Signboard Reader and Translator")
    print("="*50)
    
    # Check available Tesseract languages
    print("\nChecking Tesseract installation...")
    try:
        engine = OCREngine()
        available_langs = engine.get_available_languages()
        print(f"Available OCR languages: {available_langs}")
    except Exception as e:
        print(f"Tesseract error: {e}")
        sys.exit(1)
    
    # Process image if provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        target_lang = sys.argv[2] if len(sys.argv) > 2 else 'en'
        
        print(f"\nProcessing: {image_path}")
        print(f"Target language: {target_lang}")
        
        result = read_signboard(image_path, target_language=target_lang)
        
        if not result.error:
            print(f"\n{'='*60}")
            print(f"EXTRACTED TEXT:\n{result.extracted_text}")
            print(f"\nDETECTED LANGUAGE: {result.detected_language_name}")
            print(f"TRANSLATED TEXT:\n{result.translated_text}")
            print(f"{'='*60}")
        else:
            print(f"Error: {result.error}")
    else:
        print("\nUsage: python signboard_reader.py <image_path> [target_language]")
        print("\nExample:")
        print("  python signboard_reader.py signboard.jpg en")
        print("  python signboard_reader.py signboard.jpg es")
