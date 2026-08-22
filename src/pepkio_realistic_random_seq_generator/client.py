from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel

from .config import TOOL_ID, get_default_api_key, get_default_base_url
from .exceptions import PepkioAPIError, PepkioAuthError, PepkioHTTPError
from .models import RunResult, SequenceInput


class PepkioClient:
    """Python client for Pepkio realistic-random-seq-generator tool."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        httpx_client: Optional[httpx.Client] = None,
    ):
        self.base_url = (base_url or get_default_base_url()).rstrip("/")
        self.api_key = api_key or get_default_api_key(self.base_url)
        self.timeout = timeout
        self._custom_httpx_client = httpx_client

    def _get_client(self) -> httpx.Client:
        if self._custom_httpx_client is not None:
            return self._custom_httpx_client
        verify = False if "localtest.me" in self.base_url else True
        return httpx.Client(timeout=self.timeout, verify=verify)

    def get_manifest(self) -> Dict[str, Any]:
        """Fetch the tool manifest containing input schema and examples."""
        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/manifest"
        headers = {"Accept": "application/json"}

        client = self._get_client()
        try:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                raise PepkioHTTPError(
                    status_code=response.status_code,
                    message=f"Failed to fetch manifest: {response.text}",
                    body=response.text,
                )
            return response.json()
        finally:
            if self._custom_httpx_client is None:
                client.close()

    def run(
        self,
        input_data: Union[Dict[str, Any], SequenceInput],
        idempotency_key: Optional[str] = None,
        label: Optional[str] = None,
        share: Optional[str] = None,
    ) -> RunResult:
        """
        Run the realistic-random-seq-generator tool.

        :param input_data: Input parameters dict or SequenceInput model.
        :param idempotency_key: Optional key for idempotent runs.
        :param label: Optional run label.
        :param share: Optional sharing setting.
        :return: RunResult object.
        """
        if not self.api_key:
            raise PepkioAuthError(
                "PEPKIO_API_KEY is required to run tools. "
                "Provide api_key in constructor or set PEPKIO_API_KEY environment variable."
            )

        if isinstance(input_data, BaseModel):
            payload_input = input_data.model_dump(exclude_none=True)
        elif isinstance(input_data, dict):
            payload_input = input_data
        else:
            raise ValueError("input_data must be a dict or SequenceInput instance")

        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/run"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        options: Dict[str, Any] = {}
        if idempotency_key:
            options["idempotency_key"] = idempotency_key
        if label:
            options["label"] = label
        if share:
            options["share"] = share

        payload: Dict[str, Any] = {"input": payload_input}
        if options:
            payload["options"] = options

        client = self._get_client()
        try:
            response = client.post(url, json=payload, headers=headers)

            if response.status_code in (401, 403):
                raise PepkioAuthError(
                    f"Authentication failed (HTTP {response.status_code}): {response.text}"
                )
            if response.status_code >= 400:
                raise PepkioHTTPError(
                    status_code=response.status_code,
                    message=(
                        f"API request failed with status {response.status_code}: "
                        f"{response.text}"
                    ),
                    body=response.text,
                )

            data = response.json()

            # Check for error in response body
            top_error = data.get("error")
            if top_error:
                raise PepkioAPIError(f"Tool run error: {top_error}", details=data)

            res_obj = data.get("result")
            result_error = res_obj.get("error") if isinstance(res_obj, dict) else None
            if result_error:
                raise PepkioAPIError(f"Tool execution error: {result_error}", details=data)

            return RunResult(**data)
        finally:
            if self._custom_httpx_client is None:
                client.close()

    def get_run(self, run_id: str) -> RunResult:
        """
        Fetch status and result of a run by runId.

        :param run_id: The ID of the run to fetch.
        :return: RunResult object.
        """
        url = f"{self.base_url}/api/tools/v1/runs/{run_id}"
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        client = self._get_client()
        try:
            response = client.get(url, headers=headers)
            if response.status_code in (401, 403):
                raise PepkioAuthError(
                    f"Authentication failed (HTTP {response.status_code}): {response.text}"
                )
            if response.status_code >= 400:
                raise PepkioHTTPError(
                    status_code=response.status_code,
                    message=f"Failed to get run {run_id}: {response.text}",
                    body=response.text,
                )

            data = response.json()
            if data.get("error"):
                raise PepkioAPIError(f"Run error: {data['error']}", details=data)

            return RunResult(**data)
        finally:
            if self._custom_httpx_client is None:
                client.close()
