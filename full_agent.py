# #Using just rough boiler plate code

# from typing import Literal, TypedDict, Annotated, Sequence

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import StateGraph, START, END
# from langgraph.prebuilt import tools_condition, ToolNode
# from langchain_ollama import ChatOllama, OllamaEmbeddings
# from langgraph.graph.message import AnyMessage, add_messages


# class State(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]


# llm = ChatOllama(
#     model="qwen3",
#     temperature=1
# )

# builder = StateGraph(State)

# def user_info(state: State):
#     return {"user_info": "Passenger ID : 256"}

# def book_hotel(state: State):
#     return "The hotel has been booked ahaha"

# builder.add_node("fetch_user_info", user_info)
# builder.add_edge(START, "fetch_user_info")


# ## HOTEL ASSISTANT

# builder.add_node("hotel_primary", lambda state:state)
# builder.add_node("book hotel", books_a_hotel)

# hotel_safe_tools = [search_user_info, search_hotel]
# hotel_sensitive_tools = [book_hotel, cancel_hotel, update_hotel]

# builder.add_node("hotel_safe_tools", ToolNode(tools=hotel_safe_tools))
# builder.add_node("hotel_sensitive_tools", ToolNode(tools=hotel_sensitive_tools))

# builder.add_edge


## CAR RENTAL ASSISTANT



## EXCURSION ASSISTANT


## FLIGHTS ASSSITANT


from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain.agents import Tool, initialize_agent, AgentType

# 🛠️ Step 1: Define simple print tools

@tool
def check_order_status(order_id: str):
    """Tool to check the order status by order ID."""
    print(f"[Tool] Checking order status for order ID: {order_id}")
    return f"Order {order_id} is currently being processed."

@tool
def initiate_refund(order_id: str):
    """Tool to initiate a refund for a given order."""
    print(f"[Tool] Initiating refund for order ID: {order_id}")
    return f"Refund for order {order_id} has been initiated."

@tool
def escalate_to_human(issue: str):
    """Tool to escalate issue to human support."""
    print(f"[Tool] Escalating issue to human: {issue}")
    return "The issue has been escalated to human support."

# 🧠 Step 2: Define tools list

tools = [
    Tool.from_function(check_order_status),
    Tool.from_function(initiate_refund),
    Tool.from_function(escalate_to_human)
]

# 🤖 Step 3: Define the LLM agent using ChatOllama

llm = ChatOllama(model="qwen3", temperature=0.3)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🌐 Step 4: Define the LangGraph state and workflow logic

class AgentState(dict):
    """Simple state wrapper, you can customize it further."""
    pass

def agent_node(state: AgentState):
    print(f"[Agent Node] Current state: {state}")
    input_text = state.get("input")
    result = agent.invoke({"input": input_text})
    return {"result": result, "input": input_text}

# ✅ Step 5: Create the LangGraph workflow

def build_workflow() -> Runnable:
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", RunnableLambda(agent_node))
    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")
    return workflow.compile()

# 🚀 Step 6: Run the workflow

if __name__ == "__main__":
    workflow = build_workflow()
    output = workflow.invoke({"input": "Please check the status of order #12345"})
    print("[Final Output]", output)