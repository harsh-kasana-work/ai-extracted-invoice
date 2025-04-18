import pytesseract
import platform
from PIL import Image
import logging
from typing import List, Dict, Optional, Union
from pathlib import Path
import pdf2image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up Tesseract path
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class TesseractOCR:
    """OCR engine using Tesseract."""
    
    def __init__(self, lang: str = 'eng', config: str = '--psm 11'):
        """
        Initialize TesseractOCR.
        
        Args:
            lang: Language for OCR
            config: Tesseract configuration
        """
        self.lang = lang
        self.config = config
    
    def extract_text(self, image: Union[Image.Image, str, Path]) -> List[Dict]:
        """
        Extract text from an image using Tesseract with detailed info.
        
        Args:
            image: Input image as PIL Image or path to image file
        
        Returns:
            List of detected text blocks with text, position, and confidence
        """
        # Handle different input types
        if isinstance(image, (str, Path)):
            pil_image = Image.open(image)
        else:
            pil_image = image
        
        # Get data including bounding boxes
        data = pytesseract.image_to_data(
            pil_image, 
            lang=self.lang, 
            config=self.config, 
            output_type=pytesseract.Output.DICT
        )
        
        results = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            # Skip empty text or low confidence
            if int(data['conf'][i]) < 0 or not data['text'][i].strip():
                continue
            
            # Extract bounding box
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            
            # Create result dictionary
            result = {
                'text': data['text'][i],
                'bbox': [x, y, x + w, y + h],  # [x1, y1, x2, y2]
                'confidence': float(data['conf'][i]) / 100,
                'block_num': data['block_num'][i],
                'line_num': data['line_num'][i],
                'word_num': data['word_num'][i]
            }
            
            results.append(result)
        
        return results
    
    def get_full_text(self, image: Union[Image.Image, str, Path]) -> str:
        """
        Extract all text from an image as a single string.
        
        Args:
            image: Input image as PIL Image or path to image file
            
        Returns:
            Extracted text as string
        """
        # Handle different input types
        if isinstance(image, (str, Path)):
            pil_image = Image.open(image)
        else:
            pil_image = image
            
        return pytesseract.image_to_string(pil_image, lang=self.lang, config=self.config)

def pdf_to_images(
    uploaded_file, 
    dpi: int = 300,
    grayscale: bool = False,
    use_pdftocairo: bool = True
) -> List[Image.Image]:
    """
    Convert a PDF document to a list of PIL images.
    
    Args:
        uploaded_file: A file-like object (e.g., from Streamlit uploader)
        dpi: DPI for the output images
        grayscale: Whether to convert images to grayscale
        use_pdftocairo: Whether to use pdftocairo for conversion
        
    Returns:
        List of PIL Images
    """
    try:
        # Read the file content into bytes
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # reset for reuse if needed

        # Convert PDF to PIL Images
        pil_images = pdf2image.convert_from_bytes(
            pdf_file=file_bytes,
            dpi=dpi,
            grayscale=grayscale,
            use_pdftocairo=use_pdftocairo
        )
        
        logger.info(f"Successfully converted {len(pil_images)} pages")
        return pil_images
    
    except Exception as e:
        logger.error(f"Error converting PDF: {e}")
        raise
