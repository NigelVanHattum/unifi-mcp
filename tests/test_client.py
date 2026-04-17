"""Tests for client.py — HTTP helpers."""

import pytest
import httpx
from unittest.mock import patch, MagicMock
import client


# ---------------------------------------------------------------------------
# omit()
# ---------------------------------------------------------------------------

class TestOmit:
    def test_removes_specified_keys(self):
        result = client.omit({"a": 1, "b": 2, "c": 3}, "b")
        assert result == {"a": 1, "c": 3}

    def test_removes_multiple_keys(self):
        result = client.omit({"siteId": "x", "deviceId": "y", "action": "RESTART"},
                             "siteId", "deviceId")
        assert result == {"action": "RESTART"}

    def test_strips_none_values(self):
        result = client.omit({"a": 1, "b": None, "c": 0})
        assert result == {"a": 1, "c": 0}

    def test_strips_none_and_omits_keys(self):
        result = client.omit({"siteId": "x", "limit": None, "offset": 10}, "siteId")
        assert result == {"offset": 10}

    def test_empty_dict(self):
        assert client.omit({}) == {}

    def test_all_removed(self):
        result = client.omit({"a": 1}, "a")
        assert result == {}

    def test_false_not_stripped(self):
        """False is a valid value — only None stripped."""
        result = client.omit({"enabled": False, "x": None})
        assert result == {"enabled": False}

    def test_zero_not_stripped(self):
        result = client.omit({"offset": 0})
        assert result == {"offset": 0}


# ---------------------------------------------------------------------------
# api()
# ---------------------------------------------------------------------------

def _mock_response(json_data=None, status=200, content=b"{}"):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status
    resp.content = content
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


class TestApi:
    def test_get_returns_json(self):
        mock_resp = _mock_response(json_data={"data": [1, 2]}, content=b'{"data":[1,2]}')
        with patch("client._make_client") as mk:
            mk.return_value.__enter__.return_value.request.return_value = mock_resp
            result = client.api("GET", "/info")
        assert result == {"data": [1, 2]}

    def test_empty_response_returns_success(self):
        mock_resp = _mock_response(content=b"")
        with patch("client._make_client") as mk:
            mk.return_value.__enter__.return_value.request.return_value = mock_resp
            result = client.api("DELETE", "/sites/s1/devices/d1")
        assert result == {"status": "success"}

    def test_passes_params(self):
        mock_resp = _mock_response(json_data={}, content=b"{}")
        with patch("client._make_client") as mk:
            req = mk.return_value.__enter__.return_value.request
            req.return_value = mock_resp
            client.api("GET", "/sites", params={"limit": 10, "offset": None})
        # None params stripped before call
        call_kwargs = req.call_args
        assert call_kwargs.kwargs["params"] == {"limit": 10}

    def test_passes_body(self):
        mock_resp = _mock_response(json_data={"id": "new"}, content=b'{"id":"new"}')
        with patch("client._make_client") as mk:
            req = mk.return_value.__enter__.return_value.request
            req.return_value = mock_resp
            client.api("POST", "/sites/s1/devices", body={"macAddress": "aa:bb:cc"})
        call_kwargs = req.call_args
        assert call_kwargs.kwargs["json"] == {"macAddress": "aa:bb:cc"}

    def test_raises_on_http_error(self):
        mock_resp = _mock_response(status=404)
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=mock_resp
        )
        with patch("client._make_client") as mk:
            mk.return_value.__enter__.return_value.request.return_value = mock_resp
            with pytest.raises(httpx.HTTPStatusError):
                client.api("GET", "/sites/bad")

    def test_null_params_become_none(self):
        """All-None params dict → passes None (not empty dict) to request."""
        mock_resp = _mock_response(json_data={}, content=b"{}")
        with patch("client._make_client") as mk:
            req = mk.return_value.__enter__.return_value.request
            req.return_value = mock_resp
            client.api("GET", "/sites", params={"offset": None})
        call_kwargs = req.call_args
        assert call_kwargs.kwargs["params"] is None
