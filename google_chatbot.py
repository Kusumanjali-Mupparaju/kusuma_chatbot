import streamlit as st
from google import genai

# ============================================================
# GOOGLE AI STUDIO API KEY
# ============================================================

API_KEY = "AQ.Ab8RN6L0u2wUSTMvVvBoh1tQXusnCXNoGtxwS0PJVwP516nxkg"

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kusuma AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #fdf2f8,
        #ecfeff
    );
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #5b21b6;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🤖 Kusuma AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with Google Gemini</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input("💬 Type your message here...")


# ============================================================
# SEND MESSAGE
# ============================================================

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate Gemini response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Gemini is thinking..."):

            try:

                # Build conversation history
                conversation = ""

                for message in st.session_state.messages:

                    if message["role"] == "user":

                        conversation += (
                            "User: "
                            + message["content"]
                            + "\n"
                        )

                    elif message["role"] == "assistant":

                        conversation += (
                            "Assistant: "
                            + message["content"]
                            + "\n"
                        )

                # Send request to Gemini
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation
                )

                # Get Gemini response
                assistant_response = response.text

                # Display response
                st.markdown(assistant_response)

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

            except Exception as e:

                st.error(
                    "❌ Error occurred:\n\n"
                    + str(e)
                )


# ============================================================
# CLEAR CHAT
# ============================================================

if st.session_state.messages:

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()