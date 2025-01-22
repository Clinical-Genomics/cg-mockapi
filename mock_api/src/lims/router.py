import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi import status as http_status
from fastapi.responses import Response

from .constants import ID_PREFIXES, LIMS_PREFIX, MEDIA_TYPE_XML
from .templates import (
    get_container_batch_xml,
    get_container_xml,
    get_project_xml,
    get_researcher_xml,
    get_samples_xml,
)
from .utils import (
    parse_container_from_xml,
    parse_project_from_xml,
    parse_samples_from_xml,
)

router = APIRouter(prefix=LIMS_PREFIX)


@router.get("/researchers")
async def get_researchers(username: str | None = None):
    """Mock researcher endpoint"""
    xml_content = get_researcher_xml(username)
    return Response(content=xml_content, media_type=MEDIA_TYPE_XML)


@router.post("/projects")
async def submit_project(request: Request):
    """Create project from XML - returns hardcoded success response"""
    try:
        body = await request.body()
        project_name = parse_project_from_xml(body.decode())
        project_id = f"{ID_PREFIXES['project']}-{uuid.uuid4().hex[:6]}"

        xml_response = get_project_xml(project_id, project_name)
        return Response(content=xml_response, media_type=MEDIA_TYPE_XML)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


# mock_api/src/lims/router.py - just the container endpoints part


@router.post("/containers/batch/create")
async def create_containers(request: Request):
    """Create batch of containers"""
    try:
        body = await request.body()
        container_data = parse_container_from_xml(body.decode())
        container_id = f"{uuid.uuid4().hex[:6]}"

        xml_response = get_container_batch_xml(container_id, container_data)

        return Response(content=xml_response, media_type=MEDIA_TYPE_XML)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/containers/{container_id}")
async def get_container(container_id: str, name: str):
    """Get container details. Name comes as query parameter."""
    try:
        if not name:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail="Name parameter is required"
            )

        xml_response = get_container_xml(container_id, name)
        return Response(content=xml_response, media_type=MEDIA_TYPE_XML)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/samples")
async def get_samples(
    project_id: str | None = None,
    projectlimsid: str | None = None,
):
    """Retrieve samples for a project - returns hardcoded response"""
    try:
        final_project_id = project_id or projectlimsid
        if not final_project_id:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Missing required query parameter: project_id or projectlimsid.",
            )

        # Create mock sample map response
        mock_samples = {
            "sample1": f"{ID_PREFIXES['sample']}-{uuid.uuid4().hex[:6]}",
            "sample2": f"{ID_PREFIXES['sample']}-{uuid.uuid4().hex[:6]}",
        }

        xml_response = get_samples_xml(mock_samples, project_id=final_project_id)
        return Response(content=xml_response, media_type=MEDIA_TYPE_XML)
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@router.post("/samples/batch/create")
async def create_samples(request: Request):
    """Create batch of samples - returns hardcoded success response"""
    try:
        body = await request.body()
        samples_data = parse_samples_from_xml(body.decode())

        # Create mock sample responses
        created_samples = []
        sample_map = {}  # Add this
        for sample_data in samples_data:
            sample_id = f"{ID_PREFIXES['sample']}-{uuid.uuid4().hex[:6]}"
            created_samples.append({"id": sample_id, "name": sample_data["name"]})
            sample_map[sample_data["name"]] = sample_id  # Add this

        xml_response = get_samples_xml(created_samples)

        # Return map if it's a microbial order
        if "Strain" in str(body):  # Simple check for microbial orders
            return sample_map

        return Response(content=xml_response, media_type=MEDIA_TYPE_XML)
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
