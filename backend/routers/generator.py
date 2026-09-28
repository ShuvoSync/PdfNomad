from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from models.user import User
from models.template import Template
from models.limitation import UserLimitation
from services.auth_service import get_current_user
from services.extractor_engine import extract_text_from_pdf_bytes
from services.renderer_engine import render_pdf_from_metadata
import json

router = APIRouter()

@router.post("/extract")
async def extract_pdf_data(
    file: UploadFile = File(...),
    template_id: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a source PDF and extract text/data using optional template rules.
    """
    file_bytes = await file.read()
    
    rules = None
    if template_id:
        result = await db.execute(
            select(Template).where(Template.id == template_id, Template.user_id == current_user.id)
        )
        template = result.scalar_one_or_none()
        if template:
            rules = template.extraction_schema

    extraction_result = extract_text_from_pdf_bytes(file_bytes, rules)
    return {"filename": file.filename, "extraction": extraction_result}

@router.post("/render")
async def render_pdf_document(
    template_id: str = Form(...),
    data_payload_json: str = Form(...), # Passed as a JSON string
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Compiles and streams a PDF live using stored template metadata and injected data.
    Enforces monthly quota limits.
    """
    # 1. Check user limitations / quotas
    lim_result = await db.execute(select(UserLimitation).where(UserLimitation.user_id == current_user.id))
    limitation = lim_result.scalar_one_or_none()
    
    if limitation and limitation.current_usage >= limitation.max_monthly_generations:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Monthly generation limit reached. Please upgrade your subscription tier."
        )

    # 2. Fetch the layout template
    tmpl_result = await db.execute(
        select(Template).where(Template.id == template_id, Template.user_id == current_user.id)
    )
    template = tmpl_result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found or unauthorized.")

    try:
        data_payload = json.loads(data_payload_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for data_payload_json.")

    # 3. Render PDF binary via ReportLab engine (No raw binary saved to disk!)
    pdf_bytes = render_pdf_from_metadata(template.layout_schema, data_payload)

    # 4. Increment usage counter
    if limitation:
        limitation.current_usage += 1
        await db.commit()

    # 5. Stream PDF directly back to browser/client
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=generated_{template_id}.pdf"}
    )
