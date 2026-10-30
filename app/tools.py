
from app.vectorstore import get_vectorstore

_MOCK_TICKETS = {
    "TCK-1001": {
        "status": "Approved",
        "type": "Expense Reimbursement",
        "amount": 240.50,
    },
    "TCK-1002": {
        "status": "Pending Manager Approval",
        "type": "PTO Request",
        "days": 5,
    },
    "TCK-1003": {
        "status": "Rejected",
        "type": "Expense Reimbursement",
        "reason": "Missing receipt",
    },
}


def search_policies(query: str, k: int = 4) -> str:
    """Search enterprise policies and return relevant excerpts."""

    store = get_vectorstore()

    results = store.similarity_search_with_relevance_scores(
        query,
        k=k,
    )

    formatted = []

    for doc, score in results:
        if score < 0.50:
            continue

        source = doc.metadata.get("source", "unknown")

        formatted.append(
            f"[source: {source}]\n{doc.page_content}"
        )

    if not formatted:
        return "No sufficiently relevant policy content found."

    return "\n\n".join(formatted)


def get_ticket_status(ticket_id: str) -> str:
    """Look up the status of an HR or expense ticket."""

    ticket_id = ticket_id.strip().upper()
    ticket = _MOCK_TICKETS.get(ticket_id)

    if not ticket:
        return f"No ticket found with ID '{ticket_id}'."

    return f"Ticket {ticket_id}: {ticket}"
