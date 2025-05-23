from foundational_api_wrapper import FoundationalAPIClient

# Constants
ENTITY_TYPE = "TABLE"  # Example entity type
ENTITY_NAME = "table_name_to_search_for"
API_KEY_ID = "your_api_key_id"
API_KEY_SECRET = "your_api_key_secret"
SEARCH_PLATFORMS = ["POSTGRES", "SNOWFLAKE"]

def main():
    # Initialize the API wrapper
    api_client = FoundationalAPIClient(API_KEY_ID, API_KEY_SECRET)

    # Search for the entity
    search_results = api_client.search(entity_type=ENTITY_TYPE, name=ENTITY_NAME, platform=SEARCH_PLATFORMS)
    if not search_results.get('entities'):
        print(f"Entity '{ENTITY_NAME}' not found.")
        return

    entity_id = search_results['entities'][0]['id']  # Get the ID of the first matching entity

    # Get downstream dependencies
    downstreams = api_client.get_downstream_dependencies(entity_id)
    print("\nDownstream Dependencies:")
    print(downstreams)

    page_token = downstreams.get('pageToken', None)
    while page_token is not None:
        downstreams = api_client.get_downstream_dependencies(entity_id, page_token=page_token)
        print("\nMore Downstream Dependencies:")
        print(downstreams)

        page_token = downstreams.get('pageToken', None)

    # Get upstream dependencies
    upstreams = api_client.get_upstream_dependencies(entity_id)
    print("\nUpstream Dependencies:")
    print(upstreams)

    page_token = upstreams.get('pageToken', None)
    while page_token is not None:
        upstreams = api_client.get_upstream_dependencies(entity_id, page_token=page_token)
        print("\nMore Upstream Dependencies:")
        print(upstreams)

        page_token = upstreams.get('pageToken', None)


if __name__ == "__main__":
    main()