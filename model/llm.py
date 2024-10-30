from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def cyber_chain():
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

        chain = prompt | model
        response = chain.invoke(state)
        return {"messages": response}

    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app
