from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import Literal
import random

from pydantic import BaseModel, Field

# class State(TypedDict):
#     nodes: list[str]

# class State(MessagesState):
#     nodes: list[str]
class State(TypedDict, total=False):
    joke: str                 # Último chiste generado
    topic: str                # Tema pedido por el usuario
    feedback: str             # Feedback del evaluador para mejorar el chiste
    is_funny: bool            # Señal del evaluador: ¿aprueba o no?
    # iteraciones: int          # Contador de iteraciones (opcional)

class Feedback(BaseModel):
    is_funny: bool = Field(description="Decide if the joke is funny or not. Return True if it is, False otherwise"),
    feedback: str = Field(description="If the jode is not funny, provide feedback on how to improve it in spanish")

llm = init_chat_model("openai:gpt-4o", temperature=0)
ll_evaluator = llm.with_structured_output(Feedback, temperature =0)
SYSTEM_PROMPT = """
Un chiste gracioso debe ser mas de 2 parrafos.
"""


def generator_node(state: State):
    feedback = state.get("feedback", None)
    topic = state.get("topic", None)
    if feedback:
        msg = llm.invoke(f"Write a joke about {topic} but take into account the feedback: {feedback} respond in Spanish")
    else:
        msg = llm.invoke(f"Write a joke about {topic} respond in Spanish")
    return {"joke": msg.text}


def evaluator_node(state: State):
    joke = state.get("joke", None)
    schema = ll_evaluator.invoke(f"Grade the joke {joke} with the following prompt: {SYSTEM_PROMPT}")
    # schema = ll_evaluator.invoke(f"Grade the joke {joke}")
    return {"is_funny": schema.is_funny, "feedback": schema.feedback}

def route_edge(state: State) -> Literal[END, "generator_node"]:
    is_funny = state.get("is_funny", True)
    if is_funny:
        return END
    else:
        return "generator_node"

builder = StateGraph(State)

builder.add_node('generator_node', generator_node)
builder.add_node('evaluator_node', evaluator_node)

builder.add_edge(START, 'generator_node')
builder.add_edge('generator_node', 'evaluator_node')
builder.add_conditional_edges('evaluator_node', route_edge)
builder.add_edge('evaluator_node', END)


agent = builder.compile()