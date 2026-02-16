
import os
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

class SLMHandler:
    def __init__(self, model_path="models/tiny_model.gguf"):
        self.model_path = model_path
        self.llm = None
        self.load_model()

    def load_model(self):
        if not Llama:
            print("Warning: llama-cpp-python not installed. Using mock SLM.")
            return

        if not os.path.exists(self.model_path):
            print(f"Warning: Model not found at {self.model_path}. Please download a GGUF model (e.g., TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf) and place it there.")
            return

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,  # Context window
                n_gpu_layers=0, # Force CPU for compatibility
                verbose=False
            )
            print("SLM Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

    def generate_response(self, system_prompt, user_query, max_tokens=256):
        if not self.llm:
            return f"[SLM Mock Response] Based on fine-tuned knowledge: Here is a helpful response to '{user_query}'."

        prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_query}</s>\n<|assistant|>\n"
        
        output = self.llm(
            prompt, 
            max_tokens=max_tokens, 
            stop=["</s>"], 
            echo=False
        )
        return output['choices'][0]['text'].strip()

if __name__ == "__main__":
    slm = SLMHandler(model_path="../models/tiny_model.gguf")
    print(slm.generate_response("You are a helpful assistant.", "What is a loan?"))
