import os
import streamlit as st
from groq import Groq

# 1. Clear Tab title configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖")

st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Advanced Core Active with Continuous Session Memory.")

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
        with st.spinner("A.ai is generating comprehensive analysis..."):
            try:
                # Upgraded persona template prompt forcing advanced, deep, and highly intelligent reasoning
                system_message = (
                    "Your name is A.ai. You are an all-knowing, highly intellectual, comprehensive AI assistant. "
                    "You were created and developed by Aayan. If asked who made you, reply proudly that Aayan made you. "
                    "Provide highly advanced, deeply analytical, and professional responses. "
                    "Do not give brief answers; provide rich context, background details, and structural breakdowns for every query."
                )
                
                # Dynamic Real-Time World Data Ingestion Parameter (August 2026 calibration)
                temporal_context = (
                    "\n[Real-Time Server Notice: The current calendar date environment parameters are active for Saturday, August 22, 2026. "
                    "Synthesize your deep world knowledge accurately incorporating current global events and structural world updates for August 2026.]"
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
                    ai_response = ai_response.split(", role='assistant'")[0]
                if "', role=" in ai_response:
                    ai_response = ai_response.split("', role=")[0]
                if '", role=' in ai_response:
                    ai_response = ai_response.split('", role=')[0]
                if "content='" in ai_response:
                    ai_response = ai_response.split("content='")[-1]
                if 'content="' in ai_response:
                    ai_response = ai_response.split('content="')[-1]
                if "[Choice(finish_reason=" in ai_response:
                    ai_response = ai_response.split("[Choice(finish_reason=")[0]

                # Strip trailing syntax variables or punctuation artifacts safely
                ai_response = ai_response.strip().rstrip("',").rstrip('",').strip()
                
                # Clean up reasoning token blockages if present
                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()

                # Render the final beautiful text and log it into tracking memory state arrays
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
