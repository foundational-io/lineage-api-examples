import os
import sys
from typing import Any, Dict, List, Literal, Optional

# Add to sys path the hello_lineage_graph directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hello_lineage_graph.foundational_api_wrapper import FoundationalAPIClient
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Foundational Data MCP")


def create_api_client() -> FoundationalAPIClient:
    # Get credentials from args or environment variables
    api_key = os.environ.get("FOUNDATIONAL_API_KEY")
    api_secret = os.environ.get("FOUNDATIONAL_API_SECRET")
    base_url = "https://api.foundational.io"

    if not api_key or not api_secret:
        raise ValueError(
            "API key and secret must be provided either as command line arguments "
            "or as environment variables (FOUNDATIONAL_API_KEY and FOUNDATIONAL_API_SECRET)"
        )

    # Initialize the Foundational API client
    try:
        client = FoundationalAPIClient(api_key, api_secret, base_url)
        if client is None:
            print("Error: Failed to initialize Foundational API client")
            sys.exit(1)
        return client
    except Exception as e:
        print(f"Error initializing Foundational API client: {e}")
        sys.exit(1)

# Initialize client as None so it can be set by run_server()
client: FoundationalAPIClient = create_api_client()


@mcp.tool()
def search(
    entity_type: Literal["TABLE", "COLUMN", "DASHBOARD", "DASHBOARD_COLUMN"],
    name: Optional[str] = None,
    parent_name: Optional[str] = None,
    database: Optional[str] = None,
    db_schema: Optional[str] = None,
    platform: Optional[str] = None,
    project_name: Optional[str] = None,
    full_matches_only: bool = False,
    limit: Optional[int] = None,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Search for entities in Foundational.
    """
    if client is None:
        raise RuntimeError("API client not initialized")
    return client.search(
        entity_type=entity_type,
        name=name,
        parent_name=parent_name,
        database=database,
        db_schema=db_schema,
        platform=platform,
        project_name=project_name,
        full_matches_only=full_matches_only,
        limit=limit,
        page_token=page_token,
    )

@mcp.tool()
def get_entity_details(entity_id: str) -> Dict[str, Any]:
    """
    Get details for a specific entity.
    """
    if client is None:
        raise RuntimeError("API client not initialized")
    return client.get_entity_details(entity_id)

@mcp.tool()
def get_downstream_dependencies(
    entity_id: str,
    name: Optional[str] = None,
    parent_name: Optional[str] = None,
    database: Optional[str] = None,
    db_schema: Optional[str] = None,
    platform: Optional[str] = None,
    project_name: Optional[str] = None,
    full_matches_only: bool = False,
    max_depth: Optional[int] = None,
    limit: Optional[int] = None,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get downstream dependencies for an entity.
    """
    if client is None:
        raise RuntimeError("API client not initialized")
    return client.get_downstream_dependencies(
        entity_id=entity_id,
        name=name,
        parent_name=parent_name,
        database=database,
        db_schema=db_schema,
        platform=platform,
        project_name=project_name,
        full_matches_only=full_matches_only,
        max_depth=max_depth,
        limit=limit,
        page_token=page_token,
    )

@mcp.tool()
def get_upstream_dependencies(
    entity_id: str,
    name: Optional[str] = None,
    parent_name: Optional[str] = None,
    database: Optional[str] = None,
    db_schema: Optional[str] = None,
    platform: Optional[str] = None,
    project_name: Optional[str] = None,
    full_matches_only: bool = False,
    max_depth: Optional[int] = None,
    limit: Optional[int] = None,
    page_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get upstream dependencies for an entity.
    """
    if client is None:
        raise RuntimeError("API client not initialized")
    return client.get_upstream_dependencies(
        entity_id=entity_id,
        name=name,
        parent_name=parent_name,
        database=database,
        db_schema=db_schema,
        platform=platform,
        project_name=project_name,
        full_matches_only=full_matches_only,
        max_depth=max_depth,
        limit=limit,
        page_token=page_token,
    )