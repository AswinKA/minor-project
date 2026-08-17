"""
Test Suite for AI-based Signboard Reader and Translator

This module contains unit tests for all components:
- Image Preprocessor
- OCR Engine
- Language Detector
- Text Translator
- Signboard Reader Pipeline
"""

import unittest
import numpy as np
import cv2
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.image_preprocessor import ImagePreprocessor
from src.ocr_engine import OCREngine, OCRResult
from src.translator import LanguageDetector, TextTranslator, SignboardTranslator


class TestImagePreprocessor(unittest.TestCase):
    """Tests for the ImagePreprocessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = ImagePreprocessor(target_width=512)
        # Create a simple test image with text-like patterns
        self.test_image = np.ones((200, 400, 3), dtype=np.uint8) * 255
        # Add some dark rectangles to simulate text
        cv2.rectangle(self.test_image, (50, 50), (150, 80), (0, 0, 0), -1)
        cv2.rectangle(self.test_image, (200, 100), (350, 130), (0, 0, 0), -1)
    
    def test_load_image(self):
        """Test image loading functionality."""
        # Create a temporary test image
        test_path = '/tmp/test_image.jpg'
        cv2.imwrite(test_path, self.test_image)
        
        loaded = self.preprocessor.load_image(test_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.shape[:2], self.test_image.shape[:2])
        
        # Clean up
        os.remove(test_path)
    
    def test_convert_to_grayscale(self):
        """Test grayscale conversion."""
        gray = self.preprocessor.convert_to_grayscale(self.test_image)
        self.assertEqual(len(gray.shape), 2)
        self.assertEqual(gray.shape, self.test_image.shape[:2])
    
    def test_remove_noise(self):
        """Test noise removal."""
        noisy = self.test_image.copy()
        # Add salt-and-pepper noise
        noise = np.random.randint(0, 255, noisy.shape, dtype=np.uint8)
        noisy = cv2.addWeighted(noisy, 0.3, noisy, 0.7, 0)
        
        denoised = self.preprocessor.remove_noise(noisy)
        self.assertEqual(denoised.shape, noisy.shape)
    
    def test_adjust_contrast(self):
        """Test contrast adjustment."""
        enhanced = self.preprocessor.adjust_contrast(self.test_image, alpha=1.5, beta=30)
        self.assertEqual(enhanced.shape, self.test_image.shape)
        # Check that contrast was actually adjusted
        self.assertNotEqual(np.mean(enhanced), np.mean(self.test_image))
    
    def test_apply_thresholding(self):
        """Test thresholding methods."""
        gray = self.preprocessor.convert_to_grayscale(self.test_image)
        
        # Test Otsu thresholding
        otsu_thresh = self.preprocessor.apply_thresholding(gray, method='otsu')
        self.assertEqual(otsu_thresh.shape, gray.shape)
        self.assertTrue(np.all((otsu_thresh == 0) | (otsu_thresh == 255)))
        
        # Test adaptive thresholding
        adaptive_thresh = self.preprocessor.apply_thresholding(gray, method='adaptive')
        self.assertEqual(adaptive_thresh.shape, gray.shape)
    
    def test_full_preprocessing_pipeline(self):
        """Test complete preprocessing pipeline."""
        processed = self.preprocessor.preprocess(self.test_image)
        self.assertIsNotNone(processed)
        self.assertEqual(len(processed.shape), 2)  # Should be grayscale


class TestOCREngine(unittest.TestCase):
    """Tests for the OCREngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.engine = OCREngine(languages=['eng'])
            self.has_tesseract = True
        except RuntimeError:
            self.has_tesseract = False
    
    def test_initialization(self):
        """Test OCR engine initialization."""
        if self.has_tesseract:
            self.assertEqual(self.engine.languages, ['eng'])
    
    def test_extract_text(self):
        """Test text extraction."""
        if not self.has_tesseract:
            self.skipTest("Tesseract not available")
        
        # Create test image with clear text pattern
        image = np.ones((100, 300, 3), dtype=np.uint8) * 255
        cv2.putText(image, 'TEST', (50, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        result = self.engine.extract_text(image)
        self.assertIsInstance(result, OCRResult)
        self.assertIsInstance(result.text, str)
        self.assertIsInstance(result.confidence, float)
    
    def test_get_available_languages(self):
        """Test getting available languages."""
        if not self.has_tesseract:
            self.skipTest("Tesseract not available")
        
        langs = self.engine.get_available_languages()
        self.assertIsInstance(langs, list)
        self.assertIn('eng', langs)


class TestLanguageDetector(unittest.TestCase):
    """Tests for the LanguageDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = LanguageDetector()
    
    def test_detect_english(self):
        """Test English language detection."""
        text = "Hello, this is a test of language detection."
        lang = self.detector.detect(text)
        self.assertEqual(lang, 'en')
    
    def test_detect_spanish(self):
        """Test Spanish language detection."""
        text = "Hola, esto es una prueba de detección de idioma."
        lang = self.detector.detect(text)
        self.assertEqual(lang, 'es')
    
    def test_detect_french(self):
        """Test French language detection."""
        text = "Bonjour, ceci est un test de détection de langue."
        lang = self.detector.detect(text)
        self.assertEqual(lang, 'fr')
    
    def test_empty_text(self):
        """Test detection with empty text."""
        lang = self.detector.detect("")
        self.assertIsNone(lang)
    
    def test_short_text(self):
        """Test detection with very short text."""
        lang = self.detector.detect("Hi")
        self.assertIsNone(lang)  # Too short for reliable detection
    
    def test_get_language_name(self):
        """Test language name lookup."""
        name = self.detector.get_language_name('en')
        self.assertEqual(name, 'English')
        
        name = self.detector.get_language_name('es')
        self.assertEqual(name, 'Spanish')
    
    def test_detect_with_probability(self):
        """Test detection with probability scores."""
        text = "This is definitely English text."
        result = self.detector.detect_with_probability(text)
        self.assertIsNotNone(result)
        self.assertIn('language', result)
        self.assertIn('probability', result)
        self.assertEqual(result['language'], 'en')


class TestTextTranslator(unittest.TestCase):
    """Tests for the TextTranslator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.translator = TextTranslator()
    
    def test_translate_to_english(self):
        """Test translation to English."""
        result = self.translator.translate("Hola mundo", dest_lang='en')
        self.assertTrue(result['success'])
        self.assertIn('world', result['translated_text'].lower())
    
    def test_translate_from_nepali(self):
        """Test translation from Nepali."""
        # Note: This may fail without internet connection
        result = self.translator.translate("नमस्ते", dest_lang='en', src_lang='ne')
        # Just check that it returns a result structure
        self.assertIn('original_text', result)
        self.assertIn('translated_text', result)
    
    def test_empty_text_translation(self):
        """Test translation with empty text."""
        result = self.translator.translate("", dest_lang='en')
        self.assertFalse(result['success'])
        self.assertEqual(result['translated_text'], '')
    
    def test_get_supported_languages(self):
        """Test getting supported languages."""
        langs = self.translator.get_supported_languages()
        self.assertIsInstance(langs, dict)
        self.assertGreater(len(langs), 10)


class TestSignboardTranslator(unittest.TestCase):
    """Tests for the integrated SignboardTranslator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.translator = SignboardTranslator(default_target_language='en')
    
    def test_process_english_text(self):
        """Test processing English text."""
        text = "Welcome to our store"
        result = self.translator.process_text(text, target_language='en')
        
        self.assertEqual(result['detected_language'], 'en')
        self.assertTrue(result['translation_success'])
    
    def test_process_spanish_text(self):
        """Test processing Spanish text."""
        text = "Bienvenido a nuestra tienda"
        result = self.translator.process_text(text, target_language='en')
        
        self.assertEqual(result['detected_language'], 'es')
        self.assertTrue(result['translation_success'])
    
    def test_set_target_language(self):
        """Test changing target language."""
        self.translator.set_default_target_language('fr')
        self.assertEqual(self.translator.default_target_language, 'fr')


def run_tests():
    """Run all tests and print summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestImagePreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestOCREngine))
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestTextTranslator))
    suite.addTests(loader.loadTestsFromTestCase(TestSignboardTranslator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*60)
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
