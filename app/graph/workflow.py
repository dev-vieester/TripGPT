from typing import Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    check_missing_fields,
    conversation_router,
    extract_trip_details,
    handle_continue_trip,
    handle_general_question,
    handle_travel_information_query,
    prepare_intake_response, handle_trip_update_request,
)
from app.graph.state import TripGPTState
from app.schemas.conversation import ConversationIntent, ConversationStage
from app.agents.destination_research_agent import (
    destination_research_agent,
)


def route_conversation(
    state: TripGPTState,
) -> Literal[
    "trip_information",
    "request_trip_update",
    "general_question",
    "travel_information",
    "continue_trip",
]:

    intent = state["current_intent"]

    if intent in {
        ConversationIntent.START_TRIP,
        ConversationIntent.PROVIDE_TRIP_INFORMATION,
        ConversationIntent.UPDATE_TRIP_INFORMATION,
    }:
        return "trip_information"

    elif (
            intent
            == ConversationIntent.REQUEST_TRIP_INFORMATION_UPDATE
    ):
        return "request_trip_update"

    elif intent == ConversationIntent.GENERAL_QUESTION:
        return "general_question"

    elif intent == ConversationIntent.TRAVEL_INFORMATION_QUERY:
        return "travel_information"

    else:
        return "continue_trip"

def route_continue_trip(
        state: TripGPTState,
)-> Literal[
    "destination_research",
    # "destination_selection",
    # "trip_planning",
    "unknown",
]:
    stage = state["current_stage"]
    if stage == ConversationStage.READY_FOR_RESEARCH:
        return "destination_research"

    # elif stage == ConversationStage.DESTINATION_SELECTION:
    #     return "destination_selection"
    #
    # elif stage == ConversationStage.TRIP_PLANNING:
    #     return "trip_planning"

    return "unknown"

builder = StateGraph(TripGPTState)


# Nodes
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

builder.add_node(
    "destination_research_agent",
    destination_research_agent
)

builder.add_node(
    "handle_trip_update_request",
    handle_trip_update_request,
)

# Start
builder.add_edge(
    START,
    "conversation_router",
)


# Conversation routing
builder.add_conditional_edges(
    "conversation_router",
    route_conversation,
    {
        "trip_information": "extract_trip_details",
        "request_trip_update": "handle_trip_update_request",
        "general_question": "handle_general_question",
        "travel_information": "handle_travel_information_query",
        "continue_trip": "handle_continue_trip",
    },
)


# Trip information flow
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


# General question flow
builder.add_edge(
    "handle_general_question",
    END,
)


# Travel information flow
builder.add_edge(
    "handle_travel_information_query",
    END,
)

builder.add_edge(
"handle_trip_update_request",
    END
)


# Continue trip flow
builder.add_conditional_edges(
    "handle_continue_trip",
    route_continue_trip, {
        "destination_research": "destination_research_agent",
        "unknown": END,
    }
)

builder.add_edge(
"destination_research_agent",
    END,
)


# Short-term memory
checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)