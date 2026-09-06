from app.vectorstore import get_vectorstore

_MOCK_TICKETS = {
    "TCK-1001": {"status": "Approved", "type": "Expense Reimbursement", "amount": 240.50},
    "TCK-1002": {"status": "Pending Manager Approval", "type": "PTO Request", "days": 5},
    "TCK-1003": {"status": "Rejected", "type": "Expense Reimbursement", "reason": "Missing receipt"},
}


def search_policies(query: str, k: int = 4) -> str:
    """Search the enterprise policy knowledge base and return relevant excerpts with sources."""
    store = get_vectorstore()
    results = store.similarity_search(query, k=k)
    if not results:
        return "No relevant policy content found."
    formatted = []
    for doc in results:
        source = doc.metadata.get("source", "unknown")
        formatted.append(f"[source: {source}]\n{doc.page_content}")
    return "\n\n".join(formatted)


def get_ticket_status(ticket_id: str) -> str:
    """Look up the status of an HR/expense ticket by ID in the (mock) enterprise ticketing system."""
    ticket = _MOCK_TICKETS.get(ticket_id.upper())
    if not ticket:
        return f"No ticket found with ID '{ticket_id}'."
    return f"Ticket {ticket_id.upper()}: {ticket}"
