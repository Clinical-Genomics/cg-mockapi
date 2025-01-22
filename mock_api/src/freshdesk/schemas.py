from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr


class TicketCreate(BaseModel):
    subject: str
    description: str
    email: EmailStr
    priority: Optional[int] = 1
    status: Optional[int] = 2
    source: Optional[int] = 1
    custom_fields: Optional[Dict[str, Any]] = None


class TicketResponse(BaseModel):
    id: int
    subject: str
    description: str
    email: EmailStr
    priority: int
    status: int
    source: int
    custom_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    attachment_name: Optional[str] = None
