# Local deployment

This guide starts the community build on one workstation/localhost.

## 1. Prerequisites

Install:

- Python 3.11+ for Task API/Agent, **Python 3.13+ for the bundled MCP-SWTR server**;
- Node.js 20+ (22 recommended);
- npm;
- the bundled Python MCP-SWTR source under `mcp-swtr/` (stdio) **or** access to your organization's existing MCP-SWTR SSE server;
- a valid **SWTR token** for REAL AS21 read access;
- an **OpenAI-compatible LLM endpoint**, model name and API key.

Recommended local ports:

| Component | Port |
|---|---:|
| MCP-SWTR SSE, if used | 3000 |
| Task API | 8003 |
| PO Agent | 8004 |
| Frontend | 5175 |

## 2. Product spaces

Edit:

`task-api/config/products.yaml`

Example:

```yaml
products:
  PAY:
    display_name: "Payments"
    aliases: ["PAY", "Payments"]
    s21_projects: []
    s21_components: []

  CRM:
    display_name: "CRM"
    aliases: ["CRM"]
    s21_projects: []
    s21_components: []
```

The **YAML keys are the canonical AS21 space codes**. They replace product-specific constants. Restart the Agent after changing this file.

## 3. Team members and competencies

Edit:

`task-api/config/team_members.yaml`

Minimal member:

```yaml
schema_version: 3
members:
  - id: Ivanov.I.I
    login: Ivanov.I.I
    full_name: Иванов Иван Иванович
    products: [PAY]
    team_role: Developer
    professional_profile: Backend developer
    competencies: [Java, PostgreSQL, Payments]
```

Rules:

- `id/login` should match the identity visible from AS21;
- `products` must use codes declared in `products.yaml`;
- `competencies` are declared configuration, not inferred personal ratings;
- do not commit corporate e-mail addresses unless your repository policy explicitly allows it.

## 4. MCP-SWTR / AS21 connection

The Task API supports:

- **stdio** — launch an MCP-SWTR server as a child process;
- **sse** — connect to an already-running MCP-SWTR endpoint.

Create:

`task-api/.env`

from `task-api/.env.example`.

### stdio example

```dotenv
SWTR_MCP_TRANSPORT=stdio
SWTR_TOKEN=YOUR_SWTR_TOKEN
SWTR_MCP_BASE_URL=https://YOUR-AS21-SWTR-ENDPOINT
FRONTEND_ORIGIN=http://localhost:5175
```

The repository wrapper `mcp-swtr-wrapper.sh` uses the bundled `mcp-swtr/` source by default and passes only configured environment values to the MCP process. The community wrapper does **not** read user-specific secret files.

### SSE example

```dotenv
SWTR_MCP_TRANSPORT=sse
SWTR_MCP_SSE_URL=http://127.0.0.1:3000/sse
SWTR_TOKEN=YOUR_SWTR_TOKEN
SWTR_MCP_BASE_URL=https://YOUR-AS21-SWTR-ENDPOINT
```

If the SSE server owns authentication itself, keep the token only in that server's environment.

## 4a. Install the bundled MCP-SWTR server (stdio only)

This distribution now includes the necessary Python source. **Do not clone GitVerse or a separate MCP repository.**

```bash
cd mcp-swtr
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
cd ..
```

In `task-api/.env` set `SWTR_MCP_TRANSPORT=stdio`, `SWTR_TOKEN` and `SWTR_MCP_BASE_URL` to your authorized values. **Leave `SWTR_MCP_SERVER_DIR` unset** for the bundled directory; `mcp-swtr-wrapper.sh` will choose the correct path and use `mcp-swtr/.venv/bin/python`. Do not commit `.env` or paste credential values into logs.

If using an existing SSE service, skip this installation and configure `SWTR_MCP_TRANSPORT=sse` and `SWTR_MCP_SSE_URL` instead. In SSE mode the remote MCP process owns its credentials.

### Troubleshooting first boundary

After Task API starts, query **both** endpoints:

```bash
curl -fsS http://127.0.0.1:8003/health
curl -fsS http://127.0.0.1:8003/api/v1/swtr-read/health
```

