from foundational_api_wrapper import FoundationalAPIClient

# Constants
ENTITY_TYPE = "TABLE"  # Example entity type
ENTITY_NAME = "stg_customers"
#API_KEY_ID = "your_api_key_id"
API_KEY_ID = "0a36d191-fb98-480a-a59b-1caf749192ef"
# API_KEY_SECRET = "your_api_key_secret"
API_KEY_SECRET = "5ac0e25f-cc2c-47e6-b833-64747c627a09"

def main():
    # Initialize the API wrapper
    api_client = FoundationalAPIClient(API_KEY_ID, API_KEY_SECRET)

    # Search for the entity
    search_results = api_client.search(entity_type=ENTITY_TYPE, name=ENTITY_NAME)
    if not search_results.get('entities'):
        print(f"Entity '{ENTITY_NAME}' not found.")
        return

    entity_id = search_results['entities'][0]['id']  # Get the ID of the first matching entity

    # Get downstream dependencies
    downstreams = api_client.get_downstream_dependencies(entity_id)
    print("\nDownstream Dependencies:")
    print(downstreams)

    # Get upstream dependencies
    upstreams = api_client.get_upstream_dependencies(entity_id)
    print("\nUpstream Dependencies:")
    print(upstreams)

if __name__ == "__main__":
    main()