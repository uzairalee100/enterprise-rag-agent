from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from app.config import get_llm
from app.tools import get_ticket_status, search_policies

SYSTEM_PROMPT = (
    "You are an enterprise HR/IT policy assistant. Use the search_policies tool "
    "to ground answers in the company's actual policy documents, and the "
    "get_ticket_status tool when a user asks about a specific ticket ID. "
    "Always cite the policy source(s) you used. If the answer isn't in the "
    "retrieved policy content, say so instead of guessing."
)


class PolicyAnswer(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    sources: list[str] = Field(
        default_factory=list, description="Policy document names cited in the answer."
    )


@tool
def search_policies_tool(query: str) -> str:
    """Search the enterprise policy knowledge base for relevant excerpts."""
    return search_policies(query)


@tool
def get_ticket_status_tool(ticket_id: str) -> str:
    """Look up the status of an HR/expense ticket by ID."""
    return get_ticket_status(ticket_id)


def build_agent():
    llm = get_llm()
    return create_react_agent(
        model=llm,
        tools=[search_policies_tool, get_ticket_status_tool],
        prompt=SYSTEM_PROMPT,
        response_format=PolicyAnswer,
    )


def ask(question: str) -> PolicyAnswer:
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["structured_response"]
