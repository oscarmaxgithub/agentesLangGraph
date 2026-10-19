# from typing import TypedDict
from langgraph.graph import  MessagesState
from langchain_core.messages import AIMessage

class State(MessagesState):
    customer_name: str
    my_age: int



""" state: State = {}
customer_name = state.get("customer_name",None)
print(customer_name) """

def node_1(state: State):
    history = state.get("messages",[])
    if state.get("customer_name",None) is None:
        return {"customer_name" : "John Doe"}
    else:
        ai_message = AIMessage(content="Hola, como estas?")
        return {
            "messages" : [ai_message]
        }

from langgraph.graph import END, START, StateGraph
    

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()