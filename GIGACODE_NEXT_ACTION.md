# GigaCode — CURRENT NEXT ACTION

## A230R3.9-R2-PUBLIC-H3-COLD-MCP-HEALTH-REGATE

**QA ONLY.** Do not change application code, configs, Core V4, tests, Git history, source/AS21 data. No commits, pushes or merges. Keep Review services and worktree untouched; maintain Public PR #3/#4 Draft. Use fresh isolated Public clone and free local ports, never stop user's running services.

### Prior independent evidence
A230R3.9 (TESTED_HEAD `d8c7cd0`) confirmed real Playwright Chromium browser DOM: six tabs, business rows, task types, hierarchies/epics, member worklogs, candidate recommendations, empty/error state and absence of raw planner JSON, correct Public Vite /api proxy. Bounded REAL AS21 oracle GREEN. GitHub six-job CI successful, security scan passed, Core 6/6 unchanged. Three of four previously blocked LLM E2E cases closed, fourth remained partial (plural-week parsing / created-date long source timeout). Report verdict RELEASE_INCOMPLETE due to official H3 source readiness failing at 5s cold stdio MCP initialization (while actual Task API, H5/H6, source reads GREEN). No code changes made by QA.
Owner changes after `d8c7cd0`:
- `cac76e5` raised **only health-probe** adapter bound from 5 to 15 seconds for real cold stdio (~9–10 s) without changing task reads; possible elapsed >15s at outer health client.
- `6d42596` cleaned formatting of that docstring.
- `9df478f` adds bounded 20s for **H3** of official health script only, preserving other probes default timeout and strict source-health validator.
- `3ffd41e` adds offline assertions H3=20s, H2/H4=15s. All changes OUTSIDE frozen Core V4. Do not treat them as QA-verified until tests run.

### R2 required gates
1. `git fetch`, compare local=remote=running clone TESTED_HEAD. Identify exact production delta from `d8c7cd0` — health-probe budget and H3 check only. Verify six Core V4 Public blobs identical to Public main. Scan proposed PR branch with `python3 scripts/prepublish_scan.py` exit 0 and check internal secrets.
2. Run GitHub Community CI for actual TESTED_HEAD (six jobs: sanitize, backend, frontend, health-tool, offline-agent-regression, offline-task-api-regression), full local available offline tests (prior V4 50/50, Task API 15/15, health 9/9; count changes). Do not fake success.
3. Rebuild isolated Public stack with **own** MCP stdio, Task API, Agent, Vite proxy, never using Review services or occupied ports. On cold run (not prewarmed) time `/api/v1/swtr-read/health` and Agent `/api/v1/health`; verify H3 `source_status=healthy` from REAL AS21, not from fake/local source or a response copied from earlier cached check. Check no source mutation, no unbounded queries, no fabricated zero.
4. Run official `scripts/public_health_check.py` with configured isolated URLs and one authorized existing task code + `--probe-agent`. Expect **H0–H6 GREEN, exit 0** in cold and warm conditions. Note timings. Verify H3 transport timeout remains bounded (20s), source probe 15s and frontend H4 uses text/html.
5. Recheck real browser via existing Playwright (or equivalent) for at least task row, worklogs, sources, candidates, no raw planner JSON, `/api` strictly isolated Public proxy. Recheck independent bounded REAL AS21 A/B on one task; preserve previously observed R1 provenance without unnecessary repeat scans.
6. Previously incomplete fourth LLM E2E: plural-week creation-period interpretation and explicit date continuation. If run, use max two bounded attempts and an independent source oracle; mark remaining source unavailable/timeouts and grammar gap as OPEN, don't broaden scope or assert this is fixed by H3 patch.
7. Preserve known OPEN: Review reliability incident (separate), created-period plural-week grammar, session auth/ownership absent, full canonical default-port host test optional. GigaCode has no authorization to modify Review.
8. Report TESTED_HEAD, security, exact tests/CI, cold+warmed H3 timings/status, H0–H6, UI browser smoke, 49 MCP tools, Core 6/6, AS21 A/B and any remaining release blockers. Return `PUBLIC_RELEASE_GREEN` only if all mandatory gates pass; else `RELEASE_INCOMPLETE` or `RED`. No commits, stop.

### Command
Run A230R3.9-R2-PUBLIC-H3-COLD-MCP-HEALTH-REGATE from Public GIGACODE_NEXT_ACTION.md. QA only. Fresh isolated cold and warm H0–H6, independent REAL AS21, 6-job CI, browser smoke and Core 6/6. No changes/commits. Report and STOP.
