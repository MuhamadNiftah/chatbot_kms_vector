import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Sedang memuat Vectorstore FAISS...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(
        os.path.join(BASE_DIR, "vectorstore"),
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    total_docs = db.index.ntotal
    output_file = os.path.join(BASE_DIR, "embeddings_terbaca.txt")
    
    print(f"Ditemukan {total_docs} chunk dokumen. Menyimpan ke format teks yang bisa dibaca...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== DAFTAR EMBEDDING (Total: {total_docs} chunks) ===\n")
        f.write("Di bawah ini adalah isi asli dari index.faiss yang sudah diterjemahkan ke angka desimal agar bisa dibaca manusia.\n\n")
        
        for i in range(total_docs):
            # Ambil array angka
            emb_array = db.index.reconstruct(i).tolist()
            # Format menjadi string dengan 8 angka di belakang koma (seperti -0.01078816)
            emb_str = ", ".join([f"{num:.8f}" for num in emb_array])
            
            # Coba ambil informasi teks aslinya jika ada
            try:
                doc_id = db.index_to_docstore_id[i]
                doc = db.docstore.search(doc_id)
                teks = doc.page_content[:150].replace('\n', ' ') + "..."
                sumber = doc.metadata.get('source', 'Tidak diketahui')
            except Exception:
                teks = "Tidak ada metadata teks."
                sumber = "Unknown"
            
            f.write(f"--- [ INDEX KE-{i} ] ---\n")
            f.write(f"Sumber Dokumen : {sumber}\n")
            f.write(f"Cuplikan Teks  : {teks}\n")
            f.write(f"Array Angka ({len(emb_array)} Dimensi) :\n")
            f.write(f"[{emb_str}]\n\n")
            
    print(f"SELESAI! Silakan buka file {output_file} untuk melihat angka-angkanya secara langsung.")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
