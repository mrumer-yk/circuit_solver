"""
Utility functions for image processing and validation.
"""
import io
from typing import Tuple, Optional
from PIL import Image
from config.settings import settings

def validate_image_format(image_data: bytes) -> Tuple[bool, str]:
    """
    Validate image format and return validation result.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Check if image format is supported
        format_lower = image.format.lower() if image.format else ""
        if not any(format_lower.endswith(fmt.lower()) for fmt in settings.SUPPORTED_FORMATS):
            return False, f"Unsupported image format. Supported formats: {', '.join(settings.SUPPORTED_FORMATS)}"
        
        # Check image dimensions
        if image.width < 100 or image.height < 100:
            return False, "Image dimensions too small. Minimum size: 100x100 pixels"
        
        if image.width > 4000 or image.height > 4000:
            return False, "Image dimensions too large. Maximum size: 4000x4000 pixels"
        
        return True, "Image validation successful"
        
    except Exception as e:
        return False, f"Image validation failed: {str(e)}"

def optimize_image_for_analysis(image_data: bytes, max_size: int = 1024) -> bytes:
    """
    Optimize image for analysis by resizing if necessary.
    
    Args:
        image_data: Original image data
        max_size: Maximum dimension size
        
    Returns:
        Optimized image data as bytes
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Resize if image is too large
        if image.width > max_size or image.height > max_size:
            # Maintain aspect ratio
            ratio = min(max_size / image.width, max_size / image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary (Gemini works better with RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        # Return original if optimization fails
        return image_data

def get_image_info(image_data: bytes) -> dict:
    """
    Get basic information about the image.
    
    Returns:
        Dictionary with image information
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        return {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.width,
            'height': image.height,
            'file_size_mb': len(image_data) / (1024 * 1024)
        }
    except Exception as e:
        return {'error': str(e)}

def create_image_thumbnail(image_data: bytes, size: Tuple[int, int] = (200, 200)) -> bytes:
    """
    Create a thumbnail of the image for display purposes.
    
    Args:
        image_data: Original image data
        size: Thumbnail size (width, height)
        
    Returns:
        Thumbnail image data as bytes
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Create thumbnail
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85)
        return output.getvalue()
        
    except Exception as e:
        # Return original if thumbnail creation fails
        return image_data
