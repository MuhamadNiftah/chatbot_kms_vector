from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import sys
import io

# Fix encoding untuk Windows 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("⏳ Sedang memuat Vectorstore...")
# Load model embedding
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load Vectorstore
vectorstore_path = os.path.join(BASE_DIR, "vectorstore")
try:
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
    
    # Ambil semua data (dict) yang ada di docstore (index.pkl)
    all_docs = db.docstore._dict

    print(f"\n✅ Ditemukan {len(all_docs)} Chunks di dalam database.\n")
    print("="*50)

    # Looping untuk menampilkan isi setiap chunk
    for i, (doc_id, doc_data) in enumerate(all_docs.items()):
        print(f"CHUNK #{i+1}")
        print(f"Sumber   : {doc_data.metadata.get('source', 'Unknown')}")
        print(f"Kategori : {doc_data.metadata.get('category', 'Umum')}")
        print(f"Isi Teks : {doc_data.page_content[:200]}... (dipotong)")
        print("-" * 50)
except Exception as e:
    print(f"❌ Gagal memuat Vectorstore. Pastikan folder vectorstore ada. Error: {e}")
