from typing import Dict

from mock_api.src.config import settings

# XML namespaces used in LIMS responses
XML_NAMESPACES: Dict[str, str] = {
    "smp": "http://genologics.com/ri/sample",
    "prj": "http://genologics.com/ri/project",
    "con": "http://genologics.com/ri/container",
    "res": "http://genologics.com/ri/researcher",
    "udf": "http://genologics.com/ri/userdefined",
}

# Constants for generating IDs
ID_PREFIXES = {"project": "PRJ", "sample": "SMP"}

# API Configuration
LIMS_PREFIX = "/api/v2"
BASE_URI = f"{settings.lims_host}{LIMS_PREFIX}"
MEDIA_TYPE_XML = "application/xml"