The first only confirms Task API availability; the second checks MCP transport and tool registry. If the second fails, check (in order) bundled Python dependencies / wrapper path, configured `SWTR_MCP_TRANSPORT`, and whether the token and base URL are **set** (never print their values). If MCP connects but AS21 reads fail, verify organizational network/VPN access, token scope and server response. **An empty result is not evidence of an empty AS21 dataset until a scoped source read succeeds.**

## 5. Start Task API

```bash
cd task-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

set -a
source .env
set +a

uvicorn main:app --host 127.0.0.1 --port 8003
```

Check:

```bash
curl http://127.0.0.1:8003/health
```

The community `main.py` exposes the read-only SWTR facade only.

## 6. Configure the Agent + LLM

Create:

`po-agent-platform-v2/.env`

from `po-agent-platform-v2/.env.example`.

Required production-like values:

```dotenv
AS21_MODE=task-api
TASK_API_BASE_URL=http://127.0.0.1:8003
AGENT_CORE_V4_ENABLED=true

TEAM_CONFIG_PATH=../task-api/config/team_members.yaml
PRODUCTS_CONFIG_PATH=../task-api/config/products.yaml

LLM_API_BASE_URL=https://YOUR-OPENAI-COMPATIBLE-ENDPOINT/v1
LLM_API_KEY=YOUR_LLM_API_KEY
LLM_MODEL_NAME=YOUR_MODEL_ID
LLM_TLS_VERIFY=true
```

The model must support the normal OpenAI-compatible chat/completions contract used by the Agent runtime.

## 7. Start PO Agent

```bash
cd po-agent-platform-v2
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

uvicorn po_agent.main:app --host 127.0.0.1 --port 8004
```

Readiness:

```bash
curl http://127.0.0.1:8004/api/v1/health
```

A simple request:

```bash
curl -X POST http://127.0.0.1:8004/api/v1/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"Спринты в PAY","session_id":"local-demo"}'
```

## 8. Configure and start frontend

Create `po-agent-platform-v2/frontend/.env` from the example:

```dotenv
VITE_APP_BRAND=PO Agent
VITE_CONTEXT_LABEL=Payments Team
VITE_PRODUCT_LABELS=PAY,CRM
VITE_DEFAULT_SPRINT_ID=PAY-SPRNT-1
VITE_DEFAULT_RELEASE_ID=PAY-RELEASE-1
```

Then:

```bash
cd po-agent-platform-v2/frontend
npm ci
npm run dev
```

Open:

`http://localhost:5175`

## 9. Variables reference

### Agent

| Variable | Required | Purpose |
|---|---|---|
| `AS21_MODE` | yes | use `task-api` for REAL AS21 |
| `TASK_API_BASE_URL` | yes | Task API address |
| `AGENT_CORE_V4_ENABLED` | yes | enable V4 runtime |
| `TEAM_CONFIG_PATH` | recommended | team roster YAML |
| `PRODUCTS_CONFIG_PATH` | recommended | product spaces YAML |
| `LLM_API_BASE_URL` | yes | OpenAI-compatible base URL |
| `LLM_API_KEY` | yes | LLM credential |
| `LLM_MODEL_NAME` | yes | model identifier |
| `LLM_TLS_VERIFY` | recommended | TLS verification; keep true normally |

### Task API / MCP

| Variable | Required | Purpose |
|---|---|---|
| `SWTR_MCP_TRANSPORT` | yes | `stdio` or `sse` |
| `SWTR_TOKEN` | yes* | AS21/SWTR token (*unless auth belongs entirely to remote SSE) |
| `SWTR_MCP_BASE_URL` | stdio | upstream AS21/SWTR endpoint |
| `SWTR_MCP_SERVER_DIR` | optional | custom MCP path; omit for bundled `mcp-swtr/` |
| `SWTR_MCP_SSE_URL` | sse | remote/local SSE URL |
| `FRONTEND_ORIGIN` | no | CORS origin, default localhost:5175 |

## 10. Do not commit

Never commit:

- `.env`;
- SWTR tokens;
- LLM API keys;
- personal team rosters unless explicitly approved;
- copied QA artifacts with REAL AS21 payloads;
- workstation paths;
- browser/session dumps.

Run `python scripts/prepublish_scan.py` before pushing.
