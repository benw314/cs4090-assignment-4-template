from behave import given, when, then
from tasks import save_tasks, load_tasks

TASK_FILE = "bdd_test_tasks.json"

@given("there are no tasks")
def step_clear_tasks(context):
    save_tasks([], TASK_FILE)

@when('the user adds a task titled "{title}"')
def step_add_task(context, title):
    tasks = load_tasks(TASK_FILE)
    new_task = {"id": len(tasks)+1, "title": title, "completed": False}
    tasks.append(new_task)
    save_tasks(tasks, TASK_FILE)

@then('the task list should contain a task titled "{title}"')
def step_check_task(context, title):
    tasks = load_tasks(TASK_FILE)
    assert any(task["title"] == title for task in tasks)
