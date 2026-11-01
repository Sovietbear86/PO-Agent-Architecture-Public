# PO Agent Community — быстрый старт macOS

**Статус:** процедура подготовлена для проверки на macOS. Независимый QA Public main A230R3.12 подтвердил macOS zsh clean-clone и health H0–H6. Текущая версия этого текста ещё не прошла отдельный QA.

**Применение:** только локальное доверенное однопользовательское использование. Не открывайте Task API, MCP или Agent на 0.0.0.0 / в интернет. Корпоративные токены и .env не отправлять в чат и не коммитить.

## Предварительные условия

- macOS, zsh, Git и доступ к публичному GitHub.
- Python 3.13 для встроенного MCP-SWTR; Python >=3.11 для Task API и Agent. Проверьте `python3.13 --version`, `python3 --version`; если версия ниже, установите Python 3.13 через утверждённый способ (например, Homebrew).
- Node.js >=20 (рекомендовано 22), npm, `node --version`, `npm --version`.
- Рабочая сеть/VPN и законный доступ к своему AS21; адрес и токен предоставляются отдельно, НЕ из репозитория.
- Свой OpenAI-compatible LLM URL/model/key. Настройки должны быть локальными.
- При занятых портах 8003/8004/5175 не завершайте чужие процессы: используйте изолированные порты по `DEPLOYMENT.md`.

## 1. Получить и проверить Public

```zsh
git clone https://github.com/Sovietbear86/PO-Agent-Architecture-Public.git
cd PO-Agent-Architecture-Public
git switch main
git pull --ff-only
git rev-parse --short HEAD
test -f mcp-swtr/mcp_server.py
python3 scripts/prepublish_scan.py
```

В GigaCode можно вызвать `/public-deploy`, предварительно открыв **именно этот** клон. Skill обязан читать `DEPLOYMENT.md`.

## 2. Установить зависимости (из корня клона)

```zsh
python3.13 -m venv mcp-swtr/.venv
mcp-swtr/.venv/bin/python -m pip install -r mcp-swtr/requirements.txt

python3 -m venv task-api/.venv
task-api/.venv/bin/python -m pip install -r task-api/requirements.txt

python3 -m venv po-agent-platform-v2/.venv
(cd po-agent-platform-v2 && .venv/bin/python -m pip install -e '.[dev]')

(cd po-agent-platform-v2/frontend && npm ci && npm run build)
```

Если `mcp-swtr/.venv` создана другим Python, удалять её без согласования нельзя; сначала проверьте её версию. Для Apple Silicon и Intel используйте совместимые с вашей архитектурой пакеты.

## 3. Локальная конфигурация

```zsh
test -f task-api/.env || cp task-api/.env.example task-api/.env
test -f po-agent-platform-v2/.env || cp po-agent-platform-v2/.env.example po-agent-platform-v2/.env
test -f po-agent-platform-v2/frontend/.env || cp po-agent-platform-v2/frontend/.env.example po-agent-platform-v2/frontend/.env
chmod 600 task-api/.env po-agent-platform-v2/.env po-agent-platform-v2/frontend/.env
```

В `task-api/.env` задайте `SWTR_MCP_TRANSPORT=stdio`, собственные `SWTR_TOKEN` и `SWTR_MCP_BASE_URL`. В `po-agent-platform-v2/.env` задайте `AS21_MODE=task-api`, `TASK_API_BASE_URL=http://127.0.0.1:8003`, `AGENT_CORE_V4_ENABLED=true` и собственные `LLM_API_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL_NAME`. Отдельный SSE/MCP-сервер в stdio-режиме не нужен.

Настройте `task-api/config/products.yaml`, `task-api/config/team_members.yaml` под разрешённые пространства и команду, без фиктивных сотрудников. Изменения реальных имен/логинов храните локально, не публикуйте их.

## 4. Запуск: три независимых терминала

**Терминал 1, Task API:**
```zsh
cd PO-Agent-Architecture-Public/task-api
. .venv/bin/activate
set -a; . ./.env; set +a
uvicorn main:app --host 127.0.0.1 --port 8003
```

**Терминал 2, Agent:**
```zsh
cd PO-Agent-Architecture-Public/po-agent-platform-v2
. .venv/bin/activate
uvicorn po_agent.main:app --host 127.0.0.1 --port 8004
```

**Терминал 3, UI:**
```zsh
cd PO-Agent-Architecture-Public/po-agent-platform-v2/frontend
npm run dev -- --host 127.0.0.1
```

Пути `cd` относительны к родительской директории клона; откройте терминалы оттуда, либо используйте абсолютный путь **локально**, не помещая домашний путь в публичные отчёты. Откройте `http://127.0.0.1:5175`.

## 5. Приёмка

Из корня клона:
```zsh
python3 scripts/public_health_check.py --task-code PAY-123 --probe-agent
```

Замените `PAY-123` на **действительно существующий и доступный** вам код задачи. H0–H6 должны быть GREEN / exit 0, включая реальное чтение AS21 и доказательства результата агента; `INCOMPLETE` при отсутствии исходных данных не считается успешной установкой. Холодный stdio MCP стартует медленнее обычного; не подменяйте источник mock/fake и не отключайте безопасность TLS.

Проверьте браузер: запрос по той же задаче показывает её номер и понятные поля, нет сырых `capability_id/arguments`, ошибки HTTP отсутствуют. Только HTML H4 — **не** доказательство корректной работы интерфейса.

## 6. Диагностика / обновление / откат

- MCP не стартует: проверить Python 3.13, `mcp-swtr/.venv`, транспорт stdio, wrapper, **наличие** URL/токена без вывода содержимого.
- H5 RED: VPN, доступ пользователя к задаче, права и токен; 404 не трактовать как пустую выборку.
- H6 RED: LLM endpoint, 429, таймауты, конфигурация модели; не переписывать Core.
- H4 GREEN, UI /api не работает: убедиться, что Vite proxy направлен на **свой** Agent :8004, а не соседнюю установку.
- При ошибке установки остановить **только свои** процессы Ctrl+C, сохранить безопасные логи без секретов и вернуть предыдущий проверенный git commit/тег после согласования. Не удалять чужие .env и сессии.
- Обновление: сохранить локальную конфигурацию вне Git; `git pull --ff-only`, повторить установки зависимостей и health check. Не переносить приватную Review-ветку.

Полная справка: [DEPLOYMENT.md](DEPLOYMENT.md), [public-deploy](.gigacode/skills/public-deploy/SKILL.md), [public-health-check](.gigacode/skills/public-health-check/SKILL.md).
