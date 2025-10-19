from PIL import Image
import os
import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

#Header
col1, col2 = st.columns([1, 4])

with col1:
    logo = Image.open("logo.png")
    st.image(logo, width=150)
    
with col2:
    st.title("ZENIA.AI")
    st.text("Asisten Curhat kamu😎")

st.divider()


#API KEY
def get_api_key_input():
    st.write("Masukkan Google API Key")

    if "GOOGLE_API_KEY" not in st.session_state:
        st.session_state["GOOGLE_API_KEY"] = ""

    col1, col2 = st.columns((80, 20))
    with col1:
        api_key = st.text_input("", label_visibility="collapsed", type="password")

    with col2:
        is_submit_pressed = st.button("Submit")
        if is_submit_pressed:
            st.session_state["GOOGLE_API_KEY"] = api_key

    os.environ["GOOGLE_API_KEY"] = st.session_state["GOOGLE_API_KEY"]


def load_llm():
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    return st.session_state["llm"]

def get_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]

def display_chat_message(message):
    if type(message) is HumanMessage:
        role = "Syko"
    elif type(message) is AIMessage:
        role = "AI"
    else:
        role = "unknown"
    with st.chat_message(role):
        st.markdown(message.content)
        
get_api_key_input()
if not os.environ["GOOGLE_API_KEY"]:
    st.stop()
    
#pilih topik
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Random"

topic = st.radio(
    "Pilih topik obrolan kamu: ",
    ["Pekerjaan", "Curhat", "Belajar", "Game", "Film", "Musik", "Random"],
    index=["Pekerjaan", "Curhat", "Belajar", "Game", "Film", "Musik", "Random"].index(st.session_state.selected_topic)
)
st.session_state.selected_topic = topic
st.info(f"Topik saat ini: {topic}")

st.divider()


llm = load_llm()
chat_history = get_chat_history()

for chat in chat_history:
    display_chat_message(chat)
    
prompt = st.chat_input("Chat with AI")
if prompt:
    chat_history.append(HumanMessage(content=prompt))
    display_chat_message(chat_history[-1])
    
    typing_msg = st.empty()
    typing_msg.markdown("ZENIA.AI Sedang Mengetik. . .")
    progress = st.progress(0)
    
    for i in range(1, 101, 10):
        time.sleep(0.15)
        progress.progress(i)
    
    if not any("Topik obrolan" in msg.content for msg in chat_history):
        topic_message = f"Topik obrolan: {st.session_state.selected_topic}. Berikan respons sesuai konteks topik ini."
        chat_history.insert(0, HumanMessage(content=topic_message))
        
    response = llm.invoke(chat_history)
    
    typing_msg.empty()
    progress.empty()

    chat_history.append(response)
    display_chat_message(chat_history[-1])
