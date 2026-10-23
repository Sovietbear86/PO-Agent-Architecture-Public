# PO Agent Community — развёртывание и проверка работоспособности

Эта инструкция — **единый источник истины для публичной версии** `Sovietbear86/PO-Agent-Architecture-Public`. Развёртывание рассчитано на одну локальную машину (macOS, Linux, Windows через WSL2), без открытия внутренних API в интернет.

**Быстрый вариант через GigaCode:** два готовых skill-файла:

- `/public-deploy` — установка и локальный запуск: [`.gigacode/skills/public-deploy/SKILL.md`](.gigacode/skills/public-deploy/SKILL.md);
- `/public-health-check` — проверка MCP → REAL AS21 → Agent V4 → LLM → Web UI: [`.gigacode/skills/public-health-check/SKILL.md`](.gigacode/skills/public-health-check/SKILL.md).

GigaCode должен запускаться **из клона Public-репозитория** и читать `GIGACODE.md`. Установку не считаем завершённой только по запуску процессов: нужен health check и реальный ограниченный запрос к AS21.

## 0. Архитектура и требования

```text
Браузер :5175 (Vite /api proxy)
    → PO Agent :8004 (Agent Core V4 + LLM)
    → Task API :8003 (только read-only SWTR routes)
    → MCP-SWTR (комплектный stdio / внешний SSE)
    → REAL AS21 (корпоративная сеть и права пользователя)
```

**Принцип безопасности:** комплектный MCP-SWTR содержит также write-capable инструменты, но публичная Task API предоставляет агенту только read-only фасад. **Не публикуйте напрямую MCP SSE или Task API во внешнюю сеть без отдельного контура авторизации.**

| Компонент | Требование | Порт |
|---|---|---:|
| Git | Доступ к GitHub | — |
| MCP-SWTR | **Python 3.13+**, комплектные исходники в `mcp-swtr/` | stdio без порта; SSE обычно 3000 |
| Task API | Python **3.11+** | 8003 |
| PO Agent | Python **3.11+**, OpenAI-compatible LLM API | 8004 |
| Web UI | Node.js **20+**, npm (рекомендуется Node 22) | 5175 |
| AS21 | Корпоративный доступ/VPN, URL SWTR и действительный токен с правами чтения | внешний |

На Windows рекомендуем **WSL2**, поскольку инструкции и wrapper используют Bash. При наличии SSE-сервера организации отдельная локальная установка MCP не нужна.

## 1. Получение исходников

```bash
git clone https://github.com/Sovietbear86/PO-Agent-Architecture-Public.git
cd PO-Agent-Architecture-Public
git switch main
git pull --ff-only
git rev-parse --short HEAD
test -f mcp-swtr/mcp_server.py
python3 scripts/prepublish_scan.py
```

Исходники Python MCP-SWTR уже включены в публичную поставку. **GitVerse отдельно скачивать не нужно**. Если `mcp-swtr/mcp_server.py` отсутствует, проверьте, что клонирован именно актуальный `main`.

Прежде чем устанавливать зависимости, убедитесь, что порты 8003, 8004, 5175 не заняты другими сервисами. Не останавливайте существующее приложение без выяснения причин.

## 2. Конфигурация продуктов и сотрудников

В `task-api/config/products.yaml` замените шаблонные `PRD1` / `PRD2` на **реальные коды пространств AS21**, доступные вашей учётной записи. Пример структуры (PAY/CRM — условные идентификаторы, не гарантия существования):

```yaml
products:
  PAY:
    display_name: "Payments"
    aliases: ["PAY", "Payments"]
    s21_projects: []
    s21_components: []
```

Поля `s21_projects` и `s21_components` заполняются в соответствии с конкретными сценариями и контрактами AS21. Пустые списки в примерах **не означают**, что все продуктовые отчёты заработают без настройки.

Согласуйте `task-api/config/team_members.yaml`: `id`/`login` должны соответствовать реальным логинам AS21, а `products` — ключам `products.yaml`. Шаблонных сотрудников нельзя выдавать за фактическую команду. Не добавляйте персональные данные в публичный Git.

В `po-agent-platform-v2/frontend/.env` (создать из `.env.example`) задайте `VITE_PRODUCT_LABELS` и другие пользовательские подписи для своих пространств. При изменении настроек перезапускайте Agent и Vite.

