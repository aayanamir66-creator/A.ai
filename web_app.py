import os
import streamlit as st
from groq import Groq

# 1. Clear Tab title configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖")

st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Advanced ChatGPT-Style Engine Active.")

# 2. Initialize Groq API Client Connection Safely
if "GROQ_API_KEY" in os.environ:
    client = Groq()
else:
    client = Groq(api_key="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")

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
                
                # Dynamic Real-Time World Data Ingestion Parameter (August 2026 calibration)
                temporal_context = (
                    "\n[Real-Time Server Notice: The current calendar date environment parameters are active for Saturday, August 22, 2026. "
                    "Synthesize your world knowledge accurately incorporating current global events and structural world updates for August 2026.]"
                )

                # Feed whole context string history structures (Continuous Memory)
                api_messages = [{"role": "system", "content": system_message + temporal_context}]
                for msg in st.session_state.messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})

                # Direct execution request call to production endpoints
                completion = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=api_messages,
                    temperature=0.4
                )
                
                # Extract text data accurately from the received server response block
                try:
                    ai_response = completion.choices.message.content
                except (TypeError, AttributeError, KeyError):
                    if isinstance(completion, dict):
                        ai_response = completion.get('choices', [{}]).get('message', {}).get('content', str(completion))
                    elif hasattr(completion, 'choices') and isinstance(completion.choices, list):
                        ai_response = completion.choices.message.content if hasattr(completion.choices, 'message') else str(completion.choices)
                    else:
                        ai_response = str(completion)
                
                # Robust extraction filter block that cleanly chops off the raw object trailing metadata string strings
                if ", role='assistant'" in ai_response:
                    ai_response = ai_response.split(", role='assistant'")
                if "', role=" in ai_response:
                    ai_response = ai_response.split("', role=")
                if '", role=' in ai_response:
                    ai_response = ai_response.split('", role=')
                if "content='" in ai_response:
                    ai_response = ai_response.split("content='")[-1]
                if 'content="' in ai_response:
                    ai_response = ai_response.split('content="')[-1]
                if "[Choice(finish_reason=" in ai_response:
                    ai_response = ai_response.split("[Choice(finish_reason=")

                # Strip trailing syntax variables or punctuation artifacts safely
                ai_response = ai_response.strip().rstrip("',").rstrip('",').strip()
                
                # ADVANCED CLEANER: Completely wipes out the raw <think> tags and everything inside them
                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()
                elif "<think>" in ai_response:
                    ai_response = ai_response.split("<think>")[0].strip()
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()

                # Render the final beautiful text and log it into tracking memory state arrays
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
