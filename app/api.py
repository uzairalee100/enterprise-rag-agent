from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import ask

app = FastAPI(title="Enterprise RAG Agent", version="0.1.0")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = ask(request.question)
    return ChatResponse(
	    answer=result["answer"],
    	sources=result["sources"]
	)
