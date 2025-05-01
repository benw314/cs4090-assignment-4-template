import streamlit as st
import pandas as pd
import subprocess
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category

def run_test_command(label, command, working_dir="."):
    with st.spinner(f"Running {label}..."):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=working_dir
            )
            st.success(f"{label} completed.")
            st.text_area("Output", result.stdout, height=250)
            if result.stderr:
                st.error(result.stderr)
        except Exception as e:
            st.error(f"Error running {label}: {str(e)}")

def main():
    st.title("To-Do Application")

    tasks = load_tasks()

    # ---- SIDEBAR: ADD TASK ----
    st.sidebar.header("➕ Add New Task")
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit = st.form_submit_button("Add Task")

        if submit and task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added!")

    # ---- MAIN AREA: TASKS ----
    st.header("Your Tasks")
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + sorted(set(t["category"] for t in tasks)))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    show_completed = st.checkbox("Show Completed Tasks")

    filtered_tasks = tasks
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [t for t in filtered_tasks if not t["completed"]]

    for task in filtered_tasks:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{task['title']}**" + (" ✅" if task["completed"] else ""))
            st.caption(f"{task['description']}")
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with c2:
            if st.button("✅" if not task["completed"] else "↩️", key=f"complete_{task['id']}"):
                task["completed"] = not task["completed"]
                save_tasks(tasks)
                st.rerun()
            if st.button("🗑️", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    # ---- TEST PANEL ----
    with st.sidebar.expander("🧪 Testing Dashboard", expanded=True):
        st.markdown("### Unit Testing")
        if st.button("▶ Run Unit Tests"):
            run_test_command("Unit Tests", ["pytest", "tests/test_units.py", "--cov=src", "--cov-report=term-missing"])

        st.markdown("### Bug Reporting & Fixing")
        if st.button("🐞 Confirm Bug Fixes"):
            run_test_command("Bug Fix Confirmation", ["pytest", "tests/test_units.py"])

        st.markdown("### Pytest Features")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Pytest-Cov"):
                run_test_command("Coverage Report", ["pytest", "--cov=src", "--cov-report=term-missing"])
            if st.button("🧪 Parametrize"):
                run_test_command("Parametrized Tests", ["pytest", "tests/test_advanced.py"])
        with col2:
            if st.button("🕵️ Mocking"):
                run_test_command("Mock Tests", ["pytest", "tests/test_mocking.py"])
            if st.button("📝 HTML Report"):
                run_test_command("HTML Report", ["pytest", "--html=report.html", "--self-contained-html"])

        st.markdown("### Test-Driven Development (TDD)")
        if st.button("🚧 Run TDD Tests"):
            run_test_command("TDD", ["pytest", "tests/test_tdd.py"])

        st.markdown("### Behavior-Driven Development (BDD)")
        if st.button("🎭 Run BDD Tests"):
            run_test_command("BDD", ["behave"], working_dir="tests/features")

        st.markdown("### Property-Based Testing (Bonus)")
        if st.button("🔁 Run Hypothesis Tests"):
            run_test_command("Hypothesis", ["pytest", "tests/test_property.py"])

        # ---- Developer Tools ----
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧰 Developer Tools")

    if st.sidebar.button("🔁 Rerun App"):
        st.rerun()

    if st.sidebar.button("🧪 Force Rerun Tests"):
        st.session_state.pop("test_results", None)  # Clear cached results
        st.rerun()


if __name__ == "__main__":
    main()
