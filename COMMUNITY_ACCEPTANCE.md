# Community Distribution Acceptance

Run this gate before copying the staging snapshot into a new repository.

## A. Sanitization

- [ ] `python scripts/prepublish_scan.py` returns GREEN.
- [ ] No real `.env` files.
- [ ] No SWTR/LLM tokens, cookies, private keys or certificates.
- [ ] No `knowledge/employees` directory.
- [ ] No QA reports, screenshots or REAL AS21 payload dumps.
- [ ] No real employee roster/e-mails.
- [ ] No development-repository product defaults or team-member names.
- [ ] No workstation-specific absolute paths.

## B. Configurability

Replace the templates with a throwaway configuration:

```yaml
# task-api/config/products.yaml
products:
  PAY:
    display_name: Payments
  CRM:
    display_name: CRM
```

and synthetic members in `team_members.yaml`.

Require:

- [ ] Agent health advertises V4 successfully.
- [ ] PAY/CRM are accepted as product spaces after restart.
- [ ] a space absent from products.yaml fails clarification/grounding rather than being silently accepted.
- [ ] Team page can select configured products.
- [ ] Quality aging product selector uses configured frontend labels.
- [ ] team/competency Skills read the configured synthetic roster.

## C. Runtime

- [ ] Task API exposes only the intended read-only SWTR routers.
- [ ] MCP stdio mode starts with environment-only credentials.
- [ ] MCP SSE mode connects when configured.
- [ ] Agent starts with OpenAI-compatible LLM endpoint/model/API key.
- [ ] `GET /api/v1/health` is ready.
- [ ] direct Agent query succeeds against a configured product.
- [ ] source outage returns typed unavailable/error, never factual zero.

## D. Frontend

```bash
cd po-agent-platform-v2/frontend
npm ci
npm run build
```

Require:

- [ ] build GREEN;
- [ ] configurable brand/context/product chips visible;
- [ ] no development-product branding/defaults;
- [ ] Tasks page submits raw text to Agent API;
- [ ] six workspaces render without old product assumptions.

## E. Fresh repository history

The final repository must be created from an exported working tree **without the original .git directory**.

- [ ] new empty GitHub repository exists;
- [ ] first commit is `Initial community distribution`;
- [ ] no commit ancestry from `PO-Agent-Architecture-Review`;
- [ ] repository visibility/access is explicitly chosen by the owner;
- [ ] organization secret scanning / dependency scanning is enabled where available.

## F. GigaCode deployment / layered health gate

- [ ] `.gigacode/skills/public-deploy/SKILL.md` and `.gigacode/skills/public-health-check/SKILL.md` are in the public checkout and referenced from `GIGACODE.md`.
- [ ] `python3 -m unittest discover -s scripts/tests -p 'test_public_health_check.py' -v` passes offline.
- [ ] MCP Python 3.13 installed from the **bundled** `mcp-swtr/` checkout; not from an unrelated local GitVerse source.
- [ ] HTTP Task API `/health` is **not** mistaken for source reachability.
- [ ] Task API SWTR `/api/v1/swtr-read/health` identifies connected MCP and required read tool.
- [ ] Agent V4 `/api/v1/health` reports `adapter=task-api`, V4 ready and healthy source status (never `fake`).
- [ ] One **scoped authorized REAL AS21 task read** returns the exact requested code; LLM task query gives source-backed evidence.
- [ ] Missing SWTR token / AS21 network / LLM endpoint failures do not turn into fabricated factual-zero results.
- [ ] Browser smoke verifies UI proxy `/api` → Agent :8004.
- [ ] No `.env`, real tokens, personal data or raw AS21 payloads appear in GigaCode reports.
- [ ] If Docker is not installed/available, explicitly report container build as **NOT TESTED**, not GREEN.
