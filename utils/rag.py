"""
RAG pipeline: chunk documents, embed them locally with ChromaDB's built-in
ONNX-based embedding model, store/retrieve via a local ChromaDB instance.

NOTE: We deliberately use ChromaDB's DefaultEmbeddingFunction (ONNX runtime,
already a ChromaDB dependency) instead of sentence-transformers/torch. The
torch + transformers + sentence-transformers stack is heavy enough that it
can exceed Streamlit Community Cloud's free-tier build resources and hang
during dependency installation. The ONNX-based MiniLM model used here is
functionally similar (same underlying MiniLM architecture) at a fraction of
the install footprint.
"""

import uuid
import chromadb
from chromadb.utils import embedding_functions
try:
    # LangChain >= 1.0 split text_splitter out into its own package
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Fall back for older LangChain (< 1.0) where it lived in langchain.text_splitter
    from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 4


class RAGStore:
    def __init__(self, persist_directory: str = "./chroma_store"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        # Lightweight ONNX embedder (no torch/transformers needed)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="sage_documents",
            embedding_function=self.embedding_fn,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def add_document(self, filename: str, text: str) -> int:
        """Chunk + embed + store a document. Returns number of chunks stored."""
        chunks = self.splitter.split_text(text)
        if not chunks:
            return 0

        ids = [f"{filename}-{uuid.uuid4().hex[:8]}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        return len(chunks)

    def query(self, question: str, top_k: int = TOP_K) -> list[dict]:
        """Retrieve the most relevant chunks for a question."""
        if self.collection.count() == 0:
            return []

        results = self.collection.query(query_texts=[question], n_results=min(top_k, self.collection.count()))

        hits = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            hits.append({"text": doc, "source": meta.get("source", "unknown"), "distance": dist})
        return hits

    def has_documents(self) -> bool:
        return self.collection.count() > 0

    def clear(self):
        self.client.delete_collection("sage_documents")
        self.collection = self.client.get_or_create_collection(
            name="sage_documents",
            embedding_function=self.embedding_fn,
        )


def build_rag_prompt(question: str, hits: list[dict]) -> str:
    """Builds a grounded prompt from retrieved chunks. Falls back gracefully if no hits."""
    if not hits:
        return (
            f"The user asked: \"{question}\"\n\n"
            "No relevant content was found in the uploaded documents. "
            "Tell the user you couldn't find relevant information in their documents "
            "for this question, and answer only if it's general knowledge you're confident about, "
            "clearly labeling it as not being from their documents."
        )

    context_blocks = []
    for h in hits:
        context_blocks.append(f"[Source: {h['source']}]\n{h['text']}")
    context = "\n\n---\n\n".join(context_blocks)

    return (
        "Answer the user's question using ONLY the context below when relevant. "
        "If the context doesn't fully answer it, say what's missing rather than guessing.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}"
    )
