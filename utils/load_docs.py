from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
import os


def read_markdown(file_path):
    return TextLoader(file_path).load()


def read_pdf(file_path):
    return PyPDFLoader(file_path).load()


def read_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.md':
        return read_markdown(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def read_url(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs
