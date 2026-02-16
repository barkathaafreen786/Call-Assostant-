
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

try:
    from matcher import IntentMatcher
    from slm import SLMHandler
    from rag import RAGEngine
except ImportError:
    # Fallback for relative imports if run as module
    from .matcher import IntentMatcher
    from .slm import SLMHandler
    from .rag import RAGEngine

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BFSI AI Assistant")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Components
# Use absolute paths or reliable relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")

try:
    matcher = IntentMatcher(dataset_path=os.path.join(DATA_DIR, "dataset.json"))
    slm = SLMHandler(model_path=os.path.join(MODELS_DIR, "tiny_model.gguf"))
    rag = RAGEngine(kb_path=os.path.join(DATA_DIR, "knowledge_base"))
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    matcher = None
    slm = None
    rag = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    source: str
    confidence: float

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    query = request.query
    logger.info(f"Received query: {query}")
    
    # 1. Tier 1: Dataset Match
    if matcher:
        match_result = matcher.find_match(query)
        if match_result and match_result["match_found"]:
            logger.info("Dataset match found.")
            return QueryResponse(
                response=match_result["response"],
                source="dataset",
                confidence=match_result["score"]
            )

    # 2. Tier 3: RAG Retrieval (Check if knowledge is needed)
    context = ""
    if rag:
        retrieved_docs = rag.retrieve(query)
        if retrieved_docs:
            context = "\n".join(retrieved_docs)
            logger.info(f"Retrieved {len(retrieved_docs)} chunks.")

    # 3. Tier 2: SLM Response
    if slm:
        system_prompt = "You are a helpful BFSI assistant. Use the following context to answer the user's question. If you don't know, say so."
        if context:
            system_prompt += f"\nContext:\n{context}"
            source = "rag"
        else:
            source = "slm"
            
        try:
            response_text = slm.generate_response(system_prompt, query)
            return QueryResponse(
                response=response_text,
                source=source,
                confidence=0.5
            )
        except Exception as e:
            logger.error(f"SLM failed: {e}")
            return QueryResponse(
                response="I am currently experiencing high load. Please try again later.",
                source="error",
                confidence=0.0
            )

    return QueryResponse(
        response="Please ensure backend components are initialized.",
        source="system_error",
        confidence=0.0
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "components": {
            "matcher": matcher is not None,
            "slm": slm is not None,
            "rag": rag is not None
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
