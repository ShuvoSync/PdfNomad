import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def render_pdf_from_metadata(layout_schema: dict, data_payload: dict) -> bytes:
    """
    Compiles a PDF dynamically using layout instructions and injected data points.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Extract layout settings with fallback defaults
    title = layout_schema.get("title", "PDF Nomad Generated Document")
    font_size = layout_schema.get("font_size", 12)
    
    # Draw elements onto the PDF canvas based on user metadata
    c.setFont("Helvetica-Bold", font_size + 4)
    c.drawString(50, 750, title)
    
    c.setFont("Helvetica", font_size)
    y_position = 700
    
    # Inject user data fields dynamically
    for key, value in data_payload.items():
        c.drawString(50, y_position, f"{key}: {value}")
        y_position -= 25
        if y_position < 50:
            c.showPage()
            y_position = 750
            
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
