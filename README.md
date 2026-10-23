# PO Agent Harness — Community Distribution

Reusable, read-only product-owner agent built around **Agent Core V4**, plugin Skills/Capabilities, a read-only Task API facade and REAL AS21/SWTR as the factual source.

This distribution is intentionally separated from the product-development repository:

- no QA reports/artifacts or historical assignment logs;
- no employee knowledge files;
- no real team roster;
- no tokens, API keys or workstation paths;
- no development-team product configuration;
- no Git history from the development repository in the final community repo.

## Bundled MCP-SWTR

The public distribution includes vetted Python MCP-SWTR source in `mcp-swtr/`. The default stdio wrapper starts it without a separate checkout. Install its Python 3.13 dependencies and configure your own network/token credentials; see `DEPLOYMENT.md`. MCP's direct tool surface may include writes, so expose the community Task API's read-only facade rather than the raw MCP server.

## Установка и проверка через GigaCode

Для установки публичной версии доступны **два GigaCode Skills**, которые входят в репозиторий:

- `/public-deploy` — установка комплектного MCP-SWTR, Task API, Agent Core V4 и Web UI (инструкции: [`.gigacode/skills/public-deploy/SKILL.md`](.gigacode/skills/public-deploy/SKILL.md)).
- `/public-health-check` — послойная проверка подключения к **REAL AS21**, регистрации MCP tools, Agent V4, LLM и UI (инструкции: [`.gigacode/skills/public-health-check/SKILL.md`](.gigacode/skills/public-health-check/SKILL.md)).

Начинайте с [`DEPLOYMENT.md`](DEPLOYMENT.md) — инструкция на русском с точными командами. После запуска проверьте работу:

```bash
python3 scripts/public_health_check.py --task-code PAY-123 --probe-agent
```

Замените `PAY-123` на реально существующую и доступную вам задачу AS21. Только корректный ответ от источника и доказательный результат агента позволяют получить `GREEN`. Без контрольной задачи вердикт будет `INCOMPLETE`, а не ложный успех. Скрипт не выводит исходные данные AS21 или токены.

## Configure your deployment

The two deployment-owned configuration files are:

- `task-api/config/products.yaml` — product/space codes visible to the agent;
- `task-api/config/team_members.yaml` — team members, roles and competencies.

Credentials and endpoints live only in environment variables / local `.env` files. See [DEPLOYMENT.md](DEPLOYMENT.md).

Architecture and extension rules: [ARCHITECTURE.md](ARCHITECTURE.md).

## Runtime

```text
Browser / PO Workspace
        |
        v
PO Agent (Agent Core V4)
        |
        v
Plugin Skill / Capability Registry
        |
        v
Read-only Task API
        |
        v
MCP-SWTR
        |
        v
REAL AS21
```

The LLM plans; it does not become the factual source. Business facts must be backed by AS21 evidence or the agent fails closed.

## Safety defaults

The community Task API exposes only read-only SWTR routes. Local browser tasks remain local browser data and are not written to AS21.

Before publishing your own fork/repository, run:

```bash
python scripts/prepublish_scan.py
```
