import streamlit as st
import pandas as pd
from utils.upload_files import handle_file_upload
from utils.delete_all_files import handle_file_delete


# Define the folder for storing uploaded files
save_folder = "./Store"

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
st.sidebar.markdown("### Append URL")
