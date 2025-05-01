from tasks import save_tasks, load_tasks

def test_mark_all_tasks_complete(tmp_path):
    tasks = [
        {"id": 1, "title": "A", "completed": False},
        {"id": 2, "title": "B", "completed": False}
    ]
    
    # Step 1: Save tasks
    test_file = tmp_path / "tasks.json"
    save_tasks(tasks, test_file)

    # Step 2: Implement function mark_all_tasks_complete()
    from tasks import mark_all_tasks_complete
    mark_all_tasks_complete(test_file)

    updated = load_tasks(test_file)
    assert all(task["completed"] for task in updated)
