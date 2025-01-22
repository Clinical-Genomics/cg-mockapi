# mock_api/src/lims/schemas.py
from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    """Response format for submit_project"""

    id: str
    name: str
    date: Optional[datetime] = None


class SamplesResponse(BaseModel):
    """Response format for get_samples when map_ids=True"""

    sample_map: Dict[str, str]
