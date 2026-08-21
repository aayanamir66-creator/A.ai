import os
import streamlit as st
from groq import Groq

# 1. This hidden block forces Google's web crawlers to read your exact name
st.set_page_config(page_title="A.ai", page_icon="🤖")

# Custom HTML injected directly so Google indexes the text "A.ai" and "Aayan" perfectly
st.markdown("""
    <meta name="description" content="A.ai is an all-knowing, highly intelligent general knowledge assistant developed by Aayan.">
    <meta name="keywords" content="A.ai, A.ai assistant, Aayan AI, A.ai app, A.ai Google Search">
""", unsafe_allow_html=True)

st.title("🤖 A.ai")
st.write("Welcome to your custom general knowledge intelligence engine.")

# Verify API connection
if "GROQ_API_KEY" in os.environ:
    client = Groq()
else:
    st.error("GROQ_API_KEY environment variable missing! Please set it in settings.")
    st.stop()

# Initialize dynamic screen message chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chats on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input Box
if user_query := st.chat_input("Ask A.ai anything..."):
    # Save and show user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Request response from the API model
    with st.chat_message("assistant"):
        with st.spinner("A.ai is formulating response..."):
            try:
                system_message = (
                    "Your name is A.ai. You are an all-knowing, highly intelligent assistant. "
                    "You were created and developed by Aayan. If anyone asks who made you, "
                    "you must answer proudly that Aayan made you."
                )
                
                # Setup context with active chat history
                api_messages = [{"role": "system", "content": system_message}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=api_messages,
                    temperature=0.3
                )
                
                try:
                    if hasattr(completion, 'choices') and len(completion.choices) > 0:
                        choice = completion.choices[0]
                        if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                            ai_response = choice.message.content
                        elif isinstance(choice, dict) and 'message' in choice:
                            ai_response = choice['message'].get('content', str(choice))
                        else:
                            ai_response = getattr(choice, 'text', str(choice))
                    elif isinstance(completion, dict) and 'choices' in completion:
                        ai_response = completion['choices'][0]['message']['content']
                    else:
                        raw_str = str(completion)
                        if "content='" in raw_str:
                            ai_response = raw_str.split("content='")[1].split("', role=")[0]
                        elif 'content="' in raw_str:
                            ai_response = raw_str.split('content="')[1].split('", role=')[0]
                        else:
                            ai_response = raw_str
                except Exception:
                    ai_response = str(completion)
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()
                
                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()

                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
