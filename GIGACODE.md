# GigaCode — PO Agent Public

Это публичная поставка PO Agent (Community). Для установки и проверки используются **ровно два** GigaCode Skills, расположенные в `.gigacode/skills/`:

- `public-deploy` → `.gigacode/skills/public-deploy/SKILL.md` — установка из чистого checkout.
- `public-health-check` → `.gigacode/skills/public-health-check/SKILL.md` — обязательная послойная приёмка и диагностика REAL AS21.

При запросах «разверни публичного агента» вызывай `public-deploy`; после завершения установки всегда используй `public-health-check`. При запросах «health check/heart check/почему нет данных AS21» сразу используй `public-health-check`.

**Главные правила:** не изменять Agent Core V4 и исходники при установке/проверке; не коммитить локальные `.env`, токены или исходные ответы AS21; raw MCP имеет write-инструменты и не должен быть доступен браузеру, только read-only Task API. Не подменять реальный AS21 fake-режимом. Если не выполнено реальное чтение и проверка LLM — результат `INCOMPLETE`, а не `GREEN`. Пользователь должен вводить учётные данные локально, не в чат.

Документация: `DEPLOYMENT.md`. Автоматическая техническая проверка: `scripts/public_health_check.py`. Эти skills относятся к инфраструктуре развёртывания и **не входят** в runtime-каталог навыков PO Agent.
