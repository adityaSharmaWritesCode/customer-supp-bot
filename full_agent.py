#Using just rough boiler plate code

from typing import Literal, TypedDict, Annotated, Sequence

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


llm = ChatOllama(
    model="qwen3",
    temperature=1
)

builder = StateGraph(State)

def user_info(state: State):
    return {"user_info": "Passenger ID : 256"}

def book_hotel(state: State):


# builder.add_node("fetch_user_info", user_info)
# builder.add_edge(START, "fetch_user_info")


# ## HOTEL ASSISTANT

# builder.add_node("hotel_primary", lambda state:state)
# builder.add_node("book hotel", books a hotel)