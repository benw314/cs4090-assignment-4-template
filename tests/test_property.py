from hypothesis import given, strategies as st
from src.tasks import generate_unique_id

@given(st.lists(st.dictionaries(keys=st.just("id"), values=st.integers(min_value=1, max_value=100))))
def test_generate_unique_id_always_unique(task_list):
    result = generate_unique_id(task_list)
    existing_ids = [t["id"] for t in task_list]
    assert result not in existing_ids or result == max(existing_ids) + 1
