# AI-based Signboard Reader and Translator

A comprehensive OCR and translation system for reading and translating signboards in multiple languages, built using Tesseract OCR, OpenCV, and Google Translate API.

## Project Overview

This project implements an intelligent system that:
- **Captures** signboard images from smartphones or digital cameras
- **Preprocesses** images using OpenCV for optimal OCR recognition
- **Extracts text** using Tesseract OCR engine
- **Detects language** automatically using langdetect
- **Translates text** to the user's preferred language using Google Translate

## Features

### Core Functionality
- ✅ Image preprocessing with OpenCV (grayscale conversion, noise removal, contrast enhancement, thresholding)
- ✅ Text extraction using Tesseract OCR with multi-language support
- ✅ Automatic language detection
- ✅ Real-time translation to 80+ languages
- ✅ Support for regional languages (Nepali, Hindi, Tamang, Tharu, etc.)
- ✅ Bounding box detection for text regions
- ✅ Confidence scoring for OCR results
- ✅ Batch processing of multiple images
- ✅ JSON export of results

### Technical Stack
- **Python 3.x** - Primary programming language
- **OpenCV** - Computer vision and image preprocessing
- **Tesseract OCR** - Optical Character Recognition engine
- **Google Translate API (googletrans)** - Machine translation
- **langdetect** - Language identification
- **NumPy** - Numerical operations
- **Pillow** - Image handling

## Installation

### Prerequisites

1. **Install Tesseract OCR:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr

# Install specific language packs
sudo apt-get install tesseract-ocr-eng tesseract-ocr-nep

# macOS
brew install tesseract

# Windows
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
```

2. **Install Python dependencies:**

```bash
pip install opencv-python-headless pytesseract pillow numpy googletrans==4.0.0-rc1 langdetect
```

## Project Structure

```
signboard_translator/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── image_preprocessor.py    # OpenCV image preprocessing
│   ├── ocr_engine.py            # Tesseract OCR integration
│   ├── translator.py            # Language detection & translation
│   └── signboard_reader.py      # Main pipeline orchestrator
├── tests/
│   └── test_signboard.py        # Unit tests
├── sample_images/               # Sample test images
├── docs/                        # Documentation
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Usage

### Command Line Interface

#### Basic Usage
```bash
# Process a single signboard image
python main.py signboard.jpg

# Specify target language (translate to Spanish)
python main.py signboard.jpg -t es

# Verbose output
python main.py signboard.jpg --verbose

# Simple output mode
python main.py signboard.jpg --simple-output
```

#### Advanced Options
```bash
# Specify OCR languages
python main.py signboard.jpg --ocr-lang eng nep hin

# Disable preprocessing (for already clean images)
python main.py signboard.jpg --no-preprocess

# Export results to JSON
python main.py image1.jpg image2.jpg -o results.json

# List available OCR languages
python main.py --list-languages

# Multiple images with custom settings
python main.py img1.jpg img2.jpg img3.jpg --ocr-lang eng nep -t fr -o output.json
```

### Programmatic Usage

```python
from src.signboard_reader import SignboardReader

# Initialize the reader
reader = SignboardReader(
    target_language='en',      # Translate to English
    ocr_languages=['eng', 'nep'],  # OCR languages
    verbose=True
)

# Process a single image
result = reader.process_image('path/to/signboard.jpg')

# Access results
print(f"Extracted Text: {result.extracted_text}")
print(f"Detected Language: {result.detected_language_name}")
print(f"Translated Text: {result.translated_text}")
print(f"OCR Confidence: {result.ocr_confidence:.2f}%")

# Process multiple images
results = reader.process_images(['img1.jpg', 'img2.jpg', 'img3.jpg'])

# Pretty print results
reader.print_result(result)
```

### Using Individual Components

#### Image Preprocessing
```python
from src.image_preprocessor import ImagePreprocessor

preprocessor = ImagePreprocessor(target_width=1024)

# Load and preprocess image
image = preprocessor.load_image('signboard.jpg')
processed = preprocessor.preprocess(image)

# Save preprocessed image
import cv2
cv2.imwrite('processed.jpg', processed)
```

