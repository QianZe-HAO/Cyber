from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


def cyber_retriever(docs):
    # nomic embeddings model for text retrieval and similarity
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:v1.5",
    )
    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    # Split the documents into smaller chunks
    splits = text_splitter.split_documents(docs)
    # Create a vectorstore from the documents
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    #  Use the vectorstore as a retriever
    retriever = vectorstore.as_retriever()
    return retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)