# GigaCode — CURRENT NEXT ACTION

## A230R3.8-PUBLIC-CLEAN-CLONE-ISOLATED-DEPLOY-QA

**QA ONLY.** Do not change code, tests, docs, configuration, repository history, GitHub PRs, or existing running processes. No commits/pushes/merges. Do not use write-capable AS21 MCP tools. Respect user's existing local Review services on 8004/5175/3000 and any other occupied ports; DO NOT stop them. Always compare `LOCAL_HEAD == REMOTE_HEAD == TESTED_HEAD` for PR #4 `feat/a230r3-community-migration`. PR #4 is stacked onto Draft PR #3 and remains Draft.

### Prior verified baseline
R2 independent `A230R3.7-R2-PUBLIC-SECURITY-REGATE` on `5a2f614`: `prepublish_scan.py` GREEN; import/registry 14 plugins, 73 skills, 75 capabilities, 70 UI contracts; frontend build GREEN; 49 MCP tools; frozen Core 6/6 identical to Public main; 72/72 offline tests with `pytest-asyncio` co-installed. R2 found **undeclared test dependency** `pytest-asyncio` (12 async tests fail with clean declared-deps only). Owner added dependency in commit `e682f0e`. **Not yet retested**. Prior bounded REAL AS21 A/B in R1 showed parity but is not proof of standalone clean-clone deploy.

### Gate 0: branch, security, exact delta
1. Fetch origin; confirm actual TESTED_HEAD and local=remote. Don't overwrite dirty files or reset/stash user work. Use an isolated temporary clone OUTSIDE user's working trees. Never copy private Review .env or corporate tokens into Public repo.
2. Confirm delta since `5a2f614` is just `task-api/requirements.txt` pytest-asyncio declaration plus this QA assignment, excluding unrelated changes. Verify Core V4 six files are byte-identical to Public main, not private Review docs.
3. `python3 scripts/prepublish_scan.py` on PR #4 temp clone exit 0. No real data, tokens, corp hosts or personal identifiers. Redact all responses/logs.

### Gate 1: clean declared dependencies and regression
1. Install Task API requirements `pip install -r task-api/requirements.txt` in a brand-new isolated environment (not an agent venv; no preinstalled pytest-asyncio); verify PyYAML and pytest-asyncio are importable and provenance comes from declared requirements. Run all Task API tests; compare with R2 15/15; no missing plugins.
2. Use Public documented Python requirements: Python 3.13+ for MCP-SWTR; appropriate supported version for Agent/Task API. Run import/compile checks for MCP, Task API, Agent. Confirm 49 tools, route GET-only facade, V4 14/73/75/70 registry, public configs via products.yaml, four experimental V4 flags default OFF.
3. Run full available V4 tests, frontend build, tests for UI task tables and candidates, suites, worklogs, time grammar, clarifications and scope guard. Report passed/failed/skipped exact counts; do not pretend a fake oracle is REAL AS21.

### Gate 2: standalone isolation/no port conflict
1. Inspect `.gigacode/skills/public-deploy/SKILL.md` and `.gigacode/skills/public-health-check/SKILL.md`; validate documented stack topology and startup scripts. **Never bind 8003/8004/5175/3000 if occupied; never terminate existing servers.** Prefer an ephemeral container or namespace isolated loopback network, or independently configurable free local ports only when **all** Task API, Agent, Vite proxy, MCP transport and health-check URLs can be coherently overridden. Never assume command-line --port alone fixes hardcoded proxy URLs.
2. If the isolated stack can safely start, run actual `public-deploy` flow, `public_health_check.py` H0–H6 against that stack, including MCP/Task API/Agent/UI. Read-only limited workloads. Use valid secrets only from securely available local environment; do not expose values, copy them to temp worktree, or place credentials in console output.
3. If environment, access, package installation, or port isolation prevents full deployment, **mark INCOMPLETE, not GREEN**, with exact first unresolved boundary and a safe reproducible solution proposal. No consent to killing or reconfiguring the user's processes.

### Gate 3: authorized bounded REAL AS21 A/B
If access is valid and scoped, compare one or more of (A) clean-clone Public Agent vs (B) independent read-only REAL AS21 oracle: member date-worklogs, source-backed task type `suit`, hierarchy/relations, sprint calendar vs lifetime guard, context clarifications. Confirm complete pagination, author attribution, evidence, no silent-zero, no unscoped scans, no writes. If unavailable, separately mark `A/B NOT VERIFIED`. Four earlier LLM 429 E2E scenarios remain OPEN until genuinely verified.

### Report and stop
Return: `TESTED_HEAD`, `SECURITY`, `Core 6/6`, dependency clean install, Task API/V4/UI/health results, MCP tools, H0–H6 per checkpoint, A/B source parity and exposure scope, occupied ports respected, exact first failing boundary, leftovers, `PUBLIC_RELEASE_GREEN / RELEASE_INCOMPLETE / RED`. GigaCode may write a sanitized local untracked QA report only, not commit. **STOP**.

### Short command
Execute A230R3.8-PUBLIC-CLEAN-CLONE-ISOLATED-DEPLOY-QA from the current Public PR #4 GIGACODE_NEXT_ACTION.md. Fresh isolated clone, no collisions or service termination; independent QA only, real standalone H0–H6 where safe. Report + STOP.
