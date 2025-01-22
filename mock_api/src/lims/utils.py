from typing import Dict, List
from xml.etree import ElementTree

from .constants import XML_NAMESPACES
from .exceptions import XMLParsingError


def parse_project_from_xml(xml_content: str) -> str:
    """Extract project name from project XML"""
    try:
        project_xml = ElementTree.fromstring(xml_content)
        return project_xml.find(".//name").text
    except Exception as e:
        raise XMLParsingError(f"Failed to parse project XML: {str(e)}") from e


def parse_samples_from_xml(xml_content: str) -> List[Dict]:
    """Parse samples data from XML"""
    try:
        samples_xml = ElementTree.fromstring(xml_content)
        samples_data = []

        for sample in samples_xml.findall(".//smp:samplecreation", XML_NAMESPACES):
            sample_data = {"name": sample.find("name").text, "udfs": {}}

            project_elem = sample.find("project")
            if project_elem is not None:
                project_uri = project_elem.get("uri", "")
                project_id = project_uri.split("/")[-1]
                sample_data["udfs"]["project_id"] = project_id

            for udf in sample.findall(".//udf:field", XML_NAMESPACES):
                name = udf.get("name")
                if name:
                    sample_data["udfs"][name] = udf.text

            samples_data.append(sample_data)
        return samples_data
    except Exception as e:
        raise XMLParsingError(f"Failed to parse samples XML: {str(e)}") from e


def parse_container_from_xml(xml_content: str) -> str:
    """Extract container name from container XML.
    Example input from CG:
    <con:details xmlns:con="http://genologics.com/ri/container">
        <con:container>
            <name>Sample-AM22-Testing-02</name>
            <type uri="http://host.docker.internal:8010/api/v2/containertypes/2"/>
        </con:container>
    </con:details>
    """
    try:
        container_xml = ElementTree.fromstring(xml_content)

        # Try both with and without namespace
        name_elem = container_xml.find(".//con:container/name", XML_NAMESPACES)
        if name_elem is None:
            name_elem = container_xml.find(".//name")

        if name_elem is None or not name_elem.text:
            raise XMLParsingError("Container name not found in XML")

        return name_elem.text
    except Exception as e:
        raise XMLParsingError(f"Failed to parse container XML: {str(e)}") from e
