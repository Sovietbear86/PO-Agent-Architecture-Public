# GigaCode — CURRENT NEXT ACTION

## A230R3.8-R2-PUBLIC-ISOLATED-UI-REGATE

**Independent QA ONLY.** No code changes, commits, pushes, merges, force operations, source/AS21 writes or killing existing user services. Review 8004/5175/3000 MUST stay untouched. Fetch origin, verify LOCAL_HEAD=REMOTE_HEAD=TESTED_HEAD on Public `feat/a230r3-community-migration`; test only the actual current HEAD in a fresh temporary clone. PR #4 and parent PR #3 remain Draft.

### Previous R1 evidence
R1 tested `4b493eb` on true clean isolated Public clone. Security and Core V4 6/6 GREEN; 15/15 Task API; V4 50/50; 49 MCP tools, 14 plugins/73 skills/75 caps/70 UI; H0–H3/H5/H6 GREEN and bounded REAL AS21 oracle matched. **H4 FRONTEND RED** for 2 causes:
1. `scripts/public_health_check.py` incorrectly requested JSON from a Vite SPA GET; Vite serves index.html to HTML Accept only.
2. `frontend/vite.config.ts` hardcoded port 5175 and backend proxy 8004 (occupied by user's Review), so isolated Vite on an alternate port was not wired to the isolated Agent.
R1 correctly returned `RELEASE_INCOMPLETE` without stopping Review.

### Owner changes for R2
- `03c7b13` Health check H4 sends `Accept: text/html` specifically, keeps JSON for API checks.
- `78b3211` Vite `PO_AGENT_DEV_UI_PORT` and `PO_AGENT_DEV_PROXY_PORT` configurable with loopback-only proxy destination and unprivileged ports, default 5175/8004.
- `d6ff44a` H4 and HTML Accept offline tests.
- `2255e1d` Public DEPLOYMENT.md isolated-port guidance.
- `bded7e4` Community CI now includes synthetic Agent/Task API tests and triggers for stacked PR #4. Review and execute CI, and report failing checks independently; do not declare GREEN from workflow configuration alone.
- Core V4 files untouched.

### Mandatory independent gates
1. Exact owner delta vs R1 HEAD; check no unintended files, no secret/leaked internal identifiers. `python3 scripts/prepublish_scan.py` must exit 0.
2. Confirm the `.github/workflows/community-ci.yml` YAML parses, the PR #4 branch target actually triggers jobs, and the two new offline regression jobs execute; when GitHub Actions is unavailable mark CI NOT VERIFIED rather than implying GREEN. Full clean-declared dependency install in isolated temp clone; Task API tests, all available V4 tests, health-check tests, `python -m compileall` and frontend `npm run build`; record precise pass/fail counts, baseline 15/15, V4 50/50, health 7 + new tests.
3. Boot actual Public standalone stack using genuinely free **isolated** ports (example Task API 8803, Agent 8904, Vite 8975) with `TASK_API_BASE_URL` pointing at isolated Task API; environment-only Vite overrides `PO_AGENT_DEV_UI_PORT=8975`, `PO_AGENT_DEV_PROXY_PORT=8904`. Confirm **real request `/api/v1/health` through isolated Vite proxy** is served by isolated Public Agent, not Review. Validate via source and unique port fingerprints; don't conflate agents. Check `Vite /api` no 502. Never terminate running Review.
4. Run Public `public_health_check.py` against explicit isolated ports with real source code and LLM probe if safely authorized, H0–H6, expecting GREEN per checkpoint. Verify H4 on HTML GET, not JSON. A successful H4 is SPA HTML smoke, **not proof that the browser works**: optionally run Playwright DOM on real task result with no planner JSON, candidates and sources. If browser automation not available, mark browser UI separately NOT VERIFIED.
5. Verify MCP 49 tools; public-deploy and public-health-check skills retained, Core V4 6/6 byte-identical to Public main, 4 experimental flags default OFF, configurable product spaces, no unbounded AS21 reads or modifications.
6. Bounded independent REAL AS21 A/B for at least one task read, worklogs, task type and hierarchy as permitted; evidence/complete pagination, no silent-zero. Existing Review LLM 429-blocked multi-turn scenarios remain OPEN unless actually run on Public.
7. Cleanup ONLY test-created temp services and temp files. No access to Review process PIDs or its ports. Report TESTED_HEAD, security, Core, test counts, 49 tools, exact H0–H6, Vite /api reverse-proxy evidence, independent A/B, browser status, remaining OPEN, and clear `PUBLIC_RELEASE_GREEN` only if mandatory criteria genuinely proved, otherwise `RELEASE_INCOMPLETE`/RED. No code edits. STOP.

### GigaCode command
Execute A230R3.8-R2-PUBLIC-ISOLATED-UI-REGATE from current Public GIGACODE_NEXT_ACTION.md. Fresh clone, free ports, H0-H6 + real isolated Vite /api proxy, full offline regression and Core 6/6. QA ONLY, no fixes/commits. Report and STOP.
