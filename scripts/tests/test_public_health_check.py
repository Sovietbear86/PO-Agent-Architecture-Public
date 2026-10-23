"""Offline tests for the credential-free public deployment health checker."""
from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import public_health_check as health  # noqa: E402


class HealthCheckTests(unittest.TestCase):
    def test_rejects_external_probe_destinations(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            health._local_url("https://external.invalid")
        with self.assertRaises(argparse.ArgumentTypeError):
            health._local_url("http://localhost:8003/?token=example")
        self.assertEqual(health._local_url("http://127.0.0.1:8003/"), "http://127.0.0.1:8003")

    def test_missing_source_verification_is_not_green(self):
        args = argparse.Namespace(
            task_api_url="http://127.0.0.1:8003",
            agent_url="http://127.0.0.1:8004",
            frontend_url="http://127.0.0.1:5175",
            task_code=None, probe_agent=False, timeout=1.0, agent_timeout=1.0,
        )
        with patch.object(health, "_check", side_effect=lambda name, *a, **kw: {
            "name": name, "status": "GREEN", "http": 200, "elapsed_ms": 1, "detail": "OK"
        }):
            result = health.run(args)
        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(result["checks"][-2]["name"], "H5_REAL_AS21")
        self.assertEqual(result["checks"][-1]["name"], "H6_LLM_AGENT")

    def test_source_requires_exact_actual_unit_code(self):
        self.assertEqual(health._task({"task_code": "PAY-123", "unit": {"code": "PAY-123"}}, "PAY-123"),
                         (True, "SOURCE_TASK_CODE_MATCHED"))
        self.assertFalse(health._task({"task_code": "PAY-123", "unit": {}}, "PAY-123")[0])
        self.assertFalse(health._task({"task_code": "PAY-123", "unit": {"code": "PAY-456"}}, "PAY-123")[0])
        self.assertFalse(health._task({"task_code": "PAY-123", "errorType": "FAILED"}, "PAY-123")[0])

    def test_mcp_registry_requires_source_read_tool(self):
        self.assertTrue(health._mcp_health({
            "status": "connected", "tool_count": 48, "read_unit": True
        })[0])
        self.assertFalse(health._mcp_health({
            "status": "connected", "tool_count": 48, "read_unit": False
        })[0])

    def test_agent_requires_v4_and_source_ready(self):
        valid = {"status": "healthy", "adapter": "task-api", "source_status": "healthy",
                 "agent_core_v4_enabled": True, "agent_core_v4_ready": True}
        self.assertTrue(health._agent_health(valid)[0])
        self.assertFalse(health._agent_health({**valid, "adapter": "fake"})[0])
        self.assertFalse(health._agent_health({**valid, "source_status": "degraded"})[0])

    def test_agent_completing_without_evidence_is_not_green(self):
        valid = {"status": "COMPLETED", "runtime": "agent_core_v4",
                 "evidence": [{"source": "REAL_AS21"}]}
        self.assertTrue(health._agent_query(valid)[0])
        self.assertFalse(health._agent_query({**valid, "evidence": []})[0])
        self.assertFalse(health._agent_query({**valid, "status": "FAILED"})[0])
        self.assertFalse(health._agent_query({**valid, "runtime": "legacy_harness"})[0])

    def test_no_raw_exception_or_http_body_in_error(self):
        # _fetch never reads HTTP error response bodies.
        from io import BytesIO
        from urllib.error import HTTPError
        from unittest.mock import patch as _patch
        error = HTTPError("http://127.0.0.1:8003/health", 403, "Denied", {}, BytesIO(b"secret-should-not-log"))
        with _patch.object(health, "urlopen", side_effect=error):
            code, payload, classification = health._fetch("http://127.0.0.1:8003/health")
        self.assertEqual((code, payload, classification), (403, None, "HTTP_ERROR"))


if __name__ == "__main__":
    unittest.main()
