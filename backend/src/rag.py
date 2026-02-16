
import os
import glob
try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    chromadb = None

class RAGEngine:
    def __init__(self, kb_path="backend/data/knowledge_base"):
        self.kb_path = kb_path
        self.client = None
        self.collection = None
        
        if chromadb:
            # Persistent client in 'data/chroma_db'
            self.client = chromadb.PersistentClient(path="backend/data/chroma_db")
            
            # Use a lightweight embedding model
            self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
            
            self.collection = self.client.get_or_create_collection(
                name="bfsi_knowledge",
                embedding_function=self.ef
            )
            self.ingest_documents()
        else:
            print("ChromaDB not installed, RAG will not function.")

    def ingest_documents(self):
        if not self.collection:
            return

        # Check if already populated (naive check)
        if self.collection.count() > 0:
            print("Knowledge base already populated.")
            return

        documents = []
        ids = []
        metadatas = []
        
        files = glob.glob(os.path.join(self.kb_path, "*.txt"))
        print(f"Found {len(files)} documents in {self.kb_path}")
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking by paragraph or fixed size
            chunks = content.split('\n\n')
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50:
                    documents.append(chunk.strip())
                    ids.append(f"{os.path.basename(file_path)}_{i}")
                    metadatas.append({"source": os.path.basename(file_path)})

        if documents:
            print(f"Ingesting {len(documents)} chunks...")
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print("Ingestion complete.")

    def retrieve(self, query, n_results=2):
        if not self.collection:
            return []
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Unpack results
        retrieved_docs = []
        if results['documents']:
             retrieved_docs = results['documents'][0]
             
        return retrieved_docs

if __name__ == "__main__":
    rag = RAGEngine(kb_path="../data/knowledge_base")
    print(rag.retrieve("What is the penalty for late payment?"))
