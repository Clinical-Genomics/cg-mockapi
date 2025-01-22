from datetime import datetime

from .constants import BASE_URI, XML_NAMESPACES


def get_researcher_xml(username: str | None = None) -> str:
    """Get researcher XML response"""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<res:researchers xmlns:res="{XML_NAMESPACES['res']}">
    <researcher uri="{BASE_URI}/researchers/1">
        <first-name>Mock</first-name>
        <last-name>Researcher</last-name>
        <username>{username or "mock_user"}</username>
        <email>mock@example.com</email>
        <lab uri="{BASE_URI}/labs/1" />
    </researcher>
</res:researchers>"""


def get_project_xml(project_id: str, project_name: str) -> str:
    """Get project XML response"""
    return f"""<?xml version='1.0' encoding='utf-8'?>
<prj:project xmlns:prj="{XML_NAMESPACES['prj']}" uri="{BASE_URI}/projects/{project_id}">
    <name>{project_name}</name>
    <id>{project_id}</id>
    <researcher uri="{BASE_URI}/researchers/1" />
    <date>{datetime.now().isoformat()}</date>
</prj:project>"""


def get_container_batch_xml(container_id: str, container_name: str) -> str:
    """Generate container batch XML response."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<con:details xmlns:con="{XML_NAMESPACES['con']}">
    <link uri="{BASE_URI}/containers/{container_id}?name={container_name}">
        <name>{container_name}</name>
    </link>
</con:details>"""


def get_container_xml(container_id: str, name: str) -> str:
    """Get container XML response."""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<con:container xmlns:con="{XML_NAMESPACES['con']}">
    <name>{name}</name>
    <type uri="{BASE_URI}/containertypes/2"/>
</con:container>"""


def get_samples_xml(samples, project_id: str | None = None) -> str:
    """Generate samples XML response."""
    if not samples:
        return f"""<?xml version="1.0" encoding="utf-8"?>
<sam:samples xmlns:sam="{XML_NAMESPACES['smp']}"/>"""

    if project_id:
        # Format for get_samples response
        if isinstance(samples, dict):
            # When map_ids=True, samples is a dict of name:id
            sample_entries = []
            for sample_name, sample_id in samples.items():
                sample_entries.append(
                    f"""<sam:sample uri="{BASE_URI}/samples/{sample_id}">
                        <name>{sample_name}</name>
                        <date-received>{datetime.now().isoformat()}</date-received>
                        <project uri="{BASE_URI}/projects/{project_id}"/>
                        <artifact uri="{BASE_URI}/artifacts/{sample_id}">
                            <type>Analyte</type>
                        </artifact>
                    </sam:sample>"""
                )

            return f"""<?xml version="1.0" encoding="utf-8"?>
<sam:samples xmlns:sam="{XML_NAMESPACES['smp']}">
    {"".join(sample_entries)}
</sam:samples>"""
    else:
        # Format for create_samples response
        return f"""<?xml version="1.0" encoding="utf-8"?>
<smp:details xmlns:smp="{XML_NAMESPACES['smp']}">
    {"".join([f'<link uri="{BASE_URI}/samples/{sample["id"]}"><name>{sample["name"]}</name></link>' 
              for sample in samples])}
</smp:details>"""
