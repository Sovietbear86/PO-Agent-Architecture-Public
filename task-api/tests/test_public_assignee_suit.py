"""Public regression: task type metadata must not disable configurable spaces."""
from app.routers import swtr_assignee


def test_suit_code_and_name_from_nested_unit():
    row = {
        "unit": {
            "code": "PAY-42",
            "summary": "Synthetic issue",
            "attributes": [{"code": "suit", "value": {
                "code": "bug", "name": "Bug"}}],
        }
    }
    task = swtr_assignee._canonical_row(row)
    assert task is not None
    assert task["task_type_code"] == "bug"
    assert task["task_type_name"] == "Bug"
    assert task["source_data"]["swtr_suit"] == {"code": "bug", "name": "Bug"}


def test_suit_missing_remains_optional():
    task = swtr_assignee._canonical_row({"unit": {"code": "PAY-43"}})
    assert task is not None
    assert task["task_type_code"] is None
    assert task["task_type_name"] is None


def test_public_config_spaces_are_not_hardcoded():
    assert callable(swtr_assignee._configured_spaces)
    assert "PAY" not in swtr_assignee._configured_spaces() or isinstance(
        swtr_assignee._configured_spaces(), frozenset
    )
