
##  to test type following in terminal pytest tests/.
import pytest
from src.pdf_utils import prepare_pdf_content
from io import BytesIO

def test_prepare_pdf_content_valid_pdf():
    with open("tests/sample.pdf", "rb") as f:
        pdf_content = prepare_pdf_content(f)
    assert isinstance(pdf_content, list)
    assert pdf_content[0]["mime_type"] == "image/jpeg"
    assert "data" in pdf_content[0]

def test_prepare_pdf_content_no_file():
    with pytest.raises(FileNotFoundError):
        prepare_pdf_content(None)