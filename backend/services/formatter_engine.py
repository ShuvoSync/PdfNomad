import re
from pathlib import Path
from datetime import datetime

# Default preset templates available out-of-the-box
DEFAULT_FORMAT_PRESETS = {
    "standard": "{supplier}/{year}/{month}/{invoice_number}.pdf",
    "by_type": "{doc_type}/{supplier}/{year}-{month}_{invoice_number}.pdf",
    "flat_folder": "{supplier}_{invoice_number}_{date}.pdf"
}

def sanitize_string(value: str) -> str:
    """Removes unsafe characters for file/folder names (e.g., /, \, :, *)."""
    if not value:
        return "Unknown"
    # Keep alphanumeric, spaces, hyphens, underscores
    cleaned = re.sub(r'[\\/*?:"<>|]', "", str(value))
    return cleaned.strip().replace(" ", "_")

def build_destination_path(
    root_output_dir: str, 
    template_pattern: str, 
    extracted_data: dict
) -> tuple[Path, str]:
    """
    Takes a format pattern (e.g., '{supplier}/{year}/{invoice_number}.pdf') 
    and replaces tokens with actual extracted metadata.
    """
    # Fallback default if template is empty
    if not template_pattern:
        template_pattern = DEFAULT_FORMAT_PRESETS["standard"]

    # Extract or default metadata fields
    raw_date = extracted_data.get("date")
    if raw_date:
        try:
            parsed_date = datetime.strptime(raw_date, "%Y-%m-%d") # Adjust format as needed
            year = str(parsed_date.year)
            month = parsed_date.strftime("%m-%B")
        except ValueError:
            year = datetime.now().strftime("%Y")
            month = datetime.now().strftime("%m")
    else:
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")

    tokens = {
        "supplier": sanitize_string(extracted_data.get("supplier", "Unclassified")),
        "invoice_number": sanitize_string(extracted_data.get("invoice_number", "NoInv")),
        "doc_type": sanitize_string(extracted_data.get("doc_type", "Invoice")),
        "date": sanitize_string(raw_date or datetime.now().strftime("%Y-%m-%d")),
        "year": year,
        "month": month,
        "amount": sanitize_string(extracted_data.get("amount", "0.00"))
    }

    # Safely format the template string using python format map
    # e.g., "{supplier}/{year}/{invoice_number}.pdf" becomes "DEWA/2026/INV12345.pdf"
    try:
        relative_path_str = template_pattern.format_map(tokens)
    except KeyError as e:
        # Fallback if user typed an invalid token
        relative_path_str = f"Unclassified/{tokens['supplier']}_{tokens['invoice_number']}.pdf"

    full_destination = Path(root_output_dir) / relative_path_str
    return full_destination.parent, full_destination.name
