import sys
import os
import glob
from ocr.extract import extract_text
from ocr.language import detect_language
from ocr.translator import translate_text

def test_all():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    image_files = glob.glob("uploads/*.jpg") + glob.glob("uploads/*.jpeg") + glob.glob("uploads/*.png")
    if not image_files:
        print("No images found in uploads directory.")
        return

    for img_path in image_files[:3]:
        print("=" * 50)
        print(f"Processing Image: {img_path}")
        text = extract_text(img_path)
        print("Extracted Text:")
        print(text if text else "[No text detected]")
        
        if text:
            lang = detect_language(text)
            print(f"Detected Language: {lang}")
            translated = translate_text(text, source=lang, target="en")
            print("Translation (English):")
            print(translated)
        print("=" * 50)

if __name__ == "__main__":
    test_all()
