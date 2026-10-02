from langgraph.graph import StateGraph, START, END

from app.graph.destination.state import (
    CountryResearchState,
)

from app.graph.destination.nodes import (
    visa_agent,
    visa_processing_agent,
    budget_agent,
    safety_agent,
    health_agent,
    outbreak_agent,
    weather_agent,
    language_agent,
    attractions_agent,
    build_country_dossier,
)


SPECIALIST_NODES = [
    "visa",
    "visa_processing",
    "budget",
    "safety",
    "health",
    "outbreak",
    "weather",
    "language",
    "attractions",
]


def build_country_research_graph():

    builder = StateGraph(CountryResearchState)

    builder.add_node("visa", visa_agent)

    builder.add_node(
        "visa_processing",
        visa_processing_agent,
    )

    builder.add_node("budget", budget_agent)
    builder.add_node("safety", safety_agent)
    builder.add_node("health", health_agent)
    builder.add_node("outbreak", outbreak_agent)
    builder.add_node("weather", weather_agent)
    builder.add_node("language", language_agent)

    builder.add_node(
        "attractions",
        attractions_agent,
    )

    builder.add_node(
        "build_dossier",
        build_country_dossier,
    )

    # Fan-out
    for node in SPECIALIST_NODES:
        builder.add_edge(START, node)

    # Fan-in
    builder.add_edge(
        SPECIALIST_NODES,
        "build_dossier",
    )

    builder.add_edge(
        "build_dossier",
        END,
    )

    return builder.compile()


country_research_graph = (
    build_country_research_graph()
)