import os
from pathlib import Path

# Some corporate proxies corrupt HuggingFace's "xet" transfer protocol;
# fall back to plain HTTP downloads unless the user has set this explicitly.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "policies"
CHROMA_DIR = PROJECT_ROOT / ".chroma"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_llm(temperature: float = 0.0):
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=OPENAI_MODEL, temperature=temperature)
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=ANTHROPIC_MODEL, temperature=temperature)
    raise ValueError(
        f"Unsupported LLM_PROVIDER '{LLM_PROVIDER}'. Use 'anthropic' or 'openai'."
    )


def get_embedding_function():
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
