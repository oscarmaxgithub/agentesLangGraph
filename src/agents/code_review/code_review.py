from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

llm = init_chat_model("openai:gpt-4o", temperature=0)


## Definicion de las clases
class SecurityReview(BaseModel):
    vulnerabilities: list[str] = Field(
        description="The vulnerabilities in the code", default=None
    )
    riskLevel: str = Field(
        description="The risk level  in the vulnerabilities", default=None
    )
    suggestions: list[str] = Field(
        description="The suggestions for fixing the vulnerabilities", default=None
    )


class MaintainabilityReview(BaseModel):
    concerns: list[str] = Field(
        description="The converns about in the code", default=None
    )
    qualityScore: int = Field(
        description="The quality scvore of the code from 1 to 10",
        default=None,
        ge=1,
        le=10,
    )
    recommendations: list[str] = Field(
        description="The recommendations for improving the code", default=None
    )

class PerformanceMetrics(BaseModel):
    """Métricas de performance con claves fijas (OpenAI strict no admite dicts libres)."""
    execution_time_ms: float = Field(description="Execution time estimate in milliseconds")
    memory_usage_mb: float = Field(description="Estimated memory usage in MB")
    throughput_ops_per_sec: float = Field(description="Estimated operations per second")

class PerformanceReview(BaseModel):
    performance_metrics: PerformanceMetrics = Field(
        description="Key performance metrics (execution time, memory usage, throughput)"
    )
    complexity_score: int = Field(
        description="Estimated computational complexity score from 1 (low) to 10 (high)",
        default=None,
        ge=1,
        le=10,
    )
    hotspots: list[str] = Field(
        description="Code locations or functions that are performance hotspots",
        default=None,
    )
    suggestions: list[str] = Field(
        description="Concrete suggestions to improve performance (e.g., algorithmic changes, caching)",
        default=None,
    )
    estimated_runtime: str = Field(
        description="Estimated runtime characteristics or Big-O notation for critical paths",
        default=None,
    )


## Declaracion de state (estado en la memoria compartida)
class State(TypedDict):
    code: str
    security_review: SecurityReview
    maintainability_review: MaintainabilityReview
    performance_review: PerformanceReview
    final_review: str


## Definicion de nodos
def security_review(state: State):
    code = state["code"]
    messages = [
        (
            "system",
            "You are an expert in code security. Focus on identifying security vulnerabilities, injection risks, and authentication issues.",
        ),
        ("user", f"Review this code: {code}"),
    ]
    llm_with_structured_output = llm.with_structured_output(SecurityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {"security_review": schema}


def maintainability_review(state: State):
    code = state["code"]
    messages = [
        (
            "system",
            "You are an expert in code quality. Focus on code structure, readability, and adherence to best practices.",
        ),
        ("user", f"Review this code: {code}"),
    ]
    llm_with_structured_output = llm.with_structured_output(MaintainabilityReview)
    schema = llm_with_structured_output.invoke(messages)
    return {"maintainability_review": schema}


def performance_review(state: State):
    code = state["code"]
    messages = [
        (
            "system",
            "You are an expert in code performance analysis. Focus on identifying bottlenecks, algorithmic complexity, memory usage, and optimization opportunities.",
        ),
        (
            "user",
            f"Perform a detailed performance review the code, analyzing execution efficiency, resource consumption, and scalability; the code is : {code}",
        ),
    ]
    llm_with_structured_output = llm.with_structured_output(PerformanceReview)
    schema = llm_with_structured_output.invoke(messages)
    return {"performance_review": schema}


def aggregator(state: State):
    security_review = state["security_review"]
    maintainability_review = state["maintainability_review"]
    performance_review = state.get("performance_review")
    messages = [
        ("system", "You are a technical lead summarizing multiple code reviews"),
        (
            "user",
            f"Synthesize these code review results into a concise summary with key actions: Security review: {security_review} and Maintainability review: {maintainability_review} and Perform review: {performance_review}. The final answer must be in spanish.",
        ),
    ]
    response = llm.invoke(messages)
    return {"final_review": response.text}


## Creacion de Grafo

builder = StateGraph(State)

builder.add_node("security_review", security_review)
builder.add_node("maintainability_review", maintainability_review)
builder.add_node("performance_review", performance_review)
builder.add_node("aggregator", aggregator)

builder.add_edge(START, "security_review")
builder.add_edge(START, "maintainability_review")
builder.add_edge(START, "performance_review")
builder.add_edge("security_review", "aggregator")
builder.add_edge("maintainability_review", "aggregator")
builder.add_edge("performance_review", "aggregator")
builder.add_edge("aggregator", END)

agent = builder.compile()
