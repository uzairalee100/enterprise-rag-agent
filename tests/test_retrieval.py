
import pytest

from app.tools import get_ticket_status, search_policies
from app.vectorstore import build_index


@pytest.fixture(scope="module", autouse=True)
def prepare_vectorstore():
    """Build the policy index before running retrieval tests."""
    build_index(force=True)


def test_pto_policy_retrieval():
    result = search_policies(
        "How many PTO days do employees accrue per year?"
    )

    assert "pto_policy" in result
    assert "21 days per year" in result


def test_expense_policy_retrieval():
    result = search_policies(
        "What is the daily meal reimbursement limit while traveling?"
    )

    assert "expense_policy" in result
    assert "$75 per day" in result


def test_it_security_policy_retrieval():
    result = search_policies(
        "What are the company password security requirements?"
    )

    assert "it_security_policy" in result
    assert "14 characters" in result


def test_pto_search_excludes_unrelated_policies():
    result = search_policies("PTO policy")

    assert "pto_policy" in result
    assert "expense_policy" not in result
    assert "it_security_policy" not in result


def test_get_ticket_status_known_id():
    result = get_ticket_status("tck-1001")

    assert "Approved" in result
    assert "240.5" in result


def test_get_ticket_status_pending_id():
    result = get_ticket_status("TCK-1002")

    assert "Pending Manager Approval" in result


def test_get_ticket_status_unknown_id():
    result = get_ticket_status("TCK-9999")

    assert "No ticket found" in result
