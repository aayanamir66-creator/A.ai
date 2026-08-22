import os
import streamlit as st
from groq import Groq

# 1. Title aur Page configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖")

st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Simple Text Mode Active with Forever Memory.")

# 2. Groq Client Connection Safely
if "GROQ_API_KEY" in os.environ:
    client = Groq()
else:
    client = Groq(api_key="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")

# 3. Chat History aur Hamesha Yaad Rakhne Waali Memory System
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani saari baatein screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Sirf Sawal Aur Jawab Waala Input Box
if user_query := st.chat_input("Ask A.ai anything..."):
    # User ka sawal memory aur screen par save karein
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # AI ka jawab process karein
    with st.chat_message("assistant"):
        with st.spinner("A.ai is thinking..."):
            try:
                # Persona Prompt text
                system_message = (
                    "Your name is A.ai. You are an all-knowing, highly intelligent general assistant. "
                    "You were created and developed by Aayan. If asked who made you, reply proudly that Aayan made you."
                )
                
                # Latest News context (Forces active 2026 updates)
                temporal_context = (
                    "\n[Real-Time Server Notice: The current date environment parameters are active for Saturday, August 22, 2026. "
                    "Synthesize world knowledge accurately incorporating current global events and updates for August 2026.]"
                )

                # Saari purani baatein (Forever Memory) model ko bhejna
                api_messages = [{"role": "system", "content": system_message + temporal_context}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})

                # Rock-solid stable text model endpoint call
                completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=api_messages,
                    temperature=0.3
                )
                
                # Extraction logic for your account format
                try:
                    ai_response = completion.choices.message.content
                except (TypeError, AttributeError, KeyError):
                    if isinstance(completion, dict):
                        ai_response = completion.get('choices', [{}]).get('message', {}).get('content', str(completion))
                    elif hasattr(completion, 'choices') and isinstance(completion.choices, list):
                        ai_response = completion.choices.message.content if hasattr(completion.choices, 'message') else str(completion.choices)
                    else:
                        ai_response = str(completion)
                
                # Cleanup raw tags
                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()

                # Screen par display karein aur memory mein daal dein
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
