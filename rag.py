from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_vectorstore():
    return FAISS.load_local(
        "vectorstore",
        embeddings_model,
        allow_dangerous_deserialization=True
    )

def retrieve_context(question: str, k: int = 4) -> str:
    db = load_vectorstore()
    results = db.similarity_search(question, k=k)

    context = ""
    for doc in results:
        source = doc.metadata.get("source", "unknown")
        page   = doc.metadata.get("page", "-")
        context += f"[Sumber: {source}, Halaman: {page}]\n"
        context += doc.page_content + "\n\n"

    return context.strip()