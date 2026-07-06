import requests

from foundational_api import FoundationalAPIClient

# Constants — fill these in with your own values.
API_KEY_ID = "your_api_key_id"
API_KEY_SECRET = "your_api_key_secret"

# A repository full name as it appears in your organization, e.g. "my-org/my-repo".
REPO_NAME = "my-org/my-repo"

# A PowerBI workspace id (a GUID). Only relevant if your organization has a
# PowerBI connector configured.
POWERBI_WORKSPACE_ID = "11111111-2222-3333-4444-555555555555"


def list_repos_example(api_client: FoundationalAPIClient) -> None:
    """Read-only: list every repository in the organization (including offboarded ones)."""
    result = api_client.list_repos()
    repos = result.get("repos", [])
    print(f"\nOrganization has {len(repos)} repositories:")
    for repo in repos:
        print(f"  - {repo}")


def list_powerbi_workspaces_example(api_client: FoundationalAPIClient) -> None:
    """Read-only: list the workspaces configured on the org's PowerBI connector.

    Skips gracefully if the organization has no PowerBI connector (HTTP 404).
    """
    try:
        result = api_client.list_powerbi_workspaces()
    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            print("\nNo PowerBI connector configured for this organization; skipping.")
            return
        raise

    workspace_ids = result.get("workspaceIds", [])
    print(f"\nPowerBI connector has {len(workspace_ids)} configured workspaces:")
    for workspace_id in workspace_ids:
        print(f"  - {workspace_id}")


def trigger_onboarding_example(api_client: FoundationalAPIClient) -> None:
    """Mutating: (re-)onboard REPO_NAME, reviving it if it was previously offboarded.

    Not called by default — uncomment the call in main() to run it.
    """
    api_client.trigger_repo_onboarding(REPO_NAME)
    print(f"\nTriggered onboarding for '{REPO_NAME}'.")


def offboard_repo_example(api_client: FoundationalAPIClient) -> None:
    """Mutating: offboard REPO_NAME and its connectors.

    Not called by default — uncomment the call in main() to run it. Scan history
    is preserved; re-trigger onboarding to bring the repo back.
    """
    api_client.offboard_repo(REPO_NAME)
    print(f"\nOffboarded '{REPO_NAME}'.")


def add_powerbi_workspace_example(api_client: FoundationalAPIClient) -> None:
    """Mutating: add POWERBI_WORKSPACE_ID to the org's PowerBI connector.

    Not called by default — uncomment the call in main() to run it.
    """
    result = api_client.add_powerbi_workspace(POWERBI_WORKSPACE_ID)
    print(f"\nAdded {POWERBI_WORKSPACE_ID}. Configured workspaces: {result.get('workspaceIds', [])}")


def remove_powerbi_workspace_example(api_client: FoundationalAPIClient) -> None:
    """Mutating: remove POWERBI_WORKSPACE_ID from the org's PowerBI connector.

    Not called by default — uncomment the call in main() to run it.
    """
    result = api_client.remove_powerbi_workspace(POWERBI_WORKSPACE_ID)
    print(f"\nRemoved {POWERBI_WORKSPACE_ID}. Configured workspaces: {result.get('workspaceIds', [])}")


def main() -> None:
    api_client = FoundationalAPIClient(API_KEY_ID, API_KEY_SECRET)

    # Read-only examples — safe to run as-is.
    list_repos_example(api_client)
    list_powerbi_workspaces_example(api_client)

    # Mutating examples — these change your organization's configuration and
    # trigger scans. Uncomment deliberately, after setting the constants above.
    #
    # trigger_onboarding_example(api_client)
    # offboard_repo_example(api_client)
    # add_powerbi_workspace_example(api_client)
    # remove_powerbi_workspace_example(api_client)


if __name__ == "__main__":
    main()
