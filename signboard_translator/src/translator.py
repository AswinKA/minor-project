"""
Language Detection and Translation Module

This module handles:
- Automatic language detection using langdetect
- Text translation using Google Translate API
- Support for multiple languages including regional ones
"""

from typing import Optional, List, Dict
from langdetect import detect, DetectorFactory, LangDetectException
from deep_translator import GoogleTranslator
import re


# Set seed for consistent language detection results
DetectorFactory.seed = 0


class LanguageDetector:
    """Detects the language of input text."""
    
    # Common language codes supported by the system
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ne': 'Nepali',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'ta': 'Tamil',
        'te': 'Telugu',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'ur': 'Urdu',
        'si': 'Sinhala',
        'my': 'Myanmar',
        'th': 'Thai',
        'vi': 'Vietnamese',
        'id': 'Indonesian',
        'ms': 'Malay',
        'tl': 'Tagalog',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'no': 'Norwegian',
        'da': 'Danish',
        'fi': 'Finnish',
        'pl': 'Polish',
        'cs': 'Czech',
        'sk': 'Slovak',
        'hu': 'Romanian',
        'ro': 'Romanian',
        'bg': 'Bulgarian',
        'hr': 'Croatian',
        'sr': 'Serbian',
        'sl': 'Slovenian',
        'et': 'Estonian',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'el': 'Greek',
        'tr': 'Turkish',
        'he': 'Hebrew',
        'fa': 'Persian',
        'sw': 'Swahili',
        'af': 'Afrikaans',
        # Note: Tamang and Tharu may be detected as related languages
        # as they are low-resource languages
    }
    
    def __init__(self):
        """Initialize the language detector."""
        # deep_translator doesn't require initialization
        pass
    
    def detect(self, text: str) -> Optional[str]:
        """
        Detect the language of the input text.
        
        Args:
            text: Input text string
            
        Returns:
            Detected language code or None if detection fails
        """
        if not text or len(text.strip()) < 3:
            return None
        
        try:
            # Clean text for better detection
            cleaned_text = self._clean_text(text)
            if not cleaned_text:
                return None
            
            lang_code = detect(cleaned_text)
            return lang_code
        except LangDetectException:
            return None
    
    def detect_with_probability(self, text: str) -> Optional[Dict[str, any]]:
        """
        Detect language with probability scores.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with language code and probability, or None
        """
        if not text or len(text.strip()) < 3:
            return None
        
        try:
            cleaned_text = self._clean_text(text)
            if not cleaned_text:
                return None
            
            # Get all language probabilities
            from langdetect import detect_langs
            langs = detect_langs(cleaned_text)
            
            if langs and len(langs) > 0:
                top_lang = langs[0]
                return {
                    'language': top_lang.lang,
                    'probability': top_lang.prob,
                    'all_detections': [(l.lang, l.prob) for l in langs[:5]]
                }
            return None
        except LangDetectException:
            return None
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get human-readable language name from code.
        
        Args:
            lang_code: Language code (e.g., 'en')
            
        Returns:
            Language name or the code itself if not found
        """
        return self.SUPPORTED_LANGUAGES.get(lang_code, lang_code)
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for better language detection.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep unicode letters
        text = re.sub(r'[^\w\s\u0080-\uFFFF]', '', text)
        
        return text.strip()
    
    def is_reliable_detection(self, text: str, min_length: int = 10) -> bool:
        """
        Check if language detection is likely to be reliable.
        
        Args:
            text: Input text
            min_length: Minimum text length for reliable detection
            
        Returns:
            True if detection is likely reliable
        """
        cleaned = self._clean_text(text)
        return len(cleaned) >= min_length


class TextTranslator:
    """Handles text translation using Google Translate."""
    
    def __init__(self):
        """Initialize the translator."""
        self.translator = GoogleTranslator(source='auto', target='en')
        self.detector = LanguageDetector()
    
    def translate(self, text: str, dest_lang: str = 'en', 
                 src_lang: Optional[str] = None) -> Dict[str, any]:
        """
        Translate text to destination language.
        
        Args:
            text: Text to translate
            dest_lang: Destination language code (default: 'en')
            src_lang: Source language code (optional, auto-detected if None)
            
        Returns:
            Dictionary with translation result and metadata
        """
        if not text or not text.strip():
            return {
                'original_text': text,
                'translated_text': '',
                'source_language': None,
                'destination_language': dest_lang,
                'success': False,
                'error': 'Empty text provided'
            }
        
        try:
            # Auto-detect source language if not provided
            if src_lang is None:
                src_lang = self.detector.detect(text)
            
            # Perform translation using deep_translator
            translator_instance = GoogleTranslator(source=src_lang or 'auto', target=dest_lang)
            translated_text = translator_instance.translate(text)
            
            return {
                'original_text': text,
                'translated_text': translated_text,
                'source_language': src_lang,
                'destination_language': dest_lang,
                'pronunciation': None,
                'extra_data': None,
                'success': True,
                'error': None
            }
            
        except Exception as e:
            return {
                'original_text': text,
                'translated_text': text,  # Return original on failure
                'source_language': src_lang,
                'destination_language': dest_lang,
                'success': False,
                'error': str(e)
            }
    
    def translate_batch(self, texts: List[str], dest_lang: str = 'en',
                       src_lang: Optional[str] = None) -> List[Dict[str, any]]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate
            dest_lang: Destination language code
            src_lang: Source language code (optional)
            
        Returns:
            List of translation results
        """
        results = []
        for text in texts:
            result = self.translate(text, dest_lang, src_lang)
            results.append(result)
        return results
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get dictionary of supported languages.
        
        Returns:
            Dictionary mapping language codes to names
        """
        return LanguageDetector.SUPPORTED_LANGUAGES


class SignboardTranslator:
    """
    Combined translator for signboard text.
    Integrates language detection and translation.
    """
    
    def __init__(self, default_target_language: str = 'en'):
        """
        Initialize the signboard translator.
        
        Args:
            default_target_language: Default target language for translations
        """
        self.detector = LanguageDetector()
        self.translator = TextTranslator()
        self.default_target_language = default_target_language
    
    def process_text(self, text: str, 
                    target_language: Optional[str] = None) -> Dict[str, any]:
        """
        Process signboard text: detect language and translate.
        
        Args:
            text: Extracted text from signboard
            target_language: Target language (uses default if None)
            
        Returns:
            Complete processing result with all metadata
        """
        target_lang = target_language or self.default_target_language
        
        # Detect language
        lang_info = self.detector.detect_with_probability(text)
        detected_lang = lang_info['language'] if lang_info else None
        
        # Translate
        translation_result = self.translator.translate(
            text, 
            dest_lang=target_lang,
            src_lang=detected_lang
        )
        
        # Combine results
        return {
            'original_text': text,
            'translated_text': translation_result['translated_text'],
            'detected_language': detected_lang,
            'detected_language_name': self.detector.get_language_name(detected_lang) if detected_lang else 'Unknown',
            'detection_confidence': lang_info['probability'] if lang_info else None,
            'target_language': target_lang,
            'translation_success': translation_result['success'],
            'error': translation_result.get('error'),
            'full_detection_info': lang_info
        }
    
    def set_default_target_language(self, language: str):
        """
        Set the default target language.
        
        Args:
            language: Language code (e.g., 'en', 'es', 'fr')
        """
        self.default_target_language = language


def translate_text(text: str, target_language: str = 'en') -> str:
    """
    Convenience function to translate text.
    
    Args:
        text: Text to translate
        target_language: Target language code
        
    Returns:
        Translated text
    """
    translator = SignboardTranslator(default_target_language=target_language)
    result = translator.process_text(text, target_language)
    
    if result['translation_success']:
        return result['translated_text']
    else:
        raise RuntimeError(f"Translation failed: {result['error']}")


if __name__ == "__main__":
    # Example usage
    print("Language Detection and Translation Demo\n")
    
    # Test language detection
    detector = LanguageDetector()
    
    test_texts = [
        "Hello, welcome to our store",
        "नमस्ते, हाम्रो पसलमा स्वागत छ",
        "Bienvenido a nuestra tienda",
        " Bienvenue dans notre magasin"
    ]
    
    for text in test_texts:
        lang = detector.detect(text)
        lang_name = detector.get_language_name(lang) if lang else "Unknown"
        print(f"Text: {text}")
        print(f"Detected Language: {lang} ({lang_name})\n")
    
    # Test translation
    print("\nTranslation Demo:")
    translator = SignboardTranslator()
    
    nepali_text = "नमस्ते, यो एक परीक्षण हो"
    result = translator.process_text(nepali_text, target_language='en')
    
    print(f"Original: {nepali_text}")
    print(f"Detected: {result['detected_language_name']}")
    print(f"Translated: {result['translated_text']}")
