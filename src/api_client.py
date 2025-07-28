import google.generativeai as genai
from config import GEMINI_MODEL

def get_gemini_response(input_text, pdf_content, prompt):
    """Call Gemini API with input text, PDF content, and prompt."""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}")