"""
Tests for the pyiikocloudapi package after httpx migration.

Verifies:
- Import correctness for sync and async clients
- Method parity between sync and async
- Correct HTTP client types (httpx, not requests)
- Context manager protocols
- Shared response processing logic
"""

import inspect
import json

# ---------------------------------------------------------------------------
# Import tests
# ---------------------------------------------------------------------------


class TestImports:
    def test_import_iiko_transport(self):
        from pyiikocloudapi import IikoTransport

        assert IikoTransport is not None

    def test_import_async_iiko_transport(self):
        from pyiikocloudapi import AsyncIikoTransport

        assert AsyncIikoTransport is not None

    def test_import_base_api(self):
        from pyiikocloudapi import BaseAPI

        assert BaseAPI is not None

    def test_import_async_base_api(self):
        from pyiikocloudapi import AsyncBaseAPI

        assert AsyncBaseAPI is not None

    def test_import_models(self):
        from pyiikocloudapi.models import BaseOrganizationsModel, CustomErrorModel

        assert CustomErrorModel is not None
        assert BaseOrganizationsModel is not None

    def test_import_process_response(self):
        from pyiikocloudapi._http import process_response

        assert callable(process_response)

    def test_import_from_api_module(self):
        """Backward compatibility: importing from api.py still works."""
        from pyiikocloudapi.api import IikoTransport

        assert IikoTransport is not None

    def test_import_base_from_api_module(self):
        """Backward compatibility: importing BaseAPI from api.py still works."""
        from pyiikocloudapi.api import BaseAPI

        assert BaseAPI is not None


# ---------------------------------------------------------------------------
# HTTP client type tests
# ---------------------------------------------------------------------------


class TestClientTypes:
    def test_sync_uses_httpx_client(self):
        from pyiikocloudapi.base import BaseAPI

        sig = inspect.signature(BaseAPI.__init__)
        session_param = sig.parameters["session"]
        annotation_str = str(session_param.annotation)
        assert "httpx.Client" in annotation_str
        assert "requests" not in annotation_str

    def test_async_uses_httpx_async_client(self):
        from pyiikocloudapi.async_api import AsyncBaseAPI

        sig = inspect.signature(AsyncBaseAPI.__init__)
        session_param = sig.parameters["session"]
        annotation_str = str(session_param.annotation)
        assert "httpx.AsyncClient" in annotation_str
        assert "requests" not in annotation_str


# ---------------------------------------------------------------------------
# MRO tests
# ---------------------------------------------------------------------------


class TestMRO:
    def test_sync_mro(self):
        from pyiikocloudapi import IikoTransport

        mro_names = [c.__name__ for c in IikoTransport.__mro__]
        assert mro_names[0] == "IikoTransport"
        assert mro_names[-1] == "object"
        assert "BaseAPI" in mro_names

    def test_async_mro(self):
        from pyiikocloudapi import AsyncIikoTransport

        mro_names = [c.__name__ for c in AsyncIikoTransport.__mro__]
        assert mro_names[0] == "AsyncIikoTransport"
        assert mro_names[-1] == "object"
        assert "AsyncBaseAPI" in mro_names

    def test_mro_order_matches(self):
        """Async MRO should mirror sync MRO ordering."""
        from pyiikocloudapi import AsyncIikoTransport, IikoTransport

        sync_mro = [c.__name__ for c in IikoTransport.__mro__]
        async_mro = [c.__name__ for c in AsyncIikoTransport.__mro__]
        # Remove prefix/suffix and compare the middle classes (mixin order)
        sync_mixins = sync_mro[1:-2]  # skip IikoTransport and BaseAPI, object
        async_mixins = async_mro[1:-2]  # skip AsyncIikoTransport and AsyncBaseAPI, object
        assert len(sync_mixins) == len(async_mixins)
        for sync_name, async_name in zip(sync_mixins, async_mixins):
            assert async_name == f"Async{sync_name}"


# ---------------------------------------------------------------------------
# Method parity tests
# ---------------------------------------------------------------------------


