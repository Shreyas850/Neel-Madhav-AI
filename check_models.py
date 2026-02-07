from google import genai
import secrets

print("🔍 CONNECTING TO GOOGLE SERVERS...")

try:
    client = genai.Client(api_key=secrets.GEMINI_API_KEY)
    
    print("\n✅ AUTHORIZED MODELS FOR YOUR KEY:")
    print("-----------------------------------")
    
    # Simple loop - just print the names
    for m in client.models.list():
        print(f"👉 {m.name}")

    print("-----------------------------------")
    print("💡 TIP: Pick a name from above (e.g., 'gemini-1.5-flash') for brain_loader.py")

except Exception as e:
    print(f"\n❌ ERROR: {e}")

input("\nPress Enter to exit...")