import pytest
from tasks import filter_tasks_by_priority, filter_tasks_by_category

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 2),
    ("Medium", 1),
    ("Low", 0)
])
def test_filter_tasks_by_priority(priority, expected_count):
    sample_tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "Medium"},
        {"id": 3, "priority": "High"}
    ]
    filtered = filter_tasks_by_priority(sample_tasks, priority)
    assert len(filtered) == expected_count

def test_filter_tasks_by_category_mock(monkeypatch):
    # Simulate tasks and override behavior
    sample_tasks = [
        {"id": 1, "category": "Work"},
        {"id": 2, "category": "School"},
        {"id": 3, "category": "Work"}
    ]

    monkeypatch.setattr("tasks.load_tasks", lambda: sample_tasks)

    from tasks import load_tasks, filter_tasks_by_category
    tasks = load_tasks()
    filtered = filter_tasks_by_category(tasks, "Work")
    assert len(filtered) == 2
