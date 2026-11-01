# PO Agent Community — быстрый старт Windows 11

**Рекомендованный режим: WSL2 + Ubuntu + Bash.** В этом режиме применяются те же команды, что в Linux/macOS. **Нативный PowerShell не сертифицирован:** аудит A230R3.12 выявил различия wrapper/venv/bash/path; не выдавайте Windows native за проверенный GREEN без отдельного независимого QA.

**Безопасность:** только локальное доверенное однопользовательское развертывание. Пользовательские AS21/LLM токены не публикуйте и не пересылайте. Не открывайте API/Agent/MCP на внешние сетевые интерфейсы.

## 1. Подготовить Windows и WSL2

Откройте Windows PowerShell **от имени администратора только для первоначальной установки WSL** (если это разрешено правилами организации):

```powershell
wsl --install -d Ubuntu
wsl --status
```

WSL может потребовать перезагрузку Windows. Если корпоративная политика блокирует WSL/Virtualization, согласуйте установку с IT; не отключайте политики безопасности ради обхода. Затем откройте установленный Ubuntu и выполните остальные действия **в терминале Ubuntu, не в PowerShell**.

В WSL2 установите Git, Python **3.13+ для MCP**, Python >=3.11 для Agent/Task API, Node >=20 и npm из доверенных источников согласно корпоративной политике. На Ubuntu версия Python из стандартного `apt` может быть ниже 3.13: проверьте `python3.13 --version` и установите утверждённый пакет/интерпретатор 3.13; не подменяйте его 3.11. Проверки:

```bash
git --version
python3.13 --version
python3 --version
node --version
npm --version
```

Храните клон **в файловой системе WSL** (например, `~/work`), а не на `/mnt/c`, чтобы избежать проблем с правами, venv, shell wrapper и производительностью.

## 2. Клонировать и установить Public (в Ubuntu WSL)

```bash
mkdir -p ~/work
cd ~/work
git clone https://github.com/Sovietbear86/PO-Agent-Architecture-Public.git
cd PO-Agent-Architecture-Public
git switch main
git pull --ff-only
test -f mcp-swtr/mcp_server.py
python3 scripts/prepublish_scan.py

python3.13 -m venv mcp-swtr/.venv
mcp-swtr/.venv/bin/python -m pip install -r mcp-swtr/requirements.txt

python3 -m venv task-api/.venv
task-api/.venv/bin/python -m pip install -r task-api/requirements.txt

python3 -m venv po-agent-platform-v2/.venv
(cd po-agent-platform-v2 && .venv/bin/python -m pip install -e '.[dev]')

(cd po-agent-platform-v2/frontend && npm ci && npm run build)
```

Из GigaCode откройте **WSL-клон** и вызовите `/public-deploy`; skill должен распознать Linux/WSL2, а не пытаться исполнять shell-команды в нативном PowerShell. Никакого GitVerse/private Review checkout не требуется.

## 3. Подключение AS21 и LLM (в Ubuntu WSL)

```bash
test -f task-api/.env || cp task-api/.env.example task-api/.env
test -f po-agent-platform-v2/.env || cp po-agent-platform-v2/.env.example po-agent-platform-v2/.env
test -f po-agent-platform-v2/frontend/.env || cp po-agent-platform-v2/frontend/.env.example po-agent-platform-v2/frontend/.env
chmod 600 task-api/.env po-agent-platform-v2/.env po-agent-platform-v2/frontend/.env
```

Укажите собственные SWTR token/endpoint в `task-api/.env` и LLM URL/model/key в `po-agent-platform-v2/.env` по [DEPLOYMENT.md](DEPLOYMENT.md). `SWTR_MCP_TRANSPORT=stdio` работает с комплектным Python 3.13 MCP. Не используйте `setx`/Windows User Environment для хранения ключей и не включайте токены в CLI. Настройте `task-api/config/products.yaml` и `team_members.yaml` на свои разрешённые пространства.

**VPN/DNS:** проверьте доступ к корпоративной AS21 **внутри WSL2**, а не только в Windows. Если WSL2 не видит VPN, это сетевой вопрос IT; не меняйте системные настройки безопасности вслепую.

## 4. Запуск: три Ubuntu/WSL терминала

Task API:
```bash
cd ~/work/PO-Agent-Architecture-Public/task-api
. .venv/bin/activate
set -a; . ./.env; set +a
uvicorn main:app --host 127.0.0.1 --port 8003
```

Agent:
```bash
cd ~/work/PO-Agent-Architecture-Public/po-agent-platform-v2
. .venv/bin/activate
uvicorn po_agent.main:app --host 127.0.0.1 --port 8004
```

UI:
```bash
cd ~/work/PO-Agent-Architecture-Public/po-agent-platform-v2/frontend
npm run dev -- --host 127.0.0.1
```

В браузере Windows попробуйте `http://localhost:5175` (WSL2 обычно предоставляет localhost forwarding). Если адрес недоступен, сначала проверьте, что Vite слушает внутри Ubuntu и WSL localhost forward включён; не выставляйте `--host 0.0.0.0` для «исправления» без согласования сетевого контура.

## 5. Health Check и подтверждение установки

Из **Ubuntu WSL**, из корня клона:
```bash
python3 scripts/public_health_check.py --task-code PAY-123 --probe-agent
```

Замените `PAY-123` реальной доступной задачей. Вызов `/public-health-check` через GigaCode должен повторить H0–H6 (49 MCP tools, Task API, Agent, UI, REAL AS21, LLM+evidence). Если нет доступа к источнику/LLM — `INCOMPLETE`, не GREEN. Холодный старт WSL может отличаться по времени; таймауты не увеличивать без замеров.

## 6. Типичные проблемы и откат

- `python3.13: command not found`: не установлен нужный Python для MCP; установить 3.13 из утверждённого источника.
- `mcp-swtr-wrapper.sh`/permission denied: WSL/Linux права, LF окончания строк и корректный Python venv; не запускать wrapper напрямую через PowerShell.
- Проблемы `.env` / `source`: файлы должны быть локальными, доверенными и корректными для shell; не загружать непроверенные скрипты.
- H2/H3 RED: проверить stdio cold initialization, 49 инструментов, адрес своего Task API. H5 RED: сеть/VPN/права AS21. H6 RED: LLM 429/timeout.
- UI в Windows пустой: Vite в WSL должен проксировать `/api` на Agent **в WSL**, а не на другой сервис в Windows. Проверьте 127.0.0.1 ports и DEV proxy.
- При откате остановить **только свои** процессы Ctrl+C; вернуться к ранее подтверждённому git commit/tag, сохранить локальные .env. Не выполнять очистку чужих процессов/файлов.

Полное описание: [DEPLOYMENT.md](DEPLOYMENT.md). Нативная PowerShell-инструкция появится только после отдельного QA; пока она **не заявлена как поддерживаемая**.
