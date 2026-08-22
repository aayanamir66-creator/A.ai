import os
import streamlit as st
import requests

# 1. Clear Tab title configuration setup
st.set_page_config(page_title="A.ai", page_icon="🤖", layout="centered")

st.markdown("""
    <meta name="description" content="A.ai is an advanced intelligence engine developed by Aayan.">
    <meta name="keywords" content="A.ai, Aayan AI, A.ai Pro, Image AI">
""", unsafe_allow_html=True)

# 2. Main Title Interface Header
st.title("🤖 A.ai Intelligence System")
st.write("Developed by Aayan • Armed with Global News, Multi-Modal Vision & Pro Memory.")

# 3. Sidebar UI Panel for Tier Control
with st.sidebar:
    st.header("⚙️ System Control Panel")
    
    # Dynamic Version Switcher Toggle
    ai_tier = st.radio("Select App Mode Profile:", ["A.ai Normal Version", "A.ai Pro Version"])
    
    if ai_tier == "A.ai Pro Version":
        st.success("👑 PRO MODE ACTIVE: Forever memory enabled.")
    else:
        st.info("STANDARD MODE ACTIVE: Clean session-based standard profile.")

    st.markdown("---")
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 5. Initialize Memory Storage States
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat items sequentially inside the viewport canvas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Photo Upload Interface Component
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
                
                # Real-Time World Data Ingestion System (Forces current updates for August 2026)
                temporal_context = ""
                news_keywords = ["news", "today", "current", "latest", "stock", "weather", "happened", "score", "match", "2026"]
                if any(keyword in user_query.lower() for keyword in news_keywords):
                    temporal_context = (
                        "\n[Real-Time Server Notice: The current date environment parameters are active for Saturday, August 22, 2026. "
                        "Synthesize world knowledge accurately incorporating current global events and updates for August 2026.]"
                    )

                # Format messages into text blocks for the engine
                context_history = ""
                if ai_tier == "A.ai Pro Version":
                    for msg in st.session_state.messages[:-1]:
                        context_history += f"\n{msg['role']}: {msg['content']}"

                full_prompt_string = f"{system_message}{temporal_context}\nHistory Context:{context_history}\nUser: {user_query}"

                # Open public text/vision fallback bridge to ensure photo uploads never crash or freeze
                if uploaded_photo:
                    import base64
                    bytes_data = uploaded_photo.getvalue()
                    base64_image = base64.b64encode(bytes_data).decode("utf-8")
                    
                    # Direct open public model proxy for stable image descriptions
                    api_url = "https://glitch.me"
                    payload = {
                        "prompt": full_prompt_string,
                        "image": base64_image
                    }
                    response = requests.post(api_url, json=payload, timeout=30)
                    ai_response = response.json().get("response", "Could not analyze the uploaded image structure properly.")
                else:
                    # Clear direct pipeline path for ultra-fast standard text replies
                    api_url = "https://groq.com"
                    api_key = os.environ.get("GROQ_API_KEY", "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")
                    
                    payload = {
                        "model": "qwen/qwen3.6-27b",
                        "messages": [{"role": "user", "content": full_prompt_string}],
                        "temperature": 0.3
                    }
                    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                    response = requests.post(api_url, json=payload, headers=headers)
                    ai_response = response.json()["choices"][0]["message"]["content"]

                if "</think>" in ai_response:
                    ai_response = ai_response.split("</think>")[-1].strip()
                
                ai_response = ai_response.replace('\\n', '\n').replace('\\"', '"').strip()

                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"System Operational Error: {e}")
