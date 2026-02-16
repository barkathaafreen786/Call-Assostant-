
# BFSI AI Assistant Architecture

## 1. System Overview
The BFSI AI Assistant is a hybrid system combining rule-based matching, Small Language Models (SLM), and Retrieval-Augmented Generation (RAG) to provide fast, compliant, and accurate responses.

### Pipeline Flow
1.  **User Query** -> Interface (React) -> Backend (FastAPI)
2.  **Tier 1: Dataset Matcher** (Latency < 50ms)
    -   Checks for semantic similarity against 150+ curated Q&A pairs.
    -   If similarity > 0.85, returns strict compliant answer.
    -   Ideal for FAQs (Eligibility, Documents, contact info).
3.  **Tier 3: RAG Retrieval** (Latency ~200ms)
    -   If no direct match, retrieves relevant policies from Knowledge Base.
    -   Uses ChromaDB/FAISS with `all-MiniLM-L6-v2` embeddings.
    -   Example: "Penalty for late payment" -> Retrieves `policy.txt` section on penalties.
4.  **Tier 2: Fine-Tuned SLM** (Latency ~1-2s on CPU)
    -   Synthesizes the final answer using retrieved context + query.
    -   Uses a quantized GGUF model (e.g., TinyLlama 1.1B or Phi-2) running locally via `llama-cpp-python`.
    -   Ensures conversational flow and handles edge cases.

## 2. Component Design

### Frontend
-   **Framework**: React + Vite (Fast, modular).
-   **Design**: Dark mode, glassmorphism UI.
-   **State**: Local React state for chat history.

### Backend
-   **Framework**: FastAPI (High performance Python async framework).
-   **Matcher**: `sentence-transformers` (Cosine Similarity).
-   **RAG**: `chromadb` (Vector Store) + Text Chunking.
-   **SLM**: `llama-cpp-python` (CPU inference engine for GGUF models).

## 3. Compliance & Safety
-   **Strict Matching First**: Always prefers curated answers to avoid hallucination on critical topics (Eligibility criteria, interest rates).
-   **Context-Grounded Generation**: The SLM is instructed to use *only* provided context (RAG) for policy questions.
-   **Fallback**: If all systems fail or confidence is low, returns a standard "Please contact support" message.

## 4. Scalability
-   The dataset can be updated via JSON without retraining.
-   The knowledge base txt files can be added/edited dynamically.
-   The SLM can be swapped for larger models if hardware permits.
