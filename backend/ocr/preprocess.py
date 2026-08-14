import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Generates multiple preprocessed image variations to maximize Tesseract OCR accuracy across different signboards, background contrasts, and lighting conditions.
    """
    image = cv2.imread(image_path)
    if image is None:
        return []

    height, width = image.shape[:2]

    # Resize image dynamically if it's too small or excessively large
    max_dim = 1800
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)
    elif max(height, width) < 600:
        scale = 1200 / max(height, width)
        image = cv2.resize(image, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_CUBIC)

    # 1. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 3. Gaussian Blur + Otsu Thresholding
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    _, otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 4. Inverted Otsu Thresholding (for light text on dark backgrounds)
    otsu_inv = cv2.bitwise_not(otsu)

    # Return list of preprocessed variations to try during extraction
    return [enhanced, gray, otsu, otsu_inv]