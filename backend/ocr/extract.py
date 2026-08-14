import os
import cv2
import pytesseract
from ocr.preprocess import preprocess_image

# Configure Tesseract path
TESSERACT_EXE = r"C:\Users\aswin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_EXE):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE

def extract_text(image_path, lang="eng+nep"):
    """
    Extracts text from an image using Tesseract OCR with adaptive preprocessing variations and page segmentation modes.
    """
    variations = preprocess_image(image_path)
    if not variations:
        return ""

    best_text = ""
    psm_modes = ['--psm 3', '--psm 6', '--psm 11']

    # Try extracted variations with different PSM configurations
    for img_var in variations:
        for psm in psm_modes:
            config = f'{psm} --oem 3'
            try:
                text = pytesseract.image_to_string(img_var, config=config, lang=lang)
                cleaned = text.strip()
                if len(cleaned) > len(best_text):
                    best_text = cleaned
            except Exception:
                # If specified language combination fails (e.g. tessdata missing), fallback to english
                try:
                    text = pytesseract.image_to_string(img_var, config=config, lang="eng")
                    cleaned = text.strip()
                    if len(cleaned) > len(best_text):
                        best_text = cleaned
                except Exception:
                    continue

        # If we got a good text result (> 5 characters), we can return early
        if len(best_text) > 10:
            break

    return best_text