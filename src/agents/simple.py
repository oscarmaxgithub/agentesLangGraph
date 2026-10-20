# from typing import TypedDict
import random
from langchain_core.runnables import history
from langgraph.graph import  MessagesState
from langchain_core.messages import AIMessage
from langchain_openrouter import ChatOpenRouter


model = ChatOpenRouter(
    model="openrouter/free",
    temperature=1,
)

class State(MessagesState):
    customer_name: str
    my_age: int



""" state: State = {}
customer_name = state.get("customer_name",None)
print(customer_name) """

def node_1(state: State):
    #history = state.get("messages",[])
    new_state:State={}
    if state.get("customer_name",None) is None:
        new_state
        new_state["customer_name"]="Oscar Diaz prueba"
    else:
        new_state["my_age"]=random.randint(20,30)
    
    history =state["messages"]
    ai_messages = model.invoke(history)
    new_state["messages"] = [ai_messages]
    print(new_state)
    return new_state

from langgraph.graph import END, START, StateGraph
    

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()