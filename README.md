# Enterprise RAG Agent

An AI-powered enterprise assistant that answers employee questions using internal company policies, retrieves relevant information through Retrieval-Augmented Generation (RAG), and looks up HR and expense tickets using AI tools.

Built with **Python, Google Gemini, LangGraph, LangChain, ChromaDB, FastAPI, and Model Context Protocol (MCP)**.

<p align="center">

  **RAG · Agentic AI · LangGraph · MCP · FastAPI · Gemini**

</p>

---

## Overview

Enterprise RAG Agent demonstrates how an AI assistant can interact with enterprise knowledge bases and business tools.

Employees can ask questions about company policies, including paid time off, expense reimbursement, and IT security. The system retrieves relevant policy information from a ChromaDB vector database and uses Google Gemini to generate clear, context-based answers.

It also provides mock ticket lookup functionality and exposes its capabilities through both a REST API and an MCP server.

## Key Features

- **Retrieval-Augmented Generation (RAG):** Retrieve relevant information from internal Markdown policy documents.
- **Semantic Search:** Find policy information using Gemini embeddings and ChromaDB.
- **Agentic Workflow:** Use LangGraph to coordinate information retrieval and answer generation.
- **Gemini Integration:** Generate responses using Google's Gemini models.
- **Enterprise Tools:** Search company policies and retrieve HR or expense ticket statuses.
- **REST API:** Provide AI assistant functionality through FastAPI.
- **MCP Integration:** Expose policy search and ticket lookup as MCP tools.
- **Source Identification:** Return policy source names alongside generated answers.
- **Automated Testing:** Validate retrieval, ticket operations, and API endpoints using pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Google Gemini | LLM for answer generation |
| LangGraph | Agent workflow orchestration |
| LangChain | LLM and embedding integration |
| Gemini Embeddings | Text vectorization |
| ChromaDB | Vector database |
| FastAPI | REST API |
| Model Context Protocol | AI tool integration |
| Pydantic | Request and response validation |
| Pytest | Automated testing |

## System Architecture

```text
                  Enterprise Policy Documents
                            |
                            v
                     Document Ingestion
                            |
                            v
                   Gemini Embedding Model
                            |
                            v
                      ChromaDB Index
                            |
                            v
User Question ------> LangGraph Workflow
                            |
                            v
                   Information Retrieval
                            |
                  +---------+---------+
                  |                   |
                  v                   v
             Policy Search       Ticket Lookup
                  |                   |
                  +---------+---------+
                            |
                            v
                    Retrieved Context
                            |
                            v
                       Gemini LLM
                            |
                            v
                     Generated Answer
                            |
                  +---------+---------+
                  |                   |
                  v                   v
                FastAPI            MCP Server
                  |                   |
                  v                   v
             REST Clients       MCP Clients
```

## Project Structure

```text
enterprise-rag-agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── api.py
│   ├── config.py
│   ├── ingest.py
│   ├── mcp_server.py
│   ├── tools.py
│   └── vectorstore.py
│
├── data/
│   └── policies/
│       ├── expense_policy.md
│       ├── it_security_policy.md
│       └── pto_policy.md
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_retrieval.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11
- Git
- Google Gemini API key
- Internet connection for Gemini API requests

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd enterprise-rag-agent
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file in the root directory and add:

```env
GOOGLE_API_KEY=your_gemini_api_key_here

GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

**Security:** Never upload your actual `.env` file or API key to GitHub. The repository includes `.env.example` as a configuration template.

Gemini model availability, free-tier quotas, and rate limits depend on Google's current API policies.

## Build the Knowledge Base

Run the ingestion module:

```bash
python -m app.ingest
```

The ingestion pipeline:

1. Reads Markdown policy documents.
2. Splits documents into smaller text chunks.
3. Generates embeddings using Gemini.
4. Stores the vectors in ChromaDB.

The local vector database is stored in `.chroma/`.

When policy documents change, run ingestion again to rebuild the index.

## Run the API Server

Start FastAPI:

```bash
uvicorn app.api:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/chat` | Send a question to the AI assistant |

### Example Request

**POST `/chat`**

```json
{
  "question": "What is the company PTO policy?"
}
```

### Example Response

```json
{
  "answer": "Employees receive PTO according to the company policy...",
  "sources": [
    "pto_policy"
  ]
}
```

The response includes the generated answer and the names of the retrieved policy sources.

## MCP Server

The project also exposes its business tools through the Model Context Protocol.

Start the MCP server:

```bash
python -m app.mcp_server
```

### Available MCP Tools

| Tool | Description |
|---|---|
| `search_policies_mcp` | Search the enterprise policy knowledge base |
| `get_ticket_status_mcp` | Retrieve HR and expense ticket information |

The MCP server uses standard input/output (stdio) transport and can be connected to compatible MCP clients.

### Test MCP Connection

A client-side test script can initialize an MCP session and call both tools.

```bash
python test_mcp_client.py
```

The test script is included in the development workflow. If you publish it, include it in the repository root.

## Sample Ticket Records

The project currently uses a mock ticketing system.

| Ticket ID | Request Type | Status |
|---|---|---|
| TCK-1001 | Expense Reimbursement | Approved |
| TCK-1002 | PTO Request | Pending Manager Approval |
| TCK-1003 | Expense Reimbursement | Rejected |

These records demonstrate how an AI agent can interact with an external business system through tools. They are not connected to a real ticketing platform.

## Testing

Run the automated test suite:

```bash
pytest -v
```

### Test Coverage

- PTO policy retrieval
- Expense policy retrieval
- IT security policy retrieval
- Exclusion of unrelated policy results
- Known ticket lookup
- Pending ticket lookup
- Unknown ticket handling
- FastAPI health endpoint
- FastAPI chat endpoint
- Invalid chat request validation

### Current Test Results

**10 tests passed**

The chat endpoint test uses a mocked response, so it does not consume Gemini generation quota. Retrieval tests require a working Gemini embedding API key and available quota.

## Current Limitations

- The knowledge base currently contains three sample policy documents.
- Ticket information is stored in an in-memory mock database.
- Gemini is the configured LLM and embedding provider.
- Retrieval uses semantic similarity and a relevance threshold that requires broader evaluation.
- Authentication and role-based access control are not implemented.
- The project has not yet been hardened for production deployment.
- No real enterprise ticketing system is connected.

## Future Improvements

- Implement hybrid search using semantic and keyword retrieval.
- Add RAG evaluation with RAGAS or a custom evaluation framework.
- Integrate real ticketing platforms such as ServiceNow or Jira.
- Add authentication and role-based access control.
- Implement conversation memory.
- Add structured logging, observability, and monitoring.
- Containerize the application using Docker.
- Deploy the application to a cloud platform.

## Contact

**Uzair Alee**

- **Email:** [uzairalee100@gmail.com](mailto:uzairalee100@gmail.com)
- **GitHub:** [github.com/uzairalee100](https://github.com/uzairalee100)

For questions, suggestions, collaboration, or opportunities related to this project, feel free to reach out.

---

<p align="center">

  **Built with Python and Google Gemini.**

  *Exploring practical applications of RAG, Agentic AI, and enterprise automation.*

</p>