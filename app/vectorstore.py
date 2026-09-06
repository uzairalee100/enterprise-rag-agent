from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownTextSplitter
from langchain_core.documents import Document

from app.config import CHROMA_DIR, DATA_DIR, get_embedding_function

COLLECTION_NAME = "enterprise_policies"


def load_policy_documents() -> list[Document]:
    splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
    documents = []
    for path in sorted(DATA_DIR.glob("*.md")):
        text = path.read_text()
        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"source": path.stem, "chunk": i},
                )
            )
    return documents


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        persist_directory=str(CHROMA_DIR),
    )


def build_index(force: bool = False) -> Chroma:
    store = get_vectorstore()
    existing = store.get()["ids"]
    if existing and not force:
        return store
    if existing and force:
        store.delete(ids=existing)
    documents = load_policy_documents()
    store.add_documents(documents)
    return store
