import os
import streamlit as st
from groq import Groq

# 1. Clear Tab title configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖")

st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Advanced ChatGPT-Style Engine Active.")

# 2. Direct Hardcoded Groq Connection - Bypasses secrets conflict completely
try:
    client = Groq(
        api_key="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"
    )
except Exception as e:
    st.error(f"Configuration Setup Error: {e}")
    st.stop()

# 3. Dynamic Session State History Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messaging elements cleanly onto viewport container
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Standard Text User Prompt Interaction Controller
if user_query := st.chat_input("Ask A.ai anything..."):
    # Append user question into application state tracking arrays
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Process response string generations via highly optimized model arrays
    with st.chat_message("assistant"):
        with st.spinner("A.ai is generating response..."):
            try:
                # Custom ChatGPT behavior persona block
                system_message = (
                    "Your name is A.ai. You are an all-knowing, highly intellectual AI assistant modeled after ChatGPT. "
                    "You were created and developed by Aayan. If asked who made you, reply proudly that Aayan made you. "
                    "CRITICAL RESPONSE RULE: If the user query is a simple greeting like 'hi', 'hello', 'hey', 'yo', or 'sup', "
                    "you MUST answer with a short, friendly, polite response in exactly one single line (e.g., 'Hello! I'm A.ai, your intelligent assistant developed by Aayan. How can I help you today?'). "
                    "For all actual informational questions, provide an advanced, highly structured, clear ChatGPT-style response "
                    "using bold markdown headings, organized bullet points, clean spacing, and informative detailed paragraphs."
                )
                
                # Dynamic Real-Time World Data Ingestion Parameter
                temporal_context = (
                    "\n[Real-Time Server Notice: The current calendar date environment parameters are active for Sunday, September 6, 2026.]"
                )

                # Feed whole context string history structures (Continuous Memory)
                api_messages = [{"role": "system", "content": system_message + temporal_context}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})

                # Direct execution request call to production Groq endpoints
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.4
                )
                
                # Extract text data safely and properly
                ai_response = ""
                try:
                    if hasattr(completion, 'choices') and len(completion.choices) > 0:
                        choice = completion.choices[0] # Fixed dictionary break fix applied!
                        if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                            ai_response = str(choice.message.content)
                        else:
                            ai_response = str(choice)
                    else:
                        ai_response = str(completion)
                except Exception:
                    ai_response = str(completion)

                # Render the final text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