class TestMethodParity:
    def _get_public_methods(self, cls):
        return {name for name, _ in inspect.getmembers(cls, predicate=inspect.isfunction) if not name.startswith("_")}

    def test_async_has_all_sync_methods(self):
        from pyiikocloudapi import AsyncIikoTransport, IikoTransport

        sync_methods = self._get_public_methods(IikoTransport)
        async_methods = self._get_public_methods(AsyncIikoTransport)
        missing = sync_methods - async_methods
        assert not missing, f"Async is missing methods: {missing}"

    def test_async_extra_methods_are_expected(self):
        from pyiikocloudapi import AsyncIikoTransport, IikoTransport

        sync_methods = self._get_public_methods(IikoTransport)
        async_methods = self._get_public_methods(AsyncIikoTransport)
        extra = async_methods - sync_methods
        # Only 'ensure_token' should be extra (close exists on both sync and async)
        assert extra == {"ensure_token"}, f"Unexpected extra methods: {extra}"

    def test_async_api_methods_are_coroutines(self):
        """All non-static, non-sync-utility methods should be coroutines."""
        from pyiikocloudapi import AsyncIikoTransport

        non_coroutine_allowed = {
            "parse_webhook_order",
            "parse_webhook_reserve",  # static
            "check_status_code_token",  # sync utility
        }

        for name, method in inspect.getmembers(AsyncIikoTransport, predicate=inspect.isfunction):
            if name.startswith("_"):
                continue
            if name in non_coroutine_allowed:
                continue
            assert inspect.iscoroutinefunction(method), f"Method {name} should be a coroutine but is not"

    def test_static_methods_not_coroutines(self):
        from pyiikocloudapi.async_api import AsyncWebHook

        assert not inspect.iscoroutinefunction(AsyncWebHook.parse_webhook_order)
        assert not inspect.iscoroutinefunction(AsyncWebHook.parse_webhook_reserve)


# ---------------------------------------------------------------------------
# Context manager protocol tests
# ---------------------------------------------------------------------------


class TestContextManager:
    def test_sync_has_enter_exit(self):
        from pyiikocloudapi.base import BaseAPI

        assert hasattr(BaseAPI, "__enter__")
        assert hasattr(BaseAPI, "__exit__")

    def test_async_has_aenter_aexit(self):
        from pyiikocloudapi.async_api import AsyncBaseAPI

        assert hasattr(AsyncBaseAPI, "__aenter__")
        assert hasattr(AsyncBaseAPI, "__aexit__")
        assert inspect.iscoroutinefunction(AsyncBaseAPI.__aenter__)
        assert inspect.iscoroutinefunction(AsyncBaseAPI.__aexit__)

    def test_sync_has_close(self):
        from pyiikocloudapi.base import BaseAPI

        assert hasattr(BaseAPI, "close")

    def test_async_has_close(self):
        from pyiikocloudapi.async_api import AsyncBaseAPI

        assert hasattr(AsyncBaseAPI, "close")
        assert inspect.iscoroutinefunction(AsyncBaseAPI.close)


# ---------------------------------------------------------------------------
# process_response() tests
# ---------------------------------------------------------------------------


class TestProcessResponse:
    def test_returns_error_model_on_error_description(self):
        from pyiikocloudapi._http import process_response
        from pyiikocloudapi.models import CustomErrorModel

        data = {"errorDescription": "Something went wrong", "error": "SomeError"}
        result = process_response(
            response_content=json.dumps(data).encode(),
            response_status_code=400,
            return_dict=False,
            model_response_data=None,
            model_error=CustomErrorModel,
        )
        assert isinstance(result, CustomErrorModel)
        assert result.status_code == 400

    def test_returns_dict_when_return_dict_is_true(self):
        from pyiikocloudapi._http import process_response

        data = {"key": "value"}
        result = process_response(
            response_content=json.dumps(data).encode(),
            response_status_code=200,
            return_dict=True,
            model_response_data=None,
        )
        assert isinstance(result, dict)
        assert result == {"key": "value"}

    def test_returns_raw_dict_when_no_model(self):
        from pyiikocloudapi._http import process_response

        data = {"key": "value"}
        result = process_response(
            response_content=json.dumps(data).encode(),
            response_status_code=200,
            return_dict=False,
            model_response_data=None,
        )
        assert isinstance(result, dict)
        assert result == {"key": "value"}


# ---------------------------------------------------------------------------
# No requests references in source code
# ---------------------------------------------------------------------------


class TestNoRequestsReferences:
    """Ensure no Python source files reference the old requests library."""

    def _get_python_sources(self):
        import pathlib

        pkg_dir = pathlib.Path(__file__).parent.parent / "pyiikocloudapi"
        return list(pkg_dir.rglob("*.py"))

    def test_no_import_requests(self):
        for path in self._get_python_sources():
            content = path.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                # Skip comments and documentation files
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"') or stripped.startswith("'"):
                    continue
                assert "import requests" not in stripped, f"{path.name}:{i} still contains 'import requests'"

    def test_no_requests_session(self):
        for path in self._get_python_sources():
            content = path.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"') or stripped.startswith("'"):
                    continue
                assert "requests.Session" not in stripped, f"{path.name}:{i} still contains 'requests.Session'"

    def test_no_requests_exceptions(self):
        for path in self._get_python_sources():
            content = path.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"') or stripped.startswith("'"):
                    continue
                assert "requests.exceptions" not in stripped, f"{path.name}:{i} still contains 'requests.exceptions'"
