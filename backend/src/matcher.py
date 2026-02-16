
import json
import os
from sentence_transformers import SentenceTransformer, util
import sys

# Initialize global model
# Use a small, fast model. 
# 'all-MiniLM-L6-v2' is standard and very fast.
MODEL_NAME = 'all-MiniLM-L6-v2'

class IntentMatcher:
    def __init__(self, dataset_path="backend/data/dataset.json", threshold=0.75):
        self.dataset_path = dataset_path
        self.threshold = threshold
        self.model = SentenceTransformer(MODEL_NAME)
        self.data = []
        self.embeddings = None
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.dataset_path):
            print(f"Warning: Dataset not found at {self.dataset_path}")
            return
            
        with open(self.dataset_path, 'r') as f:
            self.data = json.load(f)
        
        # Pre-compute embeddings for instructions
        instructions = [item['instruction'] for item in self.data]
        print("Encoding dataset instructions...")
        self.embeddings = self.model.encode(instructions, convert_to_tensor=True)
        print("Dataset encoded.")

    def find_match(self, query):
        if not self.data or self.embeddings is None:
            return None
            
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Compute cosine similarity
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        
        # Find best match
        best_score_idx = int(cos_scores.argmax())
        best_score = float(cos_scores[best_score_idx])
        
        if best_score >= self.threshold:
            match = self.data[best_score_idx]
            return {
                "match_found": True,
                "score": best_score,
                "response": match['output'],
                "original_instruction": match['instruction']
            }
        
        return {"match_found": False, "score": best_score, "response": None}

if __name__ == "__main__":
    # Test
    matcher = IntentMatcher(dataset_path="../data/dataset.json")
    print(matcher.find_match("What are the docs for home loan?"))
