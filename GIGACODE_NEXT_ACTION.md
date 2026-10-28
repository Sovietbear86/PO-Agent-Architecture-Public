# GigaCode — CURRENT NEXT ACTION

## A230R3.9-PUBLIC-BROWSER-DOM-RELEASE-GATE — independent QA only

**Do not change production code, Core, tests, docs, git history, PRs, configs, credentials or AS21. No commits/merges/pushes.** Preserve user's running Review services and working tree. Fetch remote, confirm exact `LOCAL_HEAD = REMOTE_HEAD = TESTED_HEAD` on Public `feat/a230r3-community-migration`; work in isolated temporary clone with temporary services only. Parent PR #3 / PR #4 remain Draft until owner release.

### Proven baseline
- A230R3.8-R2 on `7fbb47f`: independent Security Scan GREEN; clean dependencies and offline tests GREEN, V4 50/50; Task API 15/15; health-check 9/9; 49 MCP tools; 14 plugins / 73 skills / 75 capabilities / 70 UI; frozen Public Core V4 6/6. Isolated Public stack on independently available local ports: H0–H6 GREEN (exit 0), REAL AS21 bounded A/B (task type, hierarchy, author/date worklogs) GREEN; isolated Vite `/api` routed to **isolated** Public Agent, not Review. All existing Review services untouched. This is *not yet* browser DOM proof.
- Independently checked GitHub Actions: `Community CI` run **40756533616** for `7fbb47f` completed **success**, all six jobs GREEN: `sanitize`, `backend`, `frontend`, `health-tool`, `offline-agent-regression`, `offline-task-api-regression`. Recheck status for actual tested HEAD if changed.
- R2 `RELEASE_INCOMPLETE` because browser DOM (Playwright/Puppeteer unavailable in that environment), canonical default-port clean host deployment not executed, and 4 historical LLM 429 E2E cases remain open.

### Gate A: real browser DOM (primary objective)
1. Assess available browser automation without installing intrusive/untrusted software. Prefer existing headless Chromium or Playwright in separate isolated environment. If unavailable, report `BROWSER_NOT_VERIFIED`; **do not** equate HTML H4 or proxy API response to DOM proof.
2. Create safe isolated public clone and full stack (distinct free local loopback ports; no termination of Review). Observe browser console/network and confirm root rendering, navigation `Обзор`, `Задачи`, `Спринты`, `Релизы`, `Качество`; loading vs errors, session data isolation; no raw planner JSON displayed.
3. Perform bounded authorized user-visible queries through UI for: task key/title, task type, hierarchy/epics, member worklogs for an explicit period, `team.assignee_recommendation` ranked `candidates`, sources/evidence, explicit empty result and fail-closed negative state. Compare visible business rows to source response counts (respect documented sample caps), confirm correct labels and no `capability_id/arguments/widget:/kind:` leaking.
4. Verify Vite proxy `/api` is strictly Public isolated Agent using distinct port proof. Protect tokens; no raw AS21 payload/screenshot with personal identities in report.

### Gate B: release integration / reproducibility
1. Recheck PR #3 and PR #4 dependency/stacking, GitHub Actions six jobs for TESTED_HEAD, `prepublish_scan.py` exit 0, complete offline suites, 49 MCP tools, read-only Task API, four experimental flags default OFF and public configurable products. Preserve six Core blobs byte-identical to Public main.
2. Verify the `public-deploy` and `public-health-check` skills are installed and documented. The isolated alternate-port deployment validated in R2 is sufficient for functional deployment evidence. The canonical 8003/8004/5175 deployment on an otherwise empty host is **not verified**; do not stop existing services to test it. If no free separate host, mark canonical optional, not equivalent to failure of isolated functional deployment.
3. If LLM endpoint stable and user consent/quotas permit, perform **bounded** remaining four E2E cases blocked by prior 429 on Public (lifetime-sprint clarification, multi-turn date clarification, person+status and creation period). Compare to independent REAL AS21 source, make exact source-completeness claims. Stop on 429 repeats; mark `LLM_E2E_UNVERIFIED` not GREEN if blocked. Never unbounded scan or AS21 write.
4. Report `PUBLIC_RELEASE_GREEN` **only** when all mandatory security/build/offline/isolated H0–H6/real DOM and required bounded A/B gates pass without new regressions. Otherwise `RELEASE_INCOMPLETE` with clear first still-open blocker. Distinguish optional canonical port test and LLM coverage from mandatory release issues. No merge: owner decides separately.

### Report
Return exact TESTED_HEAD, official CI 6-job status and run URL or ID, browser method/provenance, test scenarios/passed/failed, source A/B, H0–H6, frozen Core 6/6, security and remaining OPEN, no secrets or PII. QA-only, stop. **No source changes.**

### One-line command
Execute A230R3.9-PUBLIC-BROWSER-DOM-RELEASE-GATE from Public GIGACODE_NEXT_ACTION.md. Independent real browser DOM on safe isolated Public, CI/security/regression verification and bounded read-only A/B. Report and STOP.
