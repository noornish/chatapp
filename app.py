import openai
import streamlit as st

st.title("Code Explanation Chatbot")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot_expanded" not in st.session_state:
    st.session_state["chatbot_expanded"] = False

# Button to toggle chatbot visibility
if st.button("🤖💻 Code Explanation Chatbot"):
    st.session_state["chatbot_expanded"] = not st.session_state["chatbot_expanded"]

# Display chatbot content when expanded
if st.session_state["chatbot_expanded"]:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What code do you want to understand?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        code_keywords = ["code", "programming", "explain", "understand"]
        if any(keyword in prompt.lower() for keyword in code_keywords):
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            with st.chat_message("assistant"):
                st.markdown("I'm sorry, I can only provide explanations for programming code.")