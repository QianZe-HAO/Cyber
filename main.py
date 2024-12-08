from langchain_core.messages import HumanMessage
import streamlit as st
import pandas as pd
# dealing with file uploads and deletions
from utils.upload_files import handle_file_upload
from utils.delete_all_files import handle_file_delete
# dealing with URLs
from utils.process_urls import handle_url
import os
from utils.load_docs import read_file
from utils.load_docs import read_url


from model.llm import cyber_chain


from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Define the folder for storing uploaded files
save_folder = "./store"

# ----------------- Main Streamlit App ---------------------
st.set_page_config(page_title="Cyber II",
                   page_icon="./static/icon/cyberhammer.webp", layout="wide")
st.header("Cyber II")


# Sidebar title
st.sidebar.title("Cyber II")
st.sidebar.markdown(
    "Welcome to Cyber II, the latest Cyber Hammer RAG application.")
st.sidebar.markdown("""
Instructions: Upload Files or URLs $\\rightarrow$ Select Embedding Model $\\rightarrow$ Run Doc Embeddings $\\rightarrow$ Select LLM $\\rightarrow$ Run QA
""")


# ------------ File Upload and Delete Section --------------
st.sidebar.divider()
st.sidebar.markdown("### File Upload and Delete")
# Call the file upload handler function and get the list of uploaded files
uploaded_files_list = handle_file_upload(save_folder)
# Call the file delete handler function and remove all of uploaded files
uploaded_files_list = handle_file_delete(save_folder)

# Display the file list as a table in the sidebar
if uploaded_files_list:
    file_df = pd.DataFrame(uploaded_files_list, columns=["Uploaded Files"])
    st.sidebar.dataframe(file_df, width=600, hide_index=True)
else:
    st.sidebar.warning("No files uploaded yet.")
st.sidebar.divider()


# ------------- Url Upload Section -------------------------
url_list = handle_url()
st.sidebar.divider()

# -------------- Embedding Model Section -------------------
if "file_docs" not in st.session_state:
    st.session_state["file_docs"] = []

if "url_docs" not in st.session_state:
    st.session_state["url_docs"] = []

if "docs" not in st.session_state:
    st.session_state["docs"] = []

st.sidebar.markdown("### Select Model and Run Embeddings")
if len(uploaded_files_list) == 0 and len(url_list) == 0:
    st.sidebar.warning("No files or URLs need to be processed.")
else:
    if st.sidebar.button("Run Embeddings"):
        for file in uploaded_files_list:
            file_path = save_folder + "/" + file
            file_content = read_file(file_path)

            st.session_state['file_docs'] += file_content
        # print(st.session_state['file_docs'])
        for url in url_list:
            # print(url)
            url_content = read_url(url)
            st.session_state['url_docs'] += url_content

        st.session_state["docs"] = st.session_state['file_docs'] + \
            st.session_state['url_docs']

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
        )
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100, chunk_overlap=20)
        splits = text_splitter.split_documents(st.session_state["docs"])
        print(splits)
        # vectorstore = Chroma.from_documents(
        #     documents=splits, embedding=embeddings)
        # retriever = vectorstore.as_retriever()


# --------------------- Main Section -----------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state['messages']:
    st.chat_message(msg["role"]).write(msg["content"])

if "config" not in st.session_state:
    st.session_state["config"] = {"configurable": {"thread_id": "abc123"}}

if prompt := st.chat_input():
    config = st.session_state["config"]
    st.session_state["messages"].append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)
    # response = chain.invoke({"question": prompt})
    input_messages = [HumanMessage(prompt)]

    if "chain" not in st.session_state:
        st.session_state["chain"] = cyber_chain(st.session_state["docs"])

    print(st.session_state["chain"])

    res = st.session_state["chain"].invoke(
        {"messages": input_messages}, config)
    response = res["messages"][-1].content
    st.session_state["messages"].append(
        {"role": "assistant", "content": response}
    )
    st.chat_message("assistant").write(response)
