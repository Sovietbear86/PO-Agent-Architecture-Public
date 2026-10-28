# GigaCode — NEXT ACTION (Public PR #4)

## A230R3.7-PUBLIC-PR4-INTEGRITY-QA — independent security/build gate

**Only QA, no code changes and no commits.** This is public-safe release preflight for `Sovietbear86/PO-Agent-Architecture-Public` PR #4, based on Draft PR #3 branch `feat/gigacode-public-deploy-health-skills`. Never merge, push, run write-capable AS21 MCP tools, or copy private Review history. Parent PR #3 and PR #4 must remain Draft until GREEN.

### Gate 0 — exact source revisions
1. Fetch origin. Record `LOCAL_HEAD`, `REMOTE_HEAD` and `TESTED_HEAD` for `feat/a230r3-community-migration`; all must match. Check working tree and never overwrite user changes.
2. Compare staged PR #4 against parent PR #3. Verify no PR #3 deploy and health skills are lost. Check 6 Core V4 files remain byte-identical to Public `main` (Public has known sanitized docstring distinct from private Review).
3. Scan entire PR head and changed-file history for keys, tokens, personal details, internal hosts, hardcoded employee IDs, corp `products.yaml` and secret-bearing configs. Do not print sensitive content. If found, STOP / RED.

### Gate 1 — Python imports, plugin registry, and schema contracts
1. Create isolated venv using documented public requirements; run `python -m compileall` on `mcp-swtr`, `task-api/app`, `po-agent-platform-v2/src`. Run import smoke for `task_catalog`, `_task_live_handlers`, `time_accounting_period`, `time_accounting_member`, `time_accounting_aggregate`, `goal_coverage`, `missing_goal_execution`, `api.v1`, `task_api`, `runtime_factory`.
2. Registry: `task.type_analysis` and `task.hierarchy` each have SkillSpec, CapabilitySpec, handler binding and UI contract. Import, instantiate and run relevant synthetic handlers. Preserve existing task skills, live task/search/read handlers, safe source scope, pagination and provenance.
3. New member/date worklogs capability must appear in V4 registry; its handler uses actual `GET /api/v1/swtr-read/work-logs/report`, and MCP `get_work_report_filter`. Check required author and date bounds; missing/partial source never shown as factual zero. Verify all import signatures match; prevent dropped fields `task_type_code` and `task_type_name`.
4. Public `swtr_assignee.py` retains configuration-based allowed spaces via `PRODUCTS_CONFIG_PATH`; never restore private hardcoded space list. Check `settings.py` retains local placeholders (no internal corporate hosts). All new experimental flags default OFF.
5. Check Python/package requirements for `yaml`, `pydantic-settings`, MCP and real deployment. Unit-tests must use synthetic task/member names and spaces. Missing coverage is an explicit release gate, not an automatic GREEN.

### Gate 2 — offline regression
1. Run all available Agent V4, Task API and public synthetic tests; report passed/failed/skipped with exact first broken import or assertion; distinguish missing dependency from product defect.
2. Run frontend install + build and UI unit/smoke for task rows, ranked `candidates`, worklog and sprint rows, and NO raw planner JSON.
3. Verify MCP-SWTR local startup and list-tools: **49 expected** with `get_work_report_filter`; `public_health_check.py` H0/H1/H2 local; 49 count in `DEPLOYMENT.md` and Public skills. Never claim live AS21 access based on fake health.
4. Test missing/invalid auth/space and read-only operation boundaries. Public server must not make tenant-wide unbounded AS21 scans. Do not use live write-capable MCP tools.

### Gate 3 — conditional integration (only if authorized)
1. Run `public-deploy` skill from **clean clone** in isolated environment, with secrets supplied only locally (never logged/committed); run `public-health-check` H0–H6.
2. If REAL AS21 credentials and network are available, compare bounded A (Agent) vs B (independent AS21 oracle) for date worklogs, task suit, hierarchy, context clarifications, sprint calendar vs lifetime and browser UI. Do not run broad scans.
3. If credentials, LLM or VPN unavailable, mark `INCOMPLETE` and list blocked gates. Prior Review A/B was conditionally GREEN, four LLM 429 E2E cases remain unverified; do not re-label.

### Final report format
Return in chat a table `gate | observed outcome | evidence/counts | status`, exact TESTED_HEAD and first failing boundary, security verdict, Core 6/6, and explicit PR #4 release recommendation. **GREEN** only if all mandatory safety/build/tests pass; **RED** for product defects or source secrets; **INCOMPLETE** for genuine missing environment/oracle. No fixes/commits. STOP.

### One-line command
Run A230R3.7-PUBLIC-PR4-INTEGRITY-QA from public branch GIGACODE_NEXT_ACTION.md. Sync HEAD; independent read-only QA, no code changes, detailed report and STOP.
