from typing import Set

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from PIL import Image
from io import BytesIO
import base64

# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:{"jpeg"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
# background_image = "bg2.jpeg"
# add_bg_from_local(background_image)


st.header("LangChain 🦜🔗 Documentation - Helper ChatBot")

# profile_image = Image.open("langchain background removed.png")

# st.sidebar.image(profile_image, width=200)


st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.image("langchain background removed.png", width = 200)

st.sidebar.markdown(
"""
    # LangChain Helper Bot 🤖

    Welcome to the LangChain Helper Bot!

    **What does it offer ?**

    🚀 Easy scraping of LangChain documentation.
    
    📚 Instead of going through tedious LangChain documentation, just submit your query here about any LangChain topic, and you'll get the answer!

    ---  

    **How to use ?**

    Just type your LangChain-related query in the input box on the main page, and the bot will fetch precise information for you.
    """
)
 

with st.sidebar:

        st.caption(
                """The official documentation of langchain can be found at  
                https://python.langchain.com/docs/get_started
                """
            )

        st.markdown("---")
        st.markdown(
            '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://www.linkedin.com/in/anujmaha/">@anujmaha</a></h6>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '📧 : anujsmahajan1998@gmail.com',
        )
        st.markdown(
            '<div style="margin-top: 0.75em;"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
            unsafe_allow_html=True,
        )

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


prompt = st.text_input("Prompt", placeholder="Enter your Langchain related query here... (eg, what is ConversationalRetrievalChain ?)")


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)
        st.session_state.chat_history.append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(
            user_query,
            is_user=True,
            avatar_style="adventurer",
            seed=123,
        )
        # message(generated_response)
        st.write(
            f'<div style="word-wrap: break-word;">{generated_response}</div>',
            unsafe_allow_html=True,
        )
