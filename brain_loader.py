from llama_cpp import Llama
import os
import sys

# ✅ MODEL CONFIGURATION
MODEL_PATH = "kanha.gguf"

print("\n🔄 CONNECTING TO GPU (CUDA)...")

try:
    # Initialize the Model directly on GPU
    llm = Llama(
        model_path=MODEL_PATH,
        n_gpu_layers=-1,      # 🚀 -1 means "Load ALL layers to GPU"
        n_ctx=4096,           # Context window (keep 2048 for speed)
        n_threads=6,          # CPU threads for preprocessing
        verbose=False         # Silence the technical logs
    )
    print("✅ NEEL MADHAV IS RUNNING ON GPU (High Speed Mode).")

except Exception as e:
    print(f"❌ GPU ERROR: {e}")
    print("⚠️ Falling back to CPU mode (Slow)...")
    try:
        llm = Llama(model_path=MODEL_PATH, n_gpu_layers=0, n_ctx=2048, verbose=False)
    except:
        llm = None
        print("❌ CRITICAL: Could not load model.")

def query(system_prompt, user_text, mode="chat"):
    """
    Sends text to Phi-3 on the GPU and returns the response.
    """
    if not llm:
        return "Brain is sleeping."

    # ✅ STRICT PHI-3 PROMPT FORMAT (Optimized for Chat)
    full_prompt = f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_text}<|end|>\n<|assistant|>\n"

    try:
        # Generate Response
        output = llm(
            full_prompt,
            max_tokens=100,       # Keep it short for instant reply
            stop=["<|end|>", "\n"], # Stop strictly when finished
            echo=False,           # Don't repeat the question
            temperature=0.7       # Creativity level
        )
        return output['choices'][0]['text'].strip()
    except Exception as e:
        return f"Brain Error: {e}"

# Test run to warm up GPU
if __name__ == "__main__":
    print(query("You are Krishna.", "Who are you?"))