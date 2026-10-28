#!/usr/bin/env python3
"""Read-only, credential-free local health gate for PO Agent Community.

Run from the public checkout:
    python3 scripts/public_health_check.py --task-code PAY-123 --probe-agent

Do not use synthetic task codes for certification. Never prints secrets, raw
AS21 task payloads or full LLM responses. STDOUT JSON is sanitized metadata.
Exit: 0 GREEN, 1 RED, 2 INCOMPLETE (missing source/LLM verification).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4

MAX_BYTES = 2 * 1024 * 1024
CODE_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
ROOT = Path(__file__).resolve().parents[1]


def _local_url(value: str) -> str:
    """Prevent accidental submission of scoped task probes to external hosts."""
    parsed = urlsplit(value)
    if (parsed.scheme != "http" or parsed.hostname not in
            {"localhost", "127.0.0.1", "::1"} or
            parsed.username or parsed.password or parsed.query or parsed.fragment or
            parsed.path not in {"", "/"}):
        raise argparse.ArgumentTypeError(
            "Only localhost http:// URLs without credentials, paths or query strings are accepted"
        )
    return value.rstrip("/")


def _fetch(url: str, *, payload: dict | None = None, timeout: float = 10.0,
           accept: str = "application/json") -> tuple[int | None, object, str | None]:
    """Return status, parsed JSON (or short HTML), sanitized error type."""
    if accept not in {"application/json", "text/html"}:
        raise ValueError("Unsupported health-check Accept header")
    headers = {"Accept": accept}
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urlopen(req, timeout=timeout) as response:
            status = response.status
            raw = response.read(MAX_BYTES + 1)
            ctype = response.headers.get("Content-Type", "")
            if len(raw) > MAX_BYTES:
                return status, None, "RESPONSE_TOO_LARGE"
            if "json" in ctype or url.endswith("/health") or url.endswith("/query"):
                try:
                    return status, json.loads(raw.decode("utf-8")), None
                except (UnicodeError, ValueError):
                    return status, None, "INVALID_JSON"
            return status, raw.decode("utf-8", errors="replace")[:10000], None
    except HTTPError as exc:
        # Never read/print response error body: upstream may include sensitive payloads.
        return exc.code, None, "HTTP_ERROR"
    except (TimeoutError, URLError, OSError) as exc:
        return None, None, type(exc).__name__
    except Exception as exc:  # defensive fail-closed, no secret-bearing exception strings
        return None, None, type(exc).__name__


def _check(name: str, url: str, valid, *, payload: dict | None = None,
           timeout: float = 10.0, accept: str = "application/json") -> dict:
    started = time.monotonic()
    status, body, error = _fetch(url, payload=payload, timeout=timeout, accept=accept)
    result = {"name": name, "status": "RED", "http": status,
              "elapsed_ms": round((time.monotonic() - started) * 1000),
              "detail": "UNVERIFIED"}
    if error:
        result["detail"] = error
        return result
    if status != 200:
        result["detail"] = "UNEXPECTED_HTTP_STATUS"
        return result
    try:
        ok, detail = valid(body)
    except (TypeError, ValueError, KeyError, AttributeError):
        ok, detail = False, "INVALID_RESPONSE_SHAPE"
    result["status"] = "GREEN" if ok else "RED"
    result["detail"] = detail
    return result


def _task_api_health(body: object) -> tuple[bool, str]:
    return (isinstance(body, dict) and body.get("status") == "healthy",
            "TASK_API_LIVE" if isinstance(body, dict) and body.get("status") == "healthy"
            else "TASK_API_NOT_HEALTHY")


def _mcp_health(body: object) -> tuple[bool, str]:
    ok = (isinstance(body, dict) and body.get("status") == "connected"
          and isinstance(body.get("tool_count"), int)
          and body["tool_count"] > 0
          and body.get("read_unit") is True)
    if not ok:
        return False, "MCP_NOT_CONNECTED_OR_READ_TOOL_MISSING"
    return True, "MCP_CONNECTED_TOOLS_" + str(body["tool_count"])


def _agent_health(body: object) -> tuple[bool, str]:
    ok = (isinstance(body, dict) and body.get("status") == "healthy"
          and body.get("adapter") == "task-api"
          and body.get("source_status") == "healthy"
          and body.get("agent_core_v4_enabled") is True
          and body.get("agent_core_v4_ready") is True)
    return ok, "V4_TASK_API_SOURCE_READY" if ok else "V4_OR_SOURCE_NOT_READY"


def _frontend(body: object) -> tuple[bool, str]:
    ok = isinstance(body, str) and bool(re.search(r'id=["\x27]root["\x27]', body))
    return ok, "FRONTEND_HTML_READY_NOT_BROWSER_PROVEN" if ok else "FRONTEND_HTML_INVALID"


def _task(body: object, code: str) -> tuple[bool, str]:
    if not isinstance(body, dict) or body.get("task_code") != code:
        return False, "TASK_CODE_NOT_CONFIRMED"
    unit = body.get("unit")
    ok = isinstance(unit, dict) and unit.get("code") == code
    return ok, "SOURCE_TASK_CODE_MATCHED" if ok else "SOURCE_UNIT_CODE_NOT_CONFIRMED"


def _agent_query(body: object) -> tuple[bool, str]:
    if not isinstance(body, dict):
        return False, "INVALID_AGENT_RESPONSE"
    status = body.get("status")
    ev = body.get("evidence")
    if status != "COMPLETED":
        # Safe status category only; never include raw agent answer/question.
        return False, "AGENT_" + (status if status in
            {"PARTIAL", "NEEDS_CLARIFICATION", "FAILED"} else "UNEXPECTED_STATUS")
    if not isinstance(ev, list) or not ev:
        return False, "COMPLETED_WITHOUT_SOURCE_EVIDENCE"
    if not any(isinstance(item, dict) and str(item.get("source") or "").lower()
               in {"as21", "real_as21", "swtr", "mcp-swtr"} for item in ev):
        return False, "COMPLETED_WITHOUT_AS21_EVIDENCE"
    if body.get("runtime") != "agent_core_v4":
        return False, "UNEXPECTED_RUNTIME"
    return True, "COMPLETED_V4_WITH_EVIDENCE"


def run(args: argparse.Namespace) -> dict:
    checks: list[dict] = []
    present = (ROOT / "mcp-swtr" / "mcp_server.py").is_file()
    checks.append({"name": "H0_MCP_SOURCE", "status": "GREEN" if present else "RED",
                   "detail": "BUNDLED_MCP_PRESENT" if present else "BUNDLED_MCP_MISSING",
                   "http": None, "elapsed_ms": 0})
    checks.append(_check("H1_TASK_API", args.task_api_url + "/health", _task_api_health,
                         timeout=args.timeout))
    checks.append(_check("H2_MCP", args.task_api_url + "/api/v1/swtr-read/health",
                         _mcp_health, timeout=args.timeout))
    checks.append(_check("H3_AGENT_V4", args.agent_url + "/api/v1/health",
                         _agent_health, timeout=args.timeout))
    checks.append(_check("H4_FRONTEND", args.frontend_url + "/", _frontend,
                         timeout=args.timeout, accept="text/html"))
    if args.task_code:
        code = args.task_code.upper()
        checks.append(_check(
            "H5_REAL_AS21", args.task_api_url + "/api/v1/swtr-read/tasks/" + quote(code),
            lambda data: _task(data, code), timeout=args.timeout))
    else:
        checks.append({"name": "H5_REAL_AS21", "status": "INCOMPLETE",
                       "detail": "REQUIRE_EXISTING_AUTHORIZED_TASK_CODE",
                       "http": None, "elapsed_ms": 0})
    if args.probe_agent and args.task_code:
        checks.append(_check(
            "H6_LLM_AGENT", args.agent_url + "/api/v1/query", _agent_query,
            payload={"query": "Покажи задачу " + args.task_code.upper(),
                     "session_id": "public-health-" + uuid4().hex},
            timeout=args.agent_timeout))
    else:
        checks.append({"name": "H6_LLM_AGENT", "status": "INCOMPLETE",
                       "detail": "LLM_PROBE_NOT_REQUESTED_OR_TASK_CODE_MISSING",
                       "http": None, "elapsed_ms": 0})
    verdict = ("RED" if any(x["status"] == "RED" for x in checks)
               else "INCOMPLETE" if any(x["status"] == "INCOMPLETE" for x in checks)
               else "GREEN")
    return {"verdict": verdict, "checks": checks,
            "note": "Health checks alone do not replace browser UI smoke or independent AS21 A/B oracle."}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task-api-url", type=_local_url, default="http://127.0.0.1:8003")
    p.add_argument("--agent-url", type=_local_url, default="http://127.0.0.1:8004")
    p.add_argument("--frontend-url", type=_local_url, default="http://127.0.0.1:5175")
    p.add_argument("--task-code", help="Existing AS21 task accessible to current token, e.g. PAY-123")
    p.add_argument("--probe-agent", action="store_true", help="Send one bounded LLM query for this task")
    p.add_argument("--timeout", type=float, default=15.0, help="Per HTTP check timeout (seconds)")
    p.add_argument("--agent-timeout", type=float, default=180.0, help="LLM query timeout (seconds)")
    p.add_argument("--json", action="store_true", help="Emit JSON only, without response bodies")
    args = p.parse_args(argv)
    if args.timeout <= 0 or args.agent_timeout <= 0 or args.timeout > 120 or args.agent_timeout > 300:
        p.error("timeouts must be positive; health <=120s, agent <=300s")
    if args.task_code and not CODE_RE.fullmatch(args.task_code.upper()):
        p.error("task code must be like PAY-123 (no wildcards, tenant scans or free text)")
    if args.probe_agent and not args.task_code:
        p.error("--probe-agent requires --task-code")
    result = run(args)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for check in result["checks"]:
            print(f'{check["name"]:16} {check["status"]:11} {check["detail"]} '
                  f'(http={check["http"]}, {check["elapsed_ms"]}ms)')
        print("VERDICT:", result["verdict"])
        print(result["note"])
    return {"GREEN": 0, "RED": 1, "INCOMPLETE": 2}[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
