from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def cyber_chain(my_docs):
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:v1.5",
    )
    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    # Split the documents into smaller chunks
    splits = text_splitter.split_documents(my_docs)
    # Create a vectorstore from the documents
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    #  Use the vectorstore as a retriever
    retriever = vectorstore.as_retriever()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are CyberHammer II, and I am your creator, Zehao Qian. You are a powerful AI model that can generate text based on the input you receive.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    model = OllamaLLM(model="qwen2.5:7b")
    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        if len(my_docs) == 0:
            chain = prompt | model
        else:
            chain = (
                {"context": retriever
                    | format_docs, "question": RunnablePassthrough()}
                | prompt
                | model
            )
        response = chain.invoke(state)
        return {"messages": response}

    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app
