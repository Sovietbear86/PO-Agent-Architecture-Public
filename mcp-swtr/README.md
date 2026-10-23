# MCP-SWTR — bundled Python server

This directory contains the sanitized, publication-authorized **Python MCP-SWTR runtime** required by the community PO Agent distribution. No separate GitVerse checkout is necessary for the **stdio** deployment path.

**Prerequisites:** Python 3.13+, network access to your organization's AS21/SWTR endpoint, and an authorized personal/service token. Do not commit endpoints with embedded credentials, live tokens or local `.env` files.

## Install (from repository root)

```bash
cd mcp-swtr
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
cd ..
```

Configure `task-api/.env` following `DEPLOYMENT.md`; in stdio mode the repository-root `mcp-swtr-wrapper.sh` automatically uses this bundled server. Set `SWTR_MCP_TRANSPORT=stdio`, `SWTR_TOKEN` and `SWTR_MCP_BASE_URL` **only in the local environment**. Leave `SWTR_MCP_SERVER_DIR` unset to use the bundled directory. The wrapper starts the server with `PORT=0` over stdio; no separate MCP process or `/sse` endpoint is required.

## Alternative: managed SSE

If your organization provides an independently running MCP-SWTR SSE instance, configure `SWTR_MCP_TRANSPORT=sse` and `SWTR_MCP_SSE_URL`. In that case the bundled Python source need not be started. See `DEPLOYMENT.md`.

## Docker

A hardened container recipe is included; it does **not** bake in credentials. For custom deployments supply `BASE_URL`/`TOKEN` at **container runtime** through environment or a secret store. Do not place these values in build args or image layers. Do not publicly expose MCP-SWTR directly: the underlying server registers write-capable tools; the community **Task API facade** is the read-only boundary.

## Provenance

See `PROVENANCE.md`. This is a minimal runtime bundle. The optional Node/npx implementation and large internal API documentation are deliberately not included in the community distribution.

## Troubleshooting

After starting Task API, run `curl -fsS http://127.0.0.1:8003/api/v1/swtr-read/health`. `/health` alone checks Task API liveness; `/api/v1/swtr-read/health` verifies MCP availability. A successful connection does not guarantee AS21 read authorization. If tools load but data is missing, check the network/VPN, token validity, requested AS21 space and actual API response; never paste token values into tickets or logs.
