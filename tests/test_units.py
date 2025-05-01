from src.tasks import load_tasks, save_tasks, generate_unique_id
import pytest
import os

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Test 1", "completed": False},
        {"id": 2, "title": "Test 2", "completed": True}
    ]

def test_load_tasks(tmp_path):
    test_file = tmp_path / "test_tasks.json"
    test_file.write_text('[{"id": 1, "title": "Test"}]')
    tasks = load_tasks(test_file)
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test"

def test_save_tasks(tmp_path, sample_tasks):
    test_file = tmp_path / "test_tasks.json"
    save_tasks(sample_tasks, test_file)
    assert os.path.exists(test_file)
    assert test_file.read_text() == '[{"id": 1, "title": "Test 1", "completed": false}, {"id": 2, "title": "Test 2", "completed": true}]'

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 3
    assert generate_unique_id([]) == 1