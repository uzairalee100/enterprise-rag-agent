# Enterprise RAG Agent

A production-shaped example of an enterprise AI agent: a LangGraph agent that
answers questions over a company's internal policy documents (RAG), calls a
mock enterprise ticketing system as a tool, returns structured/citable
answers, and is exposed both as a REST API and as an MCP server so it can be
plugged into Claude Desktop, Claude Code, or any other MCP client.

## Why this project

Built as a portfolio project for enterprise/Forward-Deployed AI Engineer
roles (e.g. SAP's FDE track). It demonstrates:

- **RAG**: chunking, embedding, and retrieval over a real (if small) enterprise
  document set (expense, IT security, PTO policies).
- **Agentic orchestration**: LangGraph `create_react_agent` with tool calling
  and a Pydantic structured output schema (answer + cited sources).
- **MCP**: the same tools (`search_policies`, `get_ticket_status`) exposed as
  an MCP server (`app/mcp_server.py`), independent of the REST API.
- **Enterprise integration shape**: a mock ticketing-system tool standing in
  for a real backend (SAP, ServiceNow, Jira, etc.) call.
- **Provider-agnostic LLM layer**: swap between Anthropic and OpenAI via one
  env var, with embeddings kept local (`sentence-transformers`) so retrieval
  doesn't require any paid API.

## Architecture

```
                  ┌─────────────────────┐
                  │   data/policies/*.md │
                  └──────────┬───────────┘
                             │ ingest.py (chunk + embed)
                             ▼
                  ┌─────────────────────┐
                  │   Chroma vector DB   │
                  └──────────┬───────────┘
                             │ search_policies()
              ┌──────────────┴───────────────┐
              ▼                              ▼
     ┌─────────────────┐           ┌────────────────────┐
     │  LangGraph agent │           │   MCP server        │
     │  (app/agent.py)  │           │ (app/mcp_server.py)  │
     └────────┬─────────┘           └─────────────────────┘
              │ ask()
              ▼
     ┌─────────────────┐
     │   FastAPI /chat  │
     │  (app/api.py)    │
     └─────────────────┘
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY or OPENAI_API_KEY
```

Set `LLM_PROVIDER=anthropic` (default) or `LLM_PROVIDER=openai` in `.env`.
Embeddings always run locally via `sentence-transformers`, so ingestion and
retrieval work even without any API key.

## Build the index

```bash
python -m app.ingest
```

## Run the API

```bash
uvicorn app.api:app --reload
```

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many PTO days do I accrue per year, and what happens to unused ones?"}'
```

## Run as an MCP server

```bash
python -m app.mcp_server
```

Point any MCP client (Claude Desktop, Claude Code) at this command to give it
`search_policies_mcp` and `get_ticket_status_mcp` tools.

## Tests

Retrieval and mock-tool tests run without any LLM API key:

```bash
pytest
```

## Project structure

```
app/
  config.py       provider-agnostic LLM + embedding setup
  vectorstore.py  Chroma index build/load
  ingest.py       CLI to (re)build the index from data/policies/
  tools.py        search_policies, get_ticket_status (shared logic)
  agent.py        LangGraph agent with structured output
  api.py          FastAPI /chat endpoint
  mcp_server.py   MCP server exposing the same tools
data/policies/    sample enterprise policy documents (the RAG corpus)
tests/            retrieval + tool tests (no API key required)
```

## Roadmap / extensions

- Swap Chroma for Qdrant/pgvector for a multi-node deployment.
- Add SAP AI Core as an additional LLM provider option.
- Add an eval harness (e.g. RAGAS) for retrieval quality regression testing.