## 3. Локальные переменные окружения (секреты)

Создайте три файла **только локально**:

```bash
cp task-api/.env.example task-api/.env
cp po-agent-platform-v2/.env.example po-agent-platform-v2/.env
cp po-agent-platform-v2/frontend/.env.example po-agent-platform-v2/frontend/.env
chmod 600 task-api/.env po-agent-platform-v2/.env po-agent-platform-v2/frontend/.env
```

Если файл уже существует, **не перезаписывайте его**. Все `.env` игнорируются Git; никогда не коммитьте их и не прикладывайте к переписке, заявкам или QA-отчётам.

**Рекомендуемая конфигурация `task-api/.env` (stdio):**

```dotenv
SWTR_MCP_TRANSPORT=stdio
SWTR_TOKEN=YOUR_SWTR_TOKEN
SWTR_MCP_BASE_URL=https://YOUR-AS21-SWTR-ENDPOINT
FRONTEND_ORIGIN=http://localhost:5175
```

`SWTR_MCP_SERVER_DIR` **оставьте незаданным**: корневой `mcp-swtr-wrapper.sh` автоматически выберет встроенный `mcp-swtr/` и `mcp-swtr/.venv/bin/python`. Отдельно запускать MCP на :3000 **в stdio не требуется**.

**Альтернатива — уже работающий корпоративный SSE:**

```dotenv
SWTR_MCP_TRANSPORT=sse
SWTR_MCP_SSE_URL=http://127.0.0.1:3000/sse
```

Настройка авторизации внешнего SSE зависит от его владельца. Не запускайте локальный MCP одновременно в stdio и SSE «на всякий случай».

**Настройки `po-agent-platform-v2/.env`:**

```dotenv
AS21_MODE=task-api
TASK_API_BASE_URL=http://127.0.0.1:8003
TASK_API_TIMEOUT_SECONDS=120
AGENT_CORE_V4_ENABLED=true

TEAM_CONFIG_PATH=../task-api/config/team_members.yaml
PRODUCTS_CONFIG_PATH=../task-api/config/products.yaml

LLM_API_BASE_URL=https://YOUR-OPENAI-COMPATIBLE-ENDPOINT/v1
LLM_API_KEY=YOUR_LLM_API_KEY
LLM_MODEL_NAME=YOUR_MODEL_ID
LLM_TLS_VERIFY=true
```

Укажите свои действительные параметры **локально**. Для проверки связи с AS21 нужен SWTR-токен и сеть/VPN. Для полноценной работы агента также необходим доступный LLM API. Не отключайте TLS-проверку ради обхода ошибки подключения.

## 4. Установка зависимостей

Из корня клона (команды для macOS/Linux/WSL2):

```bash
# MCP-SWTR: Python 3.13+
cd mcp-swtr
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
cd ..

# Task API: Python 3.11+
cd task-api
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
cd ..

# Agent: Python 3.11+
cd po-agent-platform-v2
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
deactivate
cd ..

# UI: Node 20+
cd po-agent-platform-v2/frontend
npm ci
npm run build
cd ../..
```

Если `python3.13` не найден — установите нужную версию Python, а не заменяйте её неподдерживаемой 3.11 для MCP. В контейнерном варианте Dockerfile использует `python:3.13-slim`, не включает токен в образ, а секреты подаются на этапе запуска контейнера.

## 5. Запуск сервисов (три терминала)

**Терминал №1 — Task API**, из корня репозитория:

```bash
cd task-api
. .venv/bin/activate
set -a
. ./.env
set +a
uvicorn main:app --host 127.0.0.1 --port 8003
```

Файл `.env` здесь создан вами и должен считаться доверенным: команда `source` исполняет его как shell. Никогда не применяйте её к чужому/непроверенному файлу.

**Терминал №2 — PO Agent:**

```bash
cd po-agent-platform-v2
. .venv/bin/activate
uvicorn po_agent.main:app --host 127.0.0.1 --port 8004
```

**Терминал №3 — Web UI:**

```bash
cd po-agent-platform-v2/frontend
npm run dev -- --host 127.0.0.1
```

