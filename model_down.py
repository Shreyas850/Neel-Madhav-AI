from huggingface_hub import hf_hub_download
import os

def download_optimized_model():
    print("🚀 Downloading Phi-3 Mini (Optimized for GTX 1650)...")
    
    # Approx 2.4GB - Fits perfectly in your 4GB VRAM
    model_name = "microsoft/Phi-3-mini-4k-instruct-gguf"
    filename = "Phi-3-mini-4k-instruct-q4.gguf"
    
    path = hf_hub_download(
        repo_id=model_name, 
        filename=filename,
        local_dir="."  
    )
    
    print(f"✅ Download Complete: {path}")

if __name__ == "__main__":
    download_optimized_model()