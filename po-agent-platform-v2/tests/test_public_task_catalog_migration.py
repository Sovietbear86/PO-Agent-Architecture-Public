"""Synthetic community regression for declarative task skill migration."""
from po_agent.harness.v4_plugins import task_catalog


def test_type_and_hierarchy_registered_with_live_handlers():
    skill_ids = {skill.id for skill in task_catalog.SKILLS}
    capability_ids = {cap.id for cap in task_catalog.CAPABILITIES}
    bindings = {binding.capability_id: binding for binding in task_catalog.BINDINGS}
    for key in ("task.type_analysis", "task.hierarchy"):
        assert key in skill_ids
        assert key in capability_ids
        assert key in bindings
        assert key in task_catalog.UI


def test_existing_task_collection_contract_remains_registered():
    ids = {cap.id for cap in task_catalog.CAPABILITIES}
    assert {"task.search_text", "task.search_assignee", "task.search_created",
            "task.search_status", "task.aging", "task.similar"} <= ids