Адрес UI: `http://127.0.0.1:5175`. Vite проксирует `/api` на Agent :8004. Браузер **не должен обращаться к MCP напрямую**.

В stdio MCP стартует автоматически внутри Task API через wrapper при обращении к инструментам. Запуск SSE MCP — отдельный режим, управляется параметрами из шага 3.

## 6. Обязательный health check

Из **корня** публичного клона:

```bash
# Без валидной задачи покажет INCOMPLETE (это корректно, а не GREEN).
python3 scripts/public_health_check.py

# Полная проверка: замените код реально существующей доступной задачи.
python3 scripts/public_health_check.py --task-code PAY-123 --probe-agent
```

`PAY-123` — только демонстрация формата. Для настоящего сертификата нужно указать **существующий ID из своего AS21**. Скрипт проверяет:

- H0 — комплектные исходники MCP;
- H1 — Task API liveness;
- H2 — MCP connection, read tool registry и число инструментов;
- H3 — Agent V4 readiness, `adapter=task-api`, source healthy;
- H4 — доступность frontend HTML;
- H5 — **настоящее ограниченное чтение задачи из REAL AS21**;
- H6 — один запрос к агенту с проверкой `COMPLETED` и source evidence.

**Коды завершения:** `0 GREEN`, `1 RED`, `2 INCOMPLETE` (например, нет валидного кода или не выполняли LLM-запрос). `--json` выдаёт только технические поля без исходных данных AS21.

Для реального E2E дополнительно проверьте в браузере открытие Web UI, отправку запроса и отсутствие ошибок в DevTools. Один `200 OK` на `/health` не доказывает подключение к AS21 или готовность LLM.

## 7. Если коллега не видит данные AS21

| Симптом | Что проверить |
|---|---|
| `mcp-swtr/mcp_server.py` отсутствует | старый clone/не тот репозиторий; обновить публичный main |
| Task API :8003 не отвечает | запущен ли uvicorn, правильный venv и порт |
| Task API жив, MCP health = 503 | `SWTR_MCP_TRANSPORT`, wrapper, Python 3.13, установлен ли `fastmcp`, наличие env (**не значения**) |
| MCP connected (48 tools), AS21 read = 401/403 | токен истёк/нет прав, проверьте через корпоративный процесс без публикации токена |
| MCP connected, AS21 read = 502/timeout | `SWTR_MCP_BASE_URL`, VPN/DNS, TLS, маршрутизация до SWTR |
| Результат пустой | сначала подтвердить доступ к конкретной известной задаче и правильное пространство; не объявлять пустоту фактом без источника |
| AS21 read GREEN, Agent health = degraded | `AS21_MODE=task-api`, `TASK_API_BASE_URL`, `AGENT_CORE_V4_ENABLED`, readiness |
| AS21 GREEN, Agent query FAILED/timeout | LLM endpoint/model/key, таймауты и trace; не подменять fake-режимом |
| Agent работает, UI пустой | Vite :5175 → proxy `/api` → :8004, CORS/Network/Console |

Можно отдельно проверить состояние сервисов:

```bash
curl -fsS http://127.0.0.1:8003/health
curl -fsS http://127.0.0.1:8003/api/v1/swtr-read/health
curl -fsS http://127.0.0.1:8004/api/v1/health
```

Не публикуйте сырые ответы на задачи и внутренние идентификаторы/URLs в открытых issue. Для передачи отчёта используйте только санитизированный результат health-check.

## 8. Безопасность и границы поддержки

- **Никогда** не храните SWTR/LLM токены, JWT, cookies, private keys и реальные `.env` в Git. Учитывайте, что удаление секрета из HEAD не удаляет его из истории; скомпрометированные токены нужно **отзывать и перевыпускать**.
- Не включайте внешнюю публикацию localhost-сервисов без отдельной аутентификации/изоляции сессий. Локальный запуск — не многопользовательская production-готовность.
- Настройка `products.yaml` и `team_members.yaml` не заменяет сетевые права доступа к AS21.
- Навык `public-deploy` отвечает только за установку; `public-health-check` выдаёт проверяемый статус готовности. Эти инструменты GigaCode **не изменяют Agent Core V4**.
- Перед публикацией форка запускайте `python3 scripts/prepublish_scan.py`; доработки в публичный `main` переносите после независимого QA.
