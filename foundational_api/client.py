from enum import Enum
from uuid import uuid4
from base64 import b64encode
from typing import Any, Literal, cast
from functools import cached_property

import requests


class APICertification(str, Enum):
    Certified = "certified"
    Deprecated = "deprecated"


class FoundationalAPIError(Exception):
    pass


class FoundationalAPIClient:
    API_VERSION = "v1"

    FD_REQUEST_ID_HEADER = "X-fd-request-id"

    TOKEN_EXCHANGE_PATH = "/api/v1/auth/api-token"

    def __init__(
            self,
            api_key_id: str,
            api_key_secret: str,
            base_url: str = "https://api.foundational.io",
    ) -> None:
        self._base_url = base_url
        self._api_key_id = api_key_id
        self._api_key_secret = api_key_secret
        self.session = requests.Session()

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        headers = self._generate_request_headers()
        url = f"{self._base_url}/api/{self.API_VERSION}/{path}"
        return self.session.get(url, headers=headers, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        headers = self._generate_request_headers()
        url = f"{self._base_url}/api/{self.API_VERSION}/{path}"
        return self.session.post(url, headers=headers, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        headers = self._generate_request_headers()
        url = f"{self._base_url}/api/{self.API_VERSION}/{path}"
        return self.session.delete(url, headers=headers, **kwargs)

    def search(
            self,
            entity_type: Literal["TABLE", "COLUMN", "DASHBOARD", "DASHBOARD_COLUMN"],
            name: str | None = None,
            parent_name: str | None = None,
            database: str | None = None,
            db_schema: str | None = None,
            platform: str | list[str] | None = None,
            project_name: str | None = None,
            certification: APICertification | None = None,
            full_matches_only: bool = False,
            limit: int | None = None,
            page_token: str | None = None,
    ) -> dict[str, Any]:
        params = dict(
            entity_type=entity_type,
            name=name,
            parent_name=parent_name,
            database=database,
            db_schema=db_schema,
            platform=platform,
            project_name=project_name,
            certification=certification,
            full_matches_only=full_matches_only,
            limit=limit,
            page_token=page_token,
        )
        params = {k: v for k, v in params.items() if v is not None}
        response = self.get("lineage/search", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def get_entity_details(
            self,
            entity_id: str,
    ) -> dict[str, Any]:
        params = dict(entity_id=entity_id)
        params = {k: v for k, v in params.items() if v is not None}
        response = self.get(f"lineage/entity/{entity_id}", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def get_pr_lineage_diff(
            self,
            repo_name: str,
            pr_number: int,
    ) -> dict[str, Any]:
        params = dict(
            repo_name=repo_name,
            pr_number=pr_number,
        )
        response = self.get("lineage/pr/issues/diff", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def get_pr_lineage_issues(
            self,
            repo_name: str,
            pr_number: int,
    ) -> dict[str, Any]:
        params = dict(
            repo_name=repo_name,
            pr_number=pr_number,
        )
        response = self.get("lineage/pr/issues", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def get_downstream_dependencies(
            self,
            entity_id: str,
            name: str | None = None,
            parent_name: str | None = None,
            database: str | None = None,
            db_schema: str | None = None,
            platform: str | list[str] | None = None,
            project_name: str | None = None,
            full_matches_only: bool = False,
            max_depth: int | None = None,
            limit: int | None = None,
            page_token: str | None = None,
    ) -> dict[str, Any]:
        return self._get_dependencies(
            entity_id,
            "downstream",
            name,
            parent_name,
            database,
            db_schema,
            platform,
            project_name,
            full_matches_only,
            max_depth,
            limit,
            page_token,
        )

    def get_upstream_dependencies(
            self,
            entity_id: str,
            name: str | None = None,
            parent_name: str | None = None,
            database: str | None = None,
            db_schema: str | None = None,
            platform: str | list[str] | None = None,
            project_name: str | None = None,
            full_matches_only: bool = False,
            max_depth: int | None = None,
            limit: int | None = None,
            page_token: str | None = None,
    ) -> dict[str, Any]:
        return self._get_dependencies(
            entity_id,
            "upstream",
            name,
            parent_name,
            database,
            db_schema,
            platform,
            project_name,
            full_matches_only,
            max_depth,
            limit,
            page_token,
        )

    def _get_dependencies(
            self,
            entity_id: str,
            direction: str,
            name: str | None = None,
            parent_name: str | None = None,
            database: str | None = None,
            db_schema: str | None = None,
            platform: str | list[str] | None = None,
            project_name: str | None = None,
            full_matches_only: bool = False,
            max_depth: int | None = None,
            limit: int | None = None,
            page_token: str | None = None,
    ) -> dict[str, Any]:
        params = dict(
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
        params = {k: v for k, v in params.items() if v is not None}
        response = self.get(f"lineage/entity/{entity_id}/{direction}", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    # ------------------------------------------------------------------
    # Onboarding / offboarding API (/api/v1/onboarding/...)
    #
    # The onboarding API must be enabled for your organization; when it is not,
    # these endpoints respond with HTTP 403. Contact Foundational support to
    # enable it.
    # ------------------------------------------------------------------

    def list_repos(self) -> dict[str, Any]:
        """List the organization's repositories.

        Includes offboarded repositories. Returns ``{"repos": ["org/repo", ...]}``.
        """
        response = self.get("onboarding/repos")
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def trigger_repo_onboarding(self, repo_name: str) -> None:
        """Trigger (re-)onboarding for a repository.

        ``repo_name`` is the repository full name, for example ``org/repository``.
        If the repo was previously offboarded this brings it back before scanning.
        Responds with HTTP 204 (no body); raises on 404 if the repo is not in the
        caller's organization.
        """
        response = self.post(f"onboarding/repos/{repo_name}/trigger")
        response.raise_for_status()

    def offboard_repo(self, repo_name: str) -> None:
        """Offboard a repository and its connectors.

        ``repo_name`` is the repository full name, for example ``org/repository``.
        Scan history is preserved and :meth:`trigger_repo_onboarding` brings the
        repo back. Responds with HTTP 204 (no body); raises on 404 if the repo is
        not in the caller's organization.
        """
        response = self.delete(f"onboarding/repos/{repo_name}")
        response.raise_for_status()

    def list_powerbi_workspaces(self) -> dict[str, Any]:
        """List the workspace ids configured on the org's PowerBI connector.

        Returns ``{"workspaceIds": ["<guid>", ...]}``. Raises on 404 if the org
        has no PowerBI connector, or 409 if more than one is configured.
        """
        response = self.get("onboarding/powerbi/workspaces")
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def add_powerbi_workspace(self, workspace_id: str) -> dict[str, Any]:
        """Add a workspace id (a GUID) to the org's PowerBI connector.

        Idempotent: a no-op if the workspace is already configured. Returns the
        updated ``{"workspaceIds": [...]}`` list.
        """
        response = self.post("onboarding/powerbi/workspaces", json={"workspaceId": workspace_id})
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def remove_powerbi_workspace(self, workspace_id: str) -> dict[str, Any]:
        """Remove a workspace id (a GUID) from the org's PowerBI connector.

        Idempotent: a no-op (not a 404) if the id is absent. Removing the last id
        resets the connector to autodiscovering all authorized workspaces. Returns
        the updated ``{"workspaceIds": [...]}`` list.
        """
        response = self.delete(f"onboarding/powerbi/workspaces/{workspace_id}")
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    @cached_property
    def _jwt_token(self) -> str:
        """
        returns a ready-to-use JWT token. the token is valid for 24 hours. token refresh not implemented in this sample.
        """
        response = self.session.post(
            f"{self._base_url}{self.TOKEN_EXCHANGE_PATH}",
            data=dict(client_id=self._api_key_id, client_secret=self._api_key_secret),
        )
        if response.status_code != 200:
            raise FoundationalAPIError(
                f"Failed to exchange API key for JWT token. "
                f"Status code: {response.status_code}, response: {response.text}"
            )
        return cast(str, response.json()["access_token"])

    def _generate_request_headers(self) -> dict[str, str]:
        return {
            "Authorization": self._jwt_token,
            "Accept": "application/json",
            self.FD_REQUEST_ID_HEADER: self._generate_request_id(),
        }

    def _generate_basic_auth_header(self) -> str:
        credentials = f"{self._api_key_id}:{self._api_key_secret}"
        # noinspection PyTypeChecker
        b64_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Basic {b64_credentials}"

    @staticmethod
    def _generate_request_id() -> str:
        return uuid4().hex
