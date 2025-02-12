from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS

# Khởi tạo mô hình embedding
embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_vector_store(text_data):
    """Tạo FAISS vector store từ danh sách nội dung."""
    valid_chunks = [chunk for chunk in text_data if chunk.strip()]
    
    # Mã hóa embedding
    embeddings = embeddings_model.encode(valid_chunks, show_progress_bar=True)
    text_embeddings = list(zip(valid_chunks, embeddings))
    
    vector_store = FAISS.from_embeddings(text_embeddings, embeddings_model)
    return vector_store
