# GigaCode — CURRENT NEXT ACTION

## A230R3.9-R2-PUBLIC-HEALTH-COLD-STDIO-REGATE — independent QA

**ONLY QA.** Do not modify code, tests, docs, Core V4, or config. No commit/push/merge. Do not stop user Review services; keep existing Review branch/worktree unchanged. Public PR #3 and PR #4 remain Draft. Fetch origin and prove LOCAL_HEAD=REMOTE_HEAD=TESTED_HEAD for Public `feat/a230r3-community-migration`.

### Evidence and issue
- Prior A230R3.9 browser DOM tests on `d8c7cd0` were GREEN: all 6 tabs, task/type/hierarchy/worklog/assignee candidates, no raw planner JSON, bounded REAL AS21 parity; GitHub six-job CI GREEN. LLM 429 cleared for 3 of 4 cases, fourth created-date case PARTIAL due known regex/slow source.
- **Official H0–H6 returned RED solely at H3**. `source_health()` in `po-agent-platform-v2/src/po_agent/adapters/task_api.py` previously capped probe timeout at 5.0s, but bounded cold stdio MCP round-trip can take ~9–10s. Agent `/api/v1/health` marked source degraded with `ReadTimeout`, while H2/H5/H6 direct real reads were all GREEN.
- Owner outside-Core fix `cac76e5`: raised **bounded cap** from 5.0s to 15.0s (still min(base timeout, 15)). No API, MCP or Core changes. This change requires independent verification; do NOT claim success from code review alone.
- Known broader Review incident (FAILED task query + stale snapshot refresh) remains independently open; this Public H3 change is not a proven fix for Review.

### Mandatory gates
1. Exact owner diff vs `d8c7cd0`: prove only Task API adapter source-health timeout and this next_action changed. Frozen 6 Core V4 blobs must match Public main. `python3 scripts/prepublish_scan.py` exit 0.
2. Test source-health cold startup and repeat (at least 3 times). Instrument or safely observe HTTP duration. All H0–H6 via **official** `scripts/public_health_check.py` against isolated Public stack must be GREEN (exit 0), including H3 `source_status=healthy`. No fake oracle. Test one deliberately slow >15s probe in offline synthetic test to prove fail-closed remains, and no tenant-wide scans/writes.
3. Inspect actual `self._base_timeout_seconds`: verify >=15s in deployed settings for this scenario, since min(base,15) retains shorter configured timeouts. If base <15, classify as CONFIG/BLOCKER and provide correct safe owner change proposal; do not edit runtime code yourself.
4. Full regression: declared dependencies, Agent V4, Task API, health tests, 49 MCP tools, frontend build, source scoped read-only, public-deploy and public-health-check skills retained, all 6 CI jobs for tested commit. Confirm no 429 and no extra LLM load; source checks bounded.
5. Browser DOM coverage from previous run can be used only if no UI/proxy changes; sanity smoke as feasible. Test H3 & H5/H6 source consistency on the *same* isolated Public task-api and agent; verify no Review port access.
6. Report exact tested HEAD, H0–H6 table, H3 warm/cold timing, failed boundary if any, security, Core 6/6, official CI results, and `PUBLIC_RELEASE_GREEN` only if mandatory gates all pass. Otherwise `RELEASE_INCOMPLETE` or RED. The four E2E cases include a known remaining creation-period limitation; classify open accurately. No PR merge. STOP.

### Short GigaCode command
Run A230R3.9-R2-PUBLIC-HEALTH-COLD-STDIO-REGATE from latest Public GIGACODE_NEXT_ACTION.md. Sync HEAD, independently test H3 cold/warm 15s bounded health and full H0–H6, regress/security/CI/Core. QA-only, report and STOP.
