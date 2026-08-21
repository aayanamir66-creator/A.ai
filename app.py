import os
from groq import Groq

# Initialize the Groq Client
client = Groq()

def ask_cloud_ai(prompt, knowledge):
    target_model = "qwen/qwen3.6-27b"
    
    try:
        system_message = (
            "Your name is A.ai. You are an all-knowing, highly intelligent AI assistant. "
            "Use the following context to answer the user's question accurately. "
            f"If the answer cannot be found in the context, use your vast general knowledge.\n\nContext:\n{knowledge}"
        )
        
        # Raw API call format to avoid the choice structure parsing error
        completion = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        # Safe raw parsing strategy for your account type
        try:
            return completion.choices[0].message.content
        except (TypeError, AttributeError, KeyError):
            # Fallback parsing if the object behaves like a list or dictionary
            if isinstance(completion, dict):
                return completion.get('choices', [{}])[0].get('message', {}).get('content', str(completion))
            elif hasattr(completion, 'choices') and isinstance(completion.choices, list):
                return completion.choices[0].get('message', {}).get('content', str(completion.choices[0]))
            return str(completion)
            
    except Exception as e:
        return f"Error with model '{target_model}': {e}"

def load_local_knowledge(data_folder="data"):
    knowledge = ""
    if not os.path.exists(data_folder):
        return knowledge
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    knowledge += f"\n--- Source: {filename} ---\n" + f.read() + "\n"
            except Exception as e:
                print(f"Could not read {filename}: {e}")
    return knowledge

def main():
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable is not set!")
        return

    knowledge_base = load_local_knowledge()
    print("\n--- A.ai Engine Active (Type 'exit' to quit) ---")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower().strip() == "exit":
            print("Goodbye from A.ai!")
            break
        if not user_input.strip():
            continue
            
        print("A.ai is thinking...")
        answer = ask_cloud_ai(user_input, knowledge_base)
        print(f"\nA.ai:\n{answer}")

if __name__ == "__main__":
    main()
