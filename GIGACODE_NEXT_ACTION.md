# GigaCode — CURRENT NEXT ACTION

## A230R3.13-PUBLIC-P2-OS-QUICKSTART-QA

**Independent QA ONLY** on Public documentation PR from branch `docs/p2-cross-platform-quickstarts`. No production code edits, no commits/pushes/merges, no killing running services, no changes to REAL AS21 data or external access controls. Use clean disposable clones. This is a documentation and Skills QA, **not** authorization to deploy Public to a multi-user server.

### Baseline
- Public main after PR #3/#4 merged: `36be0493`. A230R3.12 reported POSTMERGE_GREEN: clean Public main 49 MCP tools, Core 6/6, offline Agent 50/50, Task API 15/15, health 10/10, H0–H6 cold+warm, browser/UI and bounded REAL AS21 A/B.
- A230R3.12 macOS zsh local single-user workflow verified; Windows native PowerShell has known installation/wrapper/venv gaps. This PR deliberately documents **Windows 11 WSL2+Ubuntu**, NOT unsupported native PowerShell.
- Owner adds `QUICKSTART_MACOS.md`, `QUICKSTART_WINDOWS.md` and cross-links in `DEPLOYMENT.md`, `.gigacode/skills/public-deploy/SKILL.md`, `.gigacode/skills/public-health-check/SKILL.md`. No Agent/Task API/MCP/Core changes intended.

### Gates
1. **Source integrity**: git fetch; exact TESTED_HEAD and delta vs `main`. Only two new guides, `DEPLOYMENT.md`, both Skills and this spec. Public Core V4 6/6 byte-identical to main; `python3 scripts/prepublish_scan.py` exit 0, check no secrets/PII/internal hosts or unsafe instructions in changed docs.
2. **Technical correctness (no invented success)**: cross-check every command/path/CLI flag against **actual Public main source**. Verify Python 3.13 runtime for stdio MCP, >=3.11 Agent/Task API, Node >=20, wrapper path, editable install extras, env locations, products.yaml, ports, Vite proxy, H0–H6 arguments, `--probe-agent`, 49 tools. Confirm source `.env` examples are safe for shell and no accidental token echo. Diagnose reproducibility of `npm ci`, venv commands and starting uvicorn from documented work directories. Treat unknown as NOT VERIFIED.
3. **macOS test**: use clean isolated clone and own free ports to replay quickstart as documented where permitted; observe build, H0–H6 source and LLM only with authorized local access; no login/secrets printed. If complete real run unavailable, static path audit + previously verified A230R3.12 is evidence, not current guide QA GREEN.
4. **Windows test**: if real Windows 11 WSL2 available, verify WSL preflight, Ubuntu dependencies, clone inside ext4, Python 3.13, 3 virtualenvs, Node/npm, Bash wrapper, secrets, 3 processes, local forwarding, 49 tools, H0–H6, browser. If no Windows environment, **NOT VERIFIED** explicitly; static cross-platform review may pass but must not declare Windows deployment GREEN. Native PowerShell is unsupported/NOT CERTIFIED.
5. **Skills**: verify GigaCode recognizes `/public-deploy` and `/public-health-check` from Public clone and discovers both quickstarts by correct relative Markdown links; no use of Review's private environment. Each skill must fail closed if missing AS21/LLM credentials, must never commit .env or write to AS21, and must isolate ports.
6. **CI/Regression**: run official GitHub CI for actual docs PR head if triggered and check full scan/build, no false green based only on merged main's old head. If relevant, run 49 tools and health check CLI offline tests. No code modifications by QA.

### Report / STOP
Return a table `Gate | TESTED_HEAD | evidence | status | first failure`, tested OS versions, exact commands corrected if needed, macOS confirmed/reused evidence vs Windows actual verification, Security Scan, Core 6/6, Skills resolution, CI status, remaining portability gaps. Verdict `DOCS_QA_GREEN / DOCS_QA_INCOMPLETE / RED`. No release claim for native PowerShell. STOP.
