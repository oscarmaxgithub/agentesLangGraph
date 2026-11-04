from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from src.agents.support.nodes.booking.node import booking_node
from src.agents.support.nodes.conversation.node import conversation
from src.agents.support.nodes.extractor.node import extractor
from src.agents.support.routes.intent_evalutator.route import intent_evaluator
from src.agents.support.state import State


def make_graph(config: TypedDict):

    checkpointer = config.get("checkpointer", None)

    builder = StateGraph(State)
    builder.add_node("conversation", conversation)
    builder.add_node("extractor", extractor)
    builder.add_node("booking", booking_node)

    builder.add_edge(START, "extractor")
    builder.add_conditional_edges("extractor", intent_evaluator)
    builder.add_edge("booking", END)
    builder.add_edge("conversation", END)

    return builder.compile(checkpointer=checkpointer)
