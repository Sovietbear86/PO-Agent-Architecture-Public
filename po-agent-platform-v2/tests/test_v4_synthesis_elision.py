from __future__ import annotations

import pytest

from po_agent.harness.agent_core_v4 import V4Observation
from po_agent.harness.v4_synthesis_elision import TerminalSynthesisElider


class _UnderlyingSynthesizer:
    def __init__(self) -> None:
        self.calls = 0

    async def synthesize(self, user_query, observations):
        self.calls += 1
        return "LLM synthesis"


def _obs(step: int, capability_id: str, *, answer: str, data: dict) -> V4Observation:
    return V4Observation(
        step=step,
        capability_id=capability_id,
        arguments={},
        answer=answer,
        data=data,
    )


@pytest.mark.asyncio
async def test_elides_simple_task_collection_after_resolver():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observations = [
        _obs(
            1,
            "space.resolve",
            answer="Пространство подтверждено: DEV.",
            data={"space": "DEV"},
        ),
        _obs(
            2,
            "task.search_assignee",
            answer="Найдено задач: 2.",
            data={"count": 2, "task_keys": ["DEV-1", "DEV-2"], "source": "REAL_AS21"},
        ),
    ]

    answer = await elider.synthesize("Задачи Иванова в DEV", observations)

    assert answer == "Найдено задач: 2.\nКлючи: DEV-1, DEV-2"
    assert underlying.calls == 0


@pytest.mark.asyncio
async def test_elides_task_type_analysis_using_grounded_capability_answer():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observations = [
        _obs(
            1,
            "task.type_analysis",
            answer="Найдено задач типа «Дефект»: 1.",
            data={
                "count": 1,
                "task_keys": ["DEMO-431"],
                "type_breakdown": [{"code": "bug", "name": "Дефект", "count": 1}],
                "source": "REAL_AS21",
            },
        )
    ]

    answer = await elider.synthesize("Открытые дефекты", observations)

    assert answer == "Найдено задач типа «Дефект»: 1."
    assert underlying.calls == 0


@pytest.mark.asyncio
async def test_elides_lookup_and_hierarchy_answers():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)

    lookup = await elider.synthesize(
        "DEMO-267",
        [_obs(1, "task.lookup", answer="DEMO-267: Тестовая задача — В работе.", data={"task_key": "DEMO-267"})],
    )
    hierarchy = await elider.synthesize(
        "Покажи иерархию DEMO-267",
        [_obs(
            1,
            "task.hierarchy",
            answer="Для DEMO-267: уровней родителей — 2. Эпик: DEMO-349.",
            data={"task_key": "DEMO-267", "depth": 2, "epic_key": "DEMO-349"},
        )],
    )

    assert lookup == "DEMO-267: Тестовая задача — В работе."
    assert hierarchy == "Для DEMO-267: уровней родителей — 2. Эпик: DEMO-349."
    assert underlying.calls == 0


@pytest.mark.asyncio
async def test_delegates_multi_terminal_trajectory():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observations = [
        _obs(1, "task.search", answer="Найдено задач: 2.", data={"count": 2}),
        _obs(2, "task.hierarchy", answer="Иерархия построена.", data={"depth": 2}),
    ]

    answer = await elider.synthesize("Сделай два разных анализа", observations)

    assert answer == "LLM synthesis"
    assert underlying.calls == 1


@pytest.mark.asyncio
async def test_delegates_unknown_non_resolver_observation():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observations = [
        _obs(1, "sprint.health", answer="Спринт стабилен.", data={"health": "green"}),
        _obs(2, "task.search", answer="Найдено задач: 1.", data={"count": 1}),
    ]

    answer = await elider.synthesize("Спринт и задачи", observations)

    assert answer == "LLM synthesis"
    assert underlying.calls == 1


@pytest.mark.asyncio
async def test_delegates_when_terminal_answer_is_empty():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observations = [
        _obs(1, "task.search", answer="", data={"count": 1, "task_keys": ["DEMO-1"]}),
    ]

    answer = await elider.synthesize("задачи", observations)

    assert answer == "LLM synthesis"
    assert underlying.calls == 1


@pytest.mark.asyncio
async def test_elision_renders_complete_compacted_key_sample():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observation = _obs(
        1,
        "task.search_assignee",
        answer="Для исполнителя найдено задач: 2.",
        data={
            "count": 2,
            "task_keys_sample": ["DEV-1", "DEV-2"],
            "task_key_count": 2,
            "source": "REAL_AS21",
        },
    )

    answer = await elider.synthesize("Задачи в DEV", [observation])

    assert answer == "Для исполнителя найдено задач: 2.\nКлючи: DEV-1, DEV-2"
    assert underlying.calls == 0


@pytest.mark.asyncio
async def test_elision_does_not_present_truncated_key_sample_as_complete():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    observation = _obs(
        1,
        "task.search_assignee",
        answer="Найдено задач: 27.",
        data={
            "count": 27,
            "task_keys_sample": [f"DEV-{i}" for i in range(20)],
            "task_key_count": 27,
            "source": "REAL_AS21",
        },
    )

    answer = await elider.synthesize("Задачи в DEV", [observation])

    assert answer == "Найдено задач: 27."
    assert "Ключи:" not in answer
    assert underlying.calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("query", [
    "Задачи Иванова в DEV и задачи Петрова в DEMO",
    "Задачи Иванова в DEV и иерархию DEMO-267",
    "DEMO-267, иерархию, задачи Иванова в DEV",
])
async def test_single_terminal_multi_intent_uses_query_aware_synthesizer(query):
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    answer = await elider.synthesize(
        query,
        [_obs(
            1, "task.search_assignee",
            answer="Найдено задач: 6.",
            data={"count": 6, "task_keys_sample": ["DEV-1"], "task_key_count": 6},
        )],
    )
    assert answer == "LLM synthesis"
    assert underlying.calls == 1


@pytest.mark.asyncio
async def test_single_intent_still_skips_llm_synthesis():
    underlying = _UnderlyingSynthesizer()
    elider = TerminalSynthesisElider(underlying)
    answer = await elider.synthesize(
        "Задачи Иванова в DEV",
        [_obs(1, "task.search_assignee", answer="Найдено задач: 1.",
              data={"count": 1, "task_keys_sample": ["DEV-1"], "task_key_count": 1})],
    )
    assert "DEV-1" in answer
    assert underlying.calls == 0
