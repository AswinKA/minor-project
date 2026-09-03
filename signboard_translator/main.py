#!/usr/bin/env python3
"""
Main entry point for the AI-based Signboard Reader and Translator CLI

This command-line interface allows users to:
- Process signboard images for text extraction and translation
- Configure OCR languages and target translation language
- Batch process multiple images
- Export results to JSON format

Usage:
    python main.py <image_path> [options]
    
Examples:
    python main.py signboard.jpg
    python main.py signboard.jpg -t es --verbose
    python main.py image1.jpg image2.jpg image3.jpg -o results.json
    python main.py signboard.jpg --ocr-lang eng nep hin -t fr
"""

# 1. Import libraries first
import argparse
import json
import sys
import os
from pathlib import Path
from typing import List, Optional

# 2. Configure Tesseract Path BEFORE importing pytesseract or using it
# This ensures Windows finds the executable even if not in PATH
if sys.platform == 'win32':
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        if __name__ == "__main__":
            print(f"[System] Tesseract path set to: {tesseract_path}")

# 3. Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# 4. Import project modules
from src.signboard_reader import SignboardReader, SignboardResult, read_signboard
from src.ocr_engine import OCREngine


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="AI-based Signboard Reader and Translator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s signboard.jpg
  %(prog)s signboard.jpg -t es --verbose
  %(prog)s image1.jpg image2.jpg -o results.json
  %(prog)s signboard.jpg --ocr-lang eng nep hin -t fr
        """
    )
    
    # Positional arguments (make optional if --list-languages is used)
    parser.add_argument(
        'images',
        nargs='*',
        help='Path(s) to signboard image(s)'
    )
    
    # Optional arguments
    parser.add_argument(
        '-t', '--target-language',
        default='en',
        help='Target language for translation (default: en)'
    )
    
    parser.add_argument(
        '--ocr-lang', '--ocr-langs',
        nargs='+',
        default=None,
        help='OCR language codes (e.g., eng nep hin)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output JSON file for results'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--no-preprocess',
        action='store_true',
        help='Disable image preprocessing'
    )
    
    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List available OCR languages and exit'
    )
    
    parser.add_argument(
        '--simple-output',
        action='store_true',
        help='Show only extracted and translated text'
    )
    
    return parser.parse_args()


def list_available_languages():
    """List all available Tesseract OCR languages."""
    print("Checking Tesseract OCR installation...\n")
    
    try:
        engine = OCREngine()
        available = engine.get_available_languages()
        
        print("Available OCR Languages:")
        print("-" * 40)
        for lang in sorted(available):
            print(f"  - {lang}")
        
        print("\nCommon language codes:")
        print("  eng - English")
        print("  nep - Nepali")
        print("  spa - Spanish")
        print("  fra - French")
        print("  deu - German")
        print("  hin - Hindi")
        print("  chi_sim - Chinese Simplified")
        print("  jpn - Japanese")
        print("  kor - Korean")
        print("\nNote: Install additional languages using:")
        print("  sudo apt-get install tesseract-ocr-<lang>")
        
    except Exception as e:
        print(f"Error checking Tesseract: {e}")
        sys.exit(1)


def result_to_dict(result: SignboardResult) -> dict:
    """Convert SignboardResult to dictionary for JSON export."""
    return {
        'image_path': result.image_path,
        'processing_time_seconds': result.processing_time,
        'extracted_text': result.extracted_text,
        'ocr_confidence_percent': result.ocr_confidence,
        'ocr_language': result.ocr_language,
        'translated_text': result.translated_text,
        'detected_language_code': result.detected_language,
        'detected_language_name': result.detected_language_name,
        'target_language': result.target_language,
        'translation_successful': result.translation_success,
        'error': result.error
    }


def print_simple_result(result: SignboardResult, index: int = 0, total: int = 1):
    """Print simplified output showing only essential information."""
    if total > 1:
        print(f"\n{'='*60}")
        print(f"Image {index + 1}/{total}: {result.image_path}")
        print('='*60)
    
    if result.error:
        print(f"ERROR: {result.error}")
        return
    
    print(f"\n[ORIGINAL TEXT]")
    print(result.extracted_text if result.extracted_text else "(No text detected)")
    
    print(f"\n[LANGUAGE DETECTED]")
    print(f"{result.detected_language_name} ({result.detected_language or 'Unknown'})")
    
    print(f"\n[TRANSLATED TEXT - {result.target_language.upper()}]")
    print(result.translated_text if result.translation_success else "(Translation failed)")


def print_detailed_result(result: SignboardResult, index: int = 0, total: int = 1):
    """Print detailed processing results."""
    if total > 1:
        print(f"\n{'#'*60}")
        print(f"# Image {index + 1}/{total}")
        print('#'*60)
    
    print(f"\nFile: {result.image_path}")
    print(f"Processing Time: {result.processing_time:.2f}s")
    
    if result.error:
        print(f"\n❌ ERROR: {result.error}")
        return
    
    print(f"\n📝 EXTRACTED TEXT:")
    print(f"   Language config: {result.ocr_language}")
    print(f"   Confidence: {result.ocr_confidence:.2f}%")
    print(f"   ---")
    if result.extracted_text:
        # Word wrap long lines
        words = result.extracted_text.split()
        line = "   "
        for word in words:
            if len(line) + len(word) > 70:
                print(line)
                line = "   " + word
            else:
                line += " " + word
        if line.strip():
            print(line)
    else:
        print("   (No text detected)")
    
    print(f"\n🌍 LANGUAGE DETECTION:")
    print(f"   Detected: {result.detected_language_name}")
    print(f"   Code: {result.detected_language or 'Unknown'}")
    
    print(f"\n🔄 TRANSLATION ({result.target_language.upper()}):")
    if result.translation_success and result.translated_text:
        words = result.translated_text.split()
        line = "   "
        for word in words:
            if len(line) + len(word) > 70:
                print(line)
                line = "   " + word
            else:
                line += " " + word
        if line.strip():
            print(line)
    else:
        print("   (Translation failed or no text)")
    
    print()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Handle --list-languages option
    if args.list_languages:
        list_available_languages()
        return 0
    
    # Validate input files exist
    valid_images = []
    for image_path in args.images:
        if os.path.isfile(image_path):
            valid_images.append(image_path)
        else:
            print(f"Warning: File not found - {image_path}", file=sys.stderr)
    
    if not valid_images:
        print("Error: No valid image files provided", file=sys.stderr)
        return 1
    
    # Configure OCR languages
    ocr_languages = args.ocr_lang
    if ocr_languages is None:
        # Default to English and Nepali as per proposal
        ocr_languages = ['eng', 'nep']
    
    # Initialize reader
    try:
        reader = SignboardReader(
            target_language=args.target_language,
            ocr_languages=ocr_languages,
            enable_preprocessing=not args.no_preprocess,
            verbose=args.verbose
        )
    except RuntimeError as e:
        print(f"Error initializing SignboardReader: {e}", file=sys.stderr)
        print("\nMake sure Tesseract OCR is installed:", file=sys.stderr)
        print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki", file=sys.stderr)
        return 1
    
    # Process images
    print(f"\nProcessing {len(valid_images)} image(s)...")
    print(f"Target language: {args.target_language.upper()}")
    print(f"OCR languages: {', '.join(ocr_languages)}")
    print()
    
    results: List[SignboardResult] = []
    
    for i, image_path in enumerate(valid_images):
        if args.verbose:
            print(f"\n[{i+1}/{len(valid_images)}] Processing: {image_path}")
        
        result = reader.process_image(image_path)
        results.append(result)
        
        # Print results based on output mode
        if args.simple_output:
            print_simple_result(result, i, len(valid_images))
        else:
            print_detailed_result(result, i, len(valid_images))
    
    # Export to JSON if requested
    if args.output:
        try:
            output_data = {
                'summary': {
                    'total_images': len(valid_images),
                    'successful_extractions': sum(1 for r in results if r.extracted_text),
                    'successful_translations': sum(1 for r in results if r.translation_success),
                    'target_language': args.target_language
                },
                'results': [result_to_dict(r) for r in results]
            }
            
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Results exported to: {args.output}")
        except Exception as e:
            print(f"\n⚠️  Warning: Could not export results: {e}", file=sys.stderr)
    
    # Summary
    successful = sum(1 for r in results if not r.error and r.extracted_text)
    print(f"\n{'='*60}")
    print(f"Summary: {successful}/{len(valid_images)} images processed successfully")
    print(f"{'='*60}\n")
    
    return 0 if successful > 0 else 1


if __name__ == "__main__":
    sys.exit(main())