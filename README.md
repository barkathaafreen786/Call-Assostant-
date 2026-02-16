
# BFSI AI Assistant

A complete AI Call Center Assistant for Banking & Financial Services. It provides instant, compliant, and accurate responses using a hybrid approach: **Dataset Matching**, **RAG**, and **Local SLM**.

## Features

-   **Hybrid AI Response**: Prioritizes curated dataset responses for safety.
-   **RAG Knowledge Base**: Retrieves complex policy details from documents.
-   **Local SLM**: Uses local LLM (defaults to mock if model missing) for conversational flow.
-   **Modern UI**: Beautiful, dark-themed React chat interface.
-   **100% Local & Private**: No cloud dependencies required.

## Quick Start

### 1. Backend Setup

1.  Make sure Python 3.10+ is installed.
2.  Install dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
3.  (Optional) Download a GGUF Model:
    -   Download `TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf` (or similar) from Hugging Face.
    -   Place it in `backend/models/tiny_model.gguf`.
    -   *If skipped, the system will use a mock SLM response.*
4.  Run the backend:
    ```bash
    # From project root
    uvicorn backend.src.app:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1.  Open a new terminal.
2.  Install dependencies:
    ```bash
    cd frontend
    npm install
    npm install lucide-react
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    Open `http://localhost:5173` in your browser.

## Project Structure

-   `backend/data/dataset.json`: Generated dataset (160+ items).
-   `backend/data/knowledge_base/`: Text files for RAG.
-   `backend/src/`: Core logic (Matcher, RAG, SLM, App).
-   `frontend/src/`: React application source code.
-   `docs/architecture.md`: Detailed architecture documentation.

## Customization

-   **Add Knowledge**: Add `.txt` files to `backend/data/knowledge_base` and restart backend.
-   **Update Responses**: Edit `backend/data/dataset.json`.
-   **Change Model**: Update `backend/src/slm.py` with path to a different GGUF model.
