import json
import random
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Form, HTTPException, UploadFile
from fastapi import status as http_status

from .constants import Priority, Source, Status
from .exceptions import AttachmentError, InvalidTicketDataError
from .schemas import TicketCreate, TicketResponse

router = APIRouter()


def generate_ticket_id():
    """Generate a random 6-digit ticket ID."""
    return random.randint(100000, 999999)


@router.post(
    "/api/v2/tickets", response_model=TicketResponse, status_code=http_status.HTTP_201_CREATED
)
async def create_ticket(
    subject: str = Form(...),
    description: str = Form(...),
    email: str = Form(...),
    priority: int = Form(Priority.LOW),
    status: int = Form(Status.OPEN),
    source: int = Form(Source.EMAIL),
    custom_fields: Optional[str] = Form(None),
    attachment: Optional[UploadFile] = None,
):
    """Create a ticket with optional attachment - returns hardcoded success response."""
    try:
        # Validate custom fields if provided
        custom_fields_dict = None
        if custom_fields:
            try:
                custom_fields_dict = json.loads(custom_fields)
                if not isinstance(custom_fields_dict, dict):
                    raise ValueError("Custom fields must be a JSON object.")
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid JSON in custom_fields: {str(e)}",
                ) from e

        # Create ticket data
        ticket_data = TicketCreate(
            subject=subject,
            description=description,
            email=email,
            priority=priority,
            status=status,
            source=source,
            custom_fields=custom_fields_dict,
        )

        # Mock successful ticket creation with unique ID
        mock_response = TicketResponse(
            id=generate_ticket_id(),  # Generate unique ID instead of hardcoding
            subject=ticket_data.subject,
            description=ticket_data.description,
            email=ticket_data.email,
            priority=ticket_data.priority,
            status=ticket_data.status,
            source=ticket_data.source,
            custom_fields=ticket_data.custom_fields,
            created_at=datetime.now(),
            attachment_name=attachment.filename if attachment else None,
        )

        return mock_response

    except (InvalidTicketDataError, ValueError) as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except AttachmentError as e:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


# Optional: Add a reply endpoint if needed
@router.post("/api/v2/tickets/{ticket_id}/reply")
async def reply_to_ticket(
    ticket_id: int, body: str = Form(...), attachment: Optional[UploadFile] = None
):
    """Mock endpoint for replying to a ticket."""
    # Simply return a success response
    return {"message": "Reply added successfully"}
