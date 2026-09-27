from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.database import get_db
from models.template import Template
from models.user import User
from schemas.template_schema import TemplateCreate, TemplateResponse
from services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_in: TemplateCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new custom extraction or layout format template for the authenticated user.
    """
    new_template = Template(
        user_id=current_user.id,
        name=template_in.name,
        extraction_schema=template_in.extraction_schema,
        layout_schema=template_in.layout_schema
    )
    
    db.add(new_template)
    await db.commit()
    await db.refresh(new_template)
    
    return new_template

@router.get("/", response_model=List[TemplateResponse])
async def list_user_templates(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all templates owned by the logged-in user.
    """
    result = await db.execute(select(Template).where(Template.user_id == current_user.id))
    templates = result.scalars().all()
    return templates

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template_by_id(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch a specific template by ID, ensuring it belongs to the user.
    """
    result = await db.execute(
        select(Template).where(Template.id == template_id, Template.user_id == current_user.id)
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found or unauthorized access."
        )
        
    return template

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific template.
    """
    result = await db.execute(
        select(Template).where(Template.id == template_id, Template.user_id == current_user.id)
    )
    template = result.scalar_one_or_none()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found or unauthorized access."
        )
        
    await db.delete(template)
    await db.commit()
    return None
