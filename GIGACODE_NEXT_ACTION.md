# GigaCode — CURRENT NEXT ACTION

## A230R3.7-R2-PUBLIC-SECURITY-REGATE — independent follow-up after owner-only fix

**ONLY QA.** Do not fix source code, tests, dependencies, configs, docs or Core. No commit, merge, push, force operations, user-service stop, unauthorized live AS21 mutation or tenant-wide scans. Preserve existing local worktree. Always fetch and verify `LOCAL_HEAD == REMOTE_HEAD == TESTED_HEAD`.

### Why this gate exists
A230R3.7 tested `2c05419` and reported RED **only** because `prepublish_scan.py` detected a legacy internal space identifier in a comment inside `po-agent-platform-v2/src/po_agent/harness/v4_plugins/_task_live_handlers.py` around line 1129. A/B REAL AS21, 72 offline tests, 49 MCP tools, frontend build and Core 6/6 were GREEN on that tested snapshot. Previous QA also flagged missing explicit PyYAML dependency as minor. Owner committed:
- `66c5501`: removed specific internal space identifier from historical performance comment, no behavioral change.
- `339aa92`: declared `PyYAML>=6.0` in `task-api/requirements.txt`, matching already existing `import yaml` and `products.yaml` dynamic configuration.
Both remain inside **Draft PR #4**, stacked on Draft PR #3.

### Required re-gate
1. Confirm fresh `TESTED_HEAD` of Public `feat/a230r3-community-migration` equals origin; identify *exact* diff from failed baseline `2c05419` and prove changes strictly the one comment and one dependency declaration.
2. Run `python3 scripts/prepublish_scan.py` **on the actual PR tree**. It MUST exit 0. Do not hide or suppress its rules. If RED, report exact first finding without exposing sensitive values. Re-check public history/provenance; no new credentials, corporate hosts or PII.
3. Reinstall/build in clean isolated test environment using **declared** Public dependencies, and verify import `yaml` works in isolated Task API venv; test actual `_configured_spaces()` using a synthetic `products.yaml`. Ensure no accidental hardcoded internal project/space. Avoid hidden dependency from co-installed agent venv.
4. Re-run available synthetic regression (prior 72 passed), V4 skills registry and imports, frontend build, 49 MCP instruments, read-only route count, tests for suit / hierarchy / worklogs with bounded REAL AS21 oracle if authorized. Report precise numbers and changes vs baseline, no fake green.
5. Public **6/6 Core V4** SHA match against Public main. No Core edits. PR #3 skills and tools retained, PR #4 remains Draft.
6. Determine release decision accurately: clean-clone full-stack `public-deploy` was **NOT RUN** in R1 due to conflicts with user running services and health H1/H2/H4 RED, H5/H6 INCOMPLETE. These are **still NOT VERIFIED** unless actually run in a separate safe environment with consent. Never label full release GREEN based solely on safety re-gate. Prior four LLM 429 cases are still OPEN.

### Verdict
- `SECURITY_GATE_GREEN / RELEASE_INCOMPLETE` if scanner and regression pass but clean-clone full-stack or live public health remain untested.
- `RED` if scanner or import/test regressions fail; identify first boundary and stop.
- `PUBLIC_RELEASE_GREEN` only after actual full standalone public-deploy/health H0–H6 and required authorized A/B verification pass.
Report TESTED_HEAD, gate matrix, first failing boundary and exact remaining blockers in chat. STOP.

### GigaCode one-line command
Execute A230R3.7-R2-PUBLIC-SECURITY-REGATE from Public GIGACODE_NEXT_ACTION.md. Sync HEAD, scan + offline regress + Core 6/6, verify PyYAML clean-env import. QA ONLY, no changes/commits, report and STOP.
