from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    check_missing_fields,
    conversation_router,
    extract_trip_details,
    handle_continue_trip,
    handle_general_question,
    handle_travel_information_query,
    prepare_intake_response,
)
from app.graph.state import TripGPTState
from app.schemas.conversation import ConversationIntent


def route_conversation(
    state: TripGPTState,
) -> str:

    intent = state["current_intent"]

    if intent in {
        ConversationIntent.START_TRIP,
        ConversationIntent.PROVIDE_TRIP_INFORMATION,
        ConversationIntent.UPDATE_TRIP_INFORMATION,
    }:
        return "trip_information"

    if intent == ConversationIntent.GENERAL_QUESTION:
        return "general_question"

    if intent == ConversationIntent.TRAVEL_INFORMATION_QUERY:
        return "travel_information"

    if intent == ConversationIntent.CONTINUE_TRIP:
        return "continue_trip"

    return "unknown"


builder = StateGraph(TripGPTState)


# -------------------------
# Nodes
# -------------------------

builder.add_node(
    "conversation_router",
    conversation_router,
)

builder.add_node(
    "extract_trip_details",
    extract_trip_details,
)

builder.add_node(
    "check_missing_fields",
    check_missing_fields,
)

builder.add_node(
    "prepare_intake_response",
    prepare_intake_response,
)

builder.add_node(
    "handle_general_question",
    handle_general_question,
)

builder.add_node(
    "handle_travel_information_query",
    handle_travel_information_query,
)

builder.add_node(
    "handle_continue_trip",
    handle_continue_trip,
)


# -------------------------
# Entry
# -------------------------

builder.add_edge(
    START,
    "conversation_router",
)


# -------------------------
# Intent routing
# -------------------------

builder.add_conditional_edges(
    "conversation_router",
    route_conversation,
    {
        "trip_information": "extract_trip_details",
        "general_question": "handle_general_question",
        "travel_information": (
            "handle_travel_information_query"
        ),
        "continue_trip": "handle_continue_trip",

        # temporary fallback
        "unknown": END,
    },
)


# -------------------------
# Intake flow
# -------------------------

builder.add_edge(
    "extract_trip_details",
    "check_missing_fields",
)

builder.add_edge(
    "check_missing_fields",
    "prepare_intake_response",
)

builder.add_edge(
    "prepare_intake_response",
    END,
)


# -------------------------
# Other conversation flows
# -------------------------

builder.add_edge(
    "handle_general_question",
    END,
)

builder.add_edge(
    "handle_travel_information_query",
    END,
)

builder.add_edge(
    "handle_continue_trip",
    END,
)


# -------------------------
# Short-term memory
# -------------------------

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)