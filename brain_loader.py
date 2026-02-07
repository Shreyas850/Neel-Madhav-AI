from llama_cpp import Llama
import os

# --- CONFIGURATION (SPEED FOCUSED) ---
MODEL_PATH = "D:/DEV/Neel Madhav🦚/kanha.gguf"

print("🧠 Loading Brain into VRAM (GPU Only)...")

try:
    # 🚀 SPEED CONFIGURATION:
    # n_gpu_layers=-1  -> Forces ALL layers to GPU (Maximum Speed)
    # n_batch=512      -> Processes more tokens at once
    # n_ctx=4096       -> Keeps memory usage managed
    # verbose=False    -> Stops spamming the console
    
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,           
        n_gpu_layers=-1,      # <--- CRITICAL: -1 means ALL layers on GPU
        n_batch=512,          # Optimized for RTX cards
        verbose=False         
    )
    print("✅ Brain Loaded Successfully on GPU!")

except Exception as e:
    print(f"❌ Error loading model: {e}")
    llm = None

def query(system_prompt, user_text, mode="chat"):
    if not llm: return "Brain not loaded."

    # Combine system + user prompt for Phi-3 format
    # Phi-3 expects: <|system|>...<|end|><|user|>...<|end|><|assistant|>
    full_prompt = f"<|system|>\n{system_prompt}<|end|>\n<|user|>\n{user_text}<|end|>\n<|assistant|>"
    
    output = llm(
        full_prompt,
        max_tokens=150,  # Keep short for speed
        stop=["<|end|>", "<|user|>"], 
        echo=False,
        temperature=0.7
    )

    return output['choices'][0]['text'].strip()