import cv2
import pytesseract

from ocr.preprocess import preprocess_image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\aswin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

def extract_text(image_path):
    processed = preprocess_image(image_path)

    custom_config = r'--oem 3 --psm 11'

    text = pytesseract.image_to_string(
    processed,
    config=custom_config,
    lang="eng+nep"

)
    return text