"""
Image enhancement utilities for handling blurry photos and handwritten circuits.
"""
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import Tuple, Optional

def enhance_blurry_image(image_data: bytes) -> bytes:
    """
    Enhance blurry circuit images using various techniques.
    
    Args:
        image_data: Original blurry image data
        
    Returns:
        Enhanced image data as bytes
    """
    try:
        # Convert PIL image to OpenCV format
        pil_image = Image.open(io.BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Apply multiple enhancement techniques
        
        # 1. Unsharp masking for sharpening
        gaussian = cv2.GaussianBlur(cv_image, (0, 0), 2.0)
        sharpened = cv2.addWeighted(cv_image, 1.5, gaussian, -0.5, 0)
        
        # 2. Contrast enhancement
        lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        # 3. Noise reduction
        denoised = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
        
        # 4. Edge enhancement
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        edge_enhanced = cv2.filter2D(denoised, -1, kernel)
        
        # Convert back to PIL and save
        enhanced_pil = Image.fromarray(cv2.cvtColor(edge_enhanced, cv2.COLOR_BGR2RGB))
        output = io.BytesIO()
        enhanced_pil.save(output, format='JPEG', quality=95, optimize=True)
        
        return output.getvalue()
        
    except Exception as e:
        # Return original if enhancement fails
        return image_data

def enhance_handwritten_circuit(image_data: bytes) -> bytes:
    """
    Enhance handwritten circuit diagrams for better analysis.
    
    Args:
        image_data: Original handwritten circuit image
        
    Returns:
        Enhanced image data as bytes
    """
    try:
        # Convert PIL image to OpenCV format
        pil_image = Image.open(io.BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # 1. Convert to grayscale for better processing
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # 2. Apply adaptive thresholding for better text/line detection
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # 3. Morphological operations to clean up the image
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # 4. Line enhancement for circuit connections
        kernel_horizontal = np.ones((1, 15), np.uint8)
        kernel_vertical = np.ones((15, 1), np.uint8)
        
        horizontal_lines = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel_horizontal)
        vertical_lines = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel_vertical)
        
        # Combine horizontal and vertical lines
        lines = cv2.addWeighted(horizontal_lines, 1, vertical_lines, 1, 0)
        
        # 5. Enhance contrast for better readability
        enhanced = cv2.convertScaleAbs(lines, alpha=1.5, beta=30)
        
        # Convert back to PIL and save
        enhanced_pil = Image.fromarray(enhanced)
        output = io.BytesIO()
        enhanced_pil.save(output, format='JPEG', quality=95, optimize=True)
        
        return output.getvalue()
        
    except Exception as e:
        # Return original if enhancement fails
        return image_data

def auto_enhance_circuit_image(image_data: bytes) -> Tuple[bytes, dict]:
    """
    Automatically detect and enhance circuit images based on quality issues.
    
    Args:
        image_data: Original image data
        
    Returns:
        Tuple of (enhanced_image_data, enhancement_info)
    """
    try:
        # Convert to PIL for analysis
        pil_image = Image.open(io.BytesIO(image_data))
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        enhancement_info = {
            'blur_detected': False,
            'handwritten_detected': False,
            'enhancements_applied': [],
            'quality_score': 0.0
        }
        
        # 1. Detect blur using Laplacian variance
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_threshold = 100.0
        
        if laplacian_var < blur_threshold:
            enhancement_info['blur_detected'] = True
            enhancement_info['enhancements_applied'].append('blur_reduction')
            image_data = enhance_blurry_image(image_data)
        
        # 2. Detect handwritten characteristics
        # Look for irregular patterns and text-like features
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Handwritten circuits typically have more irregular edges
        if edge_density > 0.1 and laplacian_var < 200:
            enhancement_info['handwritten_detected'] = True
            enhancement_info['enhancements_applied'].append('handwritten_enhancement')
            image_data = enhance_handwritten_circuit(image_data)
        
        # 3. Calculate quality score
        enhanced_pil = Image.open(io.BytesIO(image_data))
        enhanced_cv = cv2.cvtColor(np.array(enhanced_pil), cv2.COLOR_RGB2BGR)
        enhanced_gray = cv2.cvtColor(enhanced_cv, cv2.COLOR_BGR2GRAY)
        
        # Quality metrics
        sharpness = cv2.Laplacian(enhanced_gray, cv2.CV_64F).var()
        contrast = enhanced_gray.std()
        
        # Normalize and combine metrics
        quality_score = min(1.0, (sharpness / 500.0 + contrast / 100.0) / 2.0)
        enhancement_info['quality_score'] = quality_score
        
        return image_data, enhancement_info
        
    except Exception as e:
        # Return original with error info
        return image_data, {
            'error': str(e),
            'enhancements_applied': [],
            'quality_score': 0.0
        }

def create_enhancement_comparison(original_data: bytes, enhanced_data: bytes) -> bytes:
    """
    Create a side-by-side comparison of original vs enhanced image.
    
    Args:
        original_data: Original image data
        enhanced_data: Enhanced image data
        
    Returns:
        Comparison image data as bytes
    """
    try:
        original_pil = Image.open(io.BytesIO(original_data))
        enhanced_pil = Image.open(io.BytesIO(enhanced_data))
        
        # Resize both images to same height for comparison
        height = min(original_pil.height, enhanced_pil.height)
        width = original_pil.width + enhanced_pil.width
        
        # Create comparison image
        comparison = Image.new('RGB', (width, height), 'white')
        
        # Resize and paste original
        original_resized = original_pil.resize((original_pil.width, height), Image.Resampling.LANCZOS)
        comparison.paste(original_resized, (0, 0))
        
        # Resize and paste enhanced
        enhanced_resized = enhanced_pil.resize((enhanced_pil.width, height), Image.Resampling.LANCZOS)
        comparison.paste(enhanced_resized, (original_pil.width, 0))
        
        # Add labels
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(comparison)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "Original", fill='black', font=font)
        draw.text((original_pil.width + 10, 10), "Enhanced", fill='black', font=font)
        
        # Save comparison
        output = io.BytesIO()
        comparison.save(output, format='JPEG', quality=90)
        return output.getvalue()
        
    except Exception as e:
        # Return enhanced image if comparison fails
        return enhanced_data
