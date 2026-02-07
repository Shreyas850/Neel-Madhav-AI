from llama_cpp import Llama
import os
import sys

# 1. Check for Model
model_name = "Phi-3-mini-4k-instruct-q4.gguf"
if not os.path.exists(model_name):
    print(f"❌ ERROR: {model_name} not found.")
    print("👉 Run 'python model_down.py' first!")
    sys.exit()

print("🧪 TESTING GPU CONNECTION...")

try:
    # 2. Try to load model on GPU
    llm = Llama(
        model_path=model_name,
        n_gpu_layers=-1,      # <--- The Magic Switch (All layers to GPU)
        verbose=True          # <--- Show us the internal logs
    )
    
    print("\n" + "="*40)
    print("✅ SUCCESS! The Brain loaded successfully.")
    print("="*40)
    print("📝 CHECK THE LOGS ABOVE FOR:")
    print("   • 'BLAS = 1' (Means GPU Acceleration is ON)")
    print("   • 'ggml_cuda_init: found 1 CUDA devices' (Means GTX 1650 found)")
    print("="*40)

except Exception as e:
    print("\n❌ CRITICAL ERROR:")
    print(e)
    print("\n💡 TIP: Did you install the 'cu124' wheel correctly?")