from pydantic import BaseModel
from typing import Dict, Any, Optional

class TemplateCreate(BaseModel):
    name: str
    extraction_schema: Optional[Dict[str, Any]] = None  # Rules to extract data
    layout_schema: Dict[str, Any]                      # Canvas/formatting rules for rendering

class TemplateResponse(BaseModel):
    id: int
    user_id: int
    name: str
    extraction_schema: Optional[Dict[str, Any]] = None
    layout_schema: Dict[str, Any]

    class Config:
        from_attributes = True
