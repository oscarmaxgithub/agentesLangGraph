from typing import Literal

from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

from src.agents.support.routes.intent_evalutator.prompt import (
    SYSTEM_PROMPT_INTENT_EVALUATOR,
)
from src.agents.support.state import State


class RouteIntent(BaseModel):
    """
    Contact information for a person.
    """

    step: Literal["conversation", "booking"] = Field(
        'conversation', description="The next step in the routing process"
    )


llm = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
)
llm_extractor = llm.with_structured_output(schema=RouteIntent)


def intent_evaluator(state: State) -> Literal["conversation", "booking"]:
    history = state["messages"]
    schema = llm_extractor.invoke(
        [("system", SYSTEM_PROMPT_INTENT_EVALUATOR)] + history
    )
    if schema.step is None:
        return 'conversation'
    return schema.step
