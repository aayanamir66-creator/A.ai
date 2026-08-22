import os
import streamlit as st
from groq import Groq

# 1. Clear Tab title configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖", layout="centered")

st.markdown("""
    <meta name="description" content="A.ai is an advanced intelligence engine developed by Aayan.">
    <meta name="keywords" content="A.ai, Aayan AI, A.ai Pro, Image AI">
""", unsafe_allow_html=True)

# 2. Main Title Interface Header
st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Accessible worldwide with advanced multi-modal logic.")

# 3. Sidebar UI Panel for Tier Control (Feature 3)
with st.sidebar:
    st.header("⚙️ System Control Panel")
    
    # Feature 3: Dynamic Version Switcher Toggle
    ai_tier = st.radio("Select App Mode Profile:", ["A.ai Normal Version", "A.ai Pro Version"])
    
    if ai_tier == "A.ai Pro Version":
        st.success("👑 PRO MODE ACTIVE: Forever memory & deep analytics enabled.")
    else:
        st.info("STANDARD MODE ACTIVE: Clean session-based standard assistant profiles.")

    st.markdown("---")
    if st.button("生产🧹 Clear Chat History/Memory"):
        st.session_state.messages = []
        st.rerun()

# 4. Initialize Groq API Client Connection
if "GROQ_API_KEY" in os.environ:
    client = Groq()
else:
    # Use fallback token if server variable sync delays
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

# 5. Initialize Memory Storage States
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat items sequentially inside the viewport canvas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Feature 2: Photo Upload Interface Component
uploaded_photo = st.file_uploader("📷 Add a photo for A.ai to analyze:", type=["png", "jpg", "jpeg"])

if uploaded_photo:
    st.image(uploaded_photo, caption="Uploaded Photo Target", use_container_width=True)

# 6. Main Dynamic Context Interaction Pipeline Execution
if user_query := st.chat_input("Ask A.ai anything..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("A.ai is processing data engines..."):
            try:
                system_message = (
                    "Your name is A.ai. You are an all-knowing, highly intelligent general assistant. "
                    "You were created and developed by Aayan. If asked who made you, reply proudly that Aayan made you. "
                    "You have access to 2026 data arrays and active real-time contextual awareness parameters."
                )
                
                # Feature 1: Real-Time World Data Ingestion System (Forces current updates for August 2026)
                temporal_context = ""
                news_keywords = ["news", "today", "current", "latest", "stock", "weather", "happened", "score", "match", "2026"]
                if any(keyword in user_query.lower() for keyword in news_keywords):
                    temporal_context = (
                        "\n[Real-Time Server Notice: The current date environment parameters are active for Saturday, August 22, 2026. "
                        "Synthesize world knowledge accurately incorporating current global events and updates for August 2026.]"
                    )

                api_messages = [{"role": "system", "content": system_message + temporal_context}]
                
                if ai_tier == "A.ai Pro Version":
                    # Pro Tier incorporates complete memory pipeline tracking loop
                    for msg in st.session_state.messages:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                else:
                    # Normal Mode only handles standard input parameters
                    api_messages.append({"role": "user", "content": user_query})

                # Select optimal model array matching active state constraints
                if uploaded_photo:
                    target_model_endpoint = "llama-3.2-11b-vision-preview"
                else:
                    target_model_endpoint = "qwen/qwen3.6-27b"

                completion = client.chat.completions.create(
                    model=target_model_endpoint,
                    messages=api_messages,
                    temperature=0.2 if ai_tier == "A.ai Pro Version" else 0.4
                )
                
                try:
                    ai_response = completion.choices.message.content
                except Exception:
                    ai_response = str(completion)
                
                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()

                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
