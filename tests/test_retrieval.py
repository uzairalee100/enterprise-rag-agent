from app.tools import get_ticket_status, search_policies
from app.vectorstore import build_index


def test_index_builds_and_search_returns_relevant_chunk():
    build_index(force=True)
    result = search_policies("How many PTO days do I accrue per year?")
    assert "pto_policy" in result
    assert "accrue" in result.lower()


def test_search_covers_expense_policy():
    build_index(force=True)
    result = search_policies("What is the daily meal reimbursement limit while traveling?")
    assert "expense_policy" in result


def test_get_ticket_status_known_id():
    result = get_ticket_status("tck-1001")
    assert "Approved" in result


def test_get_ticket_status_unknown_id():
    result = get_ticket_status("TCK-9999")
    assert "No ticket found" in result