#### OCR Engine
```python
from src.ocr_engine import OCREngine

engine = OCREngine(languages=['eng', 'nep'])

# Extract text from preprocessed image
result = engine.extract_text(processed_image)
print(f"Text: {result.text}")
print(f"Confidence: {result.confidence}%")

# Extract with bounding boxes
result = engine.extract_text_with_boxes(processed_image)
for box in result.bounding_boxes:
    print(f"Text: {box['text']}, Position: ({box['x']}, {box['y']})")
```

#### Translation
```python
from src.translator import SignboardTranslator

translator = SignboardTranslator(default_target_language='en')

# Detect language and translate
result = translator.process_text("नमस्ते, यो एक परीक्षण हो")
print(f"Detected: {result['detected_language_name']}")
print(f"Translated: {result['translated_text']}")
```

## Supported Languages

### OCR Languages (Tesseract)
The OCR language support depends on installed Tesseract language packs:
- `eng` - English
- `nep` - Nepali
- `hin` - Hindi
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `chi_sim` - Chinese (Simplified)
- `jpn` - Japanese
- `kor` - Korean
- And 100+ more (install via `apt-get install tesseract-ocr-<lang>`)

### Translation Languages (Google Translate)
80+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese, Japanese, Korean, Arabic, Hindi
- Nepali, Bengali, Tamil, Telugu, Marathi, Gujarati
- And many more...

## Configuration

### OCR Engine Settings

```python
# Page Segmentation Modes (PSM)
# 3 - Fully automatic page segmentation (default)
# 6 - Assume a single uniform block of text
# 7 - Treat the image as a single text line
# 13 - Sparse text. Find as much text as possible in no particular order

engine = OCREngine(psm_mode=3, oem_mode=3)
```

### Image Preprocessing Options

```python
preprocessor = ImagePreprocessor(target_width=1024)

# Manual preprocessing control
gray = preprocessor.convert_to_grayscale(image)
denoised = preprocessor.remove_noise(gray, kernel_size=3)
enhanced = preprocessor.adjust_contrast(denoised, alpha=1.5, beta=30)
binary = preprocessor.apply_thresholding(enhanced, method='adaptive')
```

## Testing

Run the included tests:

```bash
# Run all tests
python -m pytest tests/

# Or run test file directly
python tests/test_signboard.py
```

## Examples

### Example 1: Basic Signboard Translation
```bash
python main.py sample_images/nepali_sign.jpg -t en --verbose
```

### Example 2: Multi-language Street Signs
```bash
python main.py street_sign.jpg --ocr-lang eng nep hin spa -t en
```

### Example 3: Batch Processing Tourist Photos
```bash
python main.py photos/*.jpg -o translations.json --simple-output
```

## Troubleshooting

### Common Issues

**1. Tesseract not found:**
```bash
# Verify installation
tesseract --version

# Reinstall if needed
sudo apt-get install tesseract-ocr
```

**2. Language not available:**
```bash
# Check available languages
python main.py --list-languages

# Install missing language pack
sudo apt-get install tesseract-ocr-nep
```

**3. Low OCR accuracy:**
- Ensure good lighting conditions
- Use higher resolution images
- Try different preprocessing options
- Adjust PSM mode for different text layouts

**4. Translation fails:**
- Check internet connection (Google Translate requires online access)
- Verify the detected language is supported
- Try shorter text segments

## Performance Optimization

- **Image Size**: Resize large images to 1024px width for faster processing
- **Language Selection**: Specify only needed OCR languages for faster recognition
- **Batch Processing**: Process multiple images in one command for efficiency
- **Preprocessing**: Enable adaptive thresholding for challenging lighting conditions

## Future Enhancements

- [ ] Offline translation support
- [ ] Text-to-speech output
- [ ] Mobile app interface (Flutter/React Native)
- [ ] Real-time camera translation
- [ ] Translation history storage
- [ ] Enhanced support for low-resource languages (Tamang, Tharu)
- [ ] Deep learning-based scene text recognition (CRNN, TrOCR)

## License

This project is developed for educational and research purposes as proposed in the project documentation.

## References

1. Smith, R. "An Overview of the Tesseract OCR Engine", ICDAR 2007
2. Google Cloud Translation API Documentation
3. OpenCV Documentation: https://docs.opencv.org/
4. Tesseract OCR Documentation: https://tesseract-ocr.github.io/

## Authors

AI-based Signboard Reader and Translator Project
Based on the project proposal document.

## Contact

For questions or contributions, please refer to the project documentation.
