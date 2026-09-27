import io
from pypdf import PdfReader

def extract_text_from_pdf_bytes(file_bytes: bytes, rules: dict = None) -> dict:
    """
    Extracts text from uploaded PDF bytes and applies optional user-defined rules.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        # Here you can later apply regex or keyword extraction based on the user's 'rules' dictionary
        return {
            "status": "success",
            "total_pages": len(reader.pages),
            "raw_text_snippet": extracted_text[:500], # Preview snippet
            "extracted_fields": {"sample_key": "sample_value"}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
