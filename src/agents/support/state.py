
from typing import NotRequired
from langgraph.graph import MessagesState


class State(MessagesState):
    customer_name: NotRequired[str]
    phone: NotRequired[str]
    my_age: NotRequired[str]