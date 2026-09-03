"""
Image Preprocessing Module

This module handles all image preprocessing operations using OpenCV.
It prepares signboard images for optimal OCR recognition by:
- Converting to grayscale
- Removing noise
- Adjusting contrast and brightness
- Applying thresholding techniques
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class ImagePreprocessor:
    """Handles image preprocessing operations for OCR optimization."""
    
    def __init__(self, target_width: int = 1024):
        """
        Initialize the preprocessor with optional target width.
        
        Args:
            target_width: Target width for image resizing (default: 1024)
        """
        self.target_width = target_width
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Loaded image as numpy array or None if loading fails
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image from {image_path}")
        return image
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image while maintaining aspect ratio.
        
        Args:
            image: Input image
            
        Returns:
            Resized image
        """
        height, width = image.shape[:2]
        
        # Only resize if width exceeds target
        if width > self.target_width:
            scale = self.target_width / width
            new_height = int(height * scale)
            image = cv2.resize(image, (self.target_width, new_height), 
                             interpolation=cv2.INTER_AREA)
        
        return image
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert color image to grayscale.
        
        Args:
            image: Input color image
            
        Returns:
            Grayscale image
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    def remove_noise(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Remove noise from image using Gaussian blur.
        
        Args:
            image: Input image
            kernel_size: Size of the Gaussian kernel (must be odd)
            
        Returns:
            Denoised image
        """
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def adjust_contrast(self, image: np.ndarray, alpha: float = 1.5, 
                       beta: int = 30) -> np.ndarray:
        """
        Adjust image contrast and brightness.
        
        Args:
            image: Input image
            alpha: Contrast control (1.0-3.0)
            beta: Brightness control (0-100)
            
        Returns:
            Image with adjusted contrast
        """
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    def apply_thresholding(self, image: np.ndarray, 
                          method: str = 'adaptive') -> np.ndarray:
        """
        Apply thresholding to enhance text visibility.
        
        Args:
            image: Grayscale input image
            method: Thresholding method ('otsu', 'adaptive', or 'simple')
            
        Returns:
            Thresholded binary image
        """
        if method == 'otsu':
            # Otsu's thresholding
            _, thresh = cv2.threshold(image, 0, 255, 
                                     cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh
        
        elif method == 'adaptive':
            # Adaptive thresholding - works better for varying lighting
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        
        else:  # simple
            _, thresh = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)
            return thresh
    
    def detect_edges(self, image: np.ndarray) -> np.ndarray:
        """
        Detect edges in the image using Canny edge detection.
        
        Args:
            image: Input image
            
        Returns:
            Edge-detected image
        """
        return cv2.Canny(image, 50, 150)
    
    def preprocess(self, image: np.ndarray, 
                   use_adaptive_threshold: bool = True) -> np.ndarray:
        """
        Complete preprocessing pipeline for OCR optimization.
        
        Args:
            image: Input image
            use_adaptive_threshold: Whether to use adaptive thresholding
            
        Returns:
            Preprocessed image ready for OCR
        """
        # Step 1: Resize if needed
        processed = self.resize_image(image)
        
        # Step 2: Convert to grayscale
        processed = self.convert_to_grayscale(processed)
        
        # Step 3: Remove noise
        processed = self.remove_noise(processed)
        
        # Step 4: Adjust contrast
        processed = self.adjust_contrast(processed)
        
        # Step 5: Apply thresholding
        if use_adaptive_threshold:
            processed = self.apply_thresholding(processed, method='adaptive')
        else:
            processed = self.apply_thresholding(processed, method='otsu')
        
        return processed
    
    def preprocess_from_file(self, image_path: str, 
                            use_adaptive_threshold: bool = True) -> np.ndarray:
        """
        Load and preprocess an image from file.
        
        Args:
            image_path: Path to the image file
            use_adaptive_threshold: Whether to use adaptive thresholding
            
        Returns:
            Preprocessed image
        """
        image = self.load_image(image_path)
        return self.preprocess(image, use_adaptive_threshold)


def preprocess_image(image_path: str, target_width: int = 1024) -> np.ndarray:
    """
    Convenience function to preprocess an image for OCR.
    
    Args:
        image_path: Path to the image file
        target_width: Target width for resizing
        
    Returns:
        Preprocessed image
    """
    preprocessor = ImagePreprocessor(target_width=target_width)
    return preprocessor.preprocess_from_file(image_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        preprocessor = ImagePreprocessor()
        
        # Load and preprocess
        original = preprocessor.load_image(image_path)
        processed = preprocessor.preprocess(original)
        
        # Save result
        output_path = "preprocessed_output.jpg"
        cv2.imwrite(output_path, processed)
        print(f"Preprocessed image saved to {output_path}")
    else:
        print("Usage: python image_preprocessor.py <image_path>")
