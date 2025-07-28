from pdf2image import convert_from_bytes
import io
import base64
from config import IMAGE_MIME_TYPE

def convert_pdf_to_image(pdf_file):
    """Convert a PDF file to a list of PIL images."""
    return convert_from_bytes(pdf_file.read())

def image_to_base64_jpeg(image):
    """Convert a PIL image to base64-encoded JPEG."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return base64.b64encode(img_byte_arr.getvalue()).decode()

def prepare_pdf_content(pdf_file):
    """Prepare PDF content for API by converting first page to base64 JPEG."""
    try:
        if not pdf_file:
            raise FileNotFoundError("No file uploaded")
        images = convert_pdf_to_image(pdf_file)
        if not images:
            raise ValueError("PDF contains no pages")
        first_page = images[0]
        base64_data = image_to_base64_jpeg(first_page)
        return [{"mime_type": IMAGE_MIME_TYPE, "data": base64_data}]
    except pdf2image.exceptions.PDFPageCountError:
        raise ValueError("Invalid or empty PDF file")
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")