from mcp.server.fastmcp import FastMCP

from app.tools import get_ticket_status, search_policies

mcp = FastMCP("enterprise-policy-server")


@mcp.tool()
def search_policies_mcp(query: str) -> str:
    """Search the enterprise policy knowledge base (expense, IT security, PTO) and return relevant excerpts with sources."""
    return search_policies(query)


@mcp.tool()
def get_ticket_status_mcp(ticket_id: str) -> str:
    """Look up the status of an HR/expense ticket by ID, e.g. TCK-1001."""
    return get_ticket_status(ticket_id)


if __name__ == "__main__":
    mcp.run()
