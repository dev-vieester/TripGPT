from app.schemas.trip import REQUIRED_TRIP_FIELDS
from langgraph.types import interrupt
from app.agents.intake_agent import extract_trip_information
from app.schemas.intake import TripInformationExtraction
from app.schemas.trip import TripProfile

from langchain_core.messages import HumanMessage, AIMessage
from app.agents.conversation_router_agent import (
    classify_conversation_intent
)
from app.graph.state import TripGPTState
from app.schemas.conversation import ConversationIntent, ConversationStage


async def conversation_router(
        state: TripGPTState
) -> dict:
    messages = state["messages"]

    latest_message = messages[-1]
    if not isinstance(latest_message, HumanMessage):
        return {}

    result = await classify_conversation_intent(
        message=latest_message.content,
        current_stage=state["current_stage"],
        pending_fields=state.get("pending_fields"),
        trip_profile=state.get("trip_profile")
    )

    return {
        "current_intent": result.intent
    }



def merge_trip_profile(
        current: TripProfile,
        extraction: TripInformationExtraction
) -> TripProfile:
    current_Data = current.model_dump()
    extracted_data = extraction.model_dump()

    for field, value in extracted_data.items():
        if value is None:
            continue

        current_Data[field] = value
    return TripProfile(**current_Data)

async def extract_trip_details(
        state: TripGPTState
)-> dict:
    messages = state["messages"]
    latest_message = messages[-1]

    if not isinstance(latest_message, HumanMessage):
        return {}

    extraction = await extract_trip_information(
        latest_message.content
    )

    return {
        "trip_profile": merge_trip_profile(state['trip_profile'], extraction)
    }

async def check_missing_fields(
        state: TripGPTState
) -> dict:
    trip_profile = state["trip_profile"]

    missing_fields = []

    for field in REQUIRED_TRIP_FIELDS:
        value = getattr(trip_profile, field)

        if value is None or value == "":
            missing_fields.append(field)

    return {
        "missing_required_fields": missing_fields,
        "intake_complete": len(missing_fields) == 0
    }
#
# async def request_missing_information(
#         state: TripGPTState
# )-> dict:
#     missing = state["missing_required_fields"]
#
#     user_response = interrupt(
#         {
#             "type": "missing_trip_information",
#             "missing_fields": missing,
#             "message": build_missing_fields_message(missing)
#         }
#     )
#
#     return {
#         "messages": [
#             HumanMessage(content=user_response)
#         ]
#     }

async def prepare_intake_response(
        state: TripGPTState
) -> dict:

    missing = state["missing_required_fields"]

    if not missing:
        return {
            "pending_fields": [],
            "intake_complete": True,
            "current_stage": (
                ConversationStage.DESTINATION_RESEARCH
            ),
            "messages": [
                AIMessage(
                    content=(
                        "Great, I have the information "
                        "I need to start evaluating "
                        "destinations."
                    )
                )
            ],
        }
    pending = missing[:2]

    message = build_missing_fields_message(pending)

    return {
        "current_stage": ConversationStage.INTAKE,
        "pending_fields": pending,
        "messages": [
            AIMessage(content=message)
        ],
    }

async def handle_general_question(
    state: TripGPTState,
) -> dict:

    return {
        "messages": [
            AIMessage(
                content=(
                    "General question handling "
                    "is not implemented yet."
                )
            )
        ]
    }


async def handle_travel_information_query(
    state: TripGPTState,
) -> dict:

    return {
        "messages": [
            AIMessage(
                content=(
                    "Travel information research "
                    "is not implemented yet."
                )
            )
        ]
    }


async def handle_continue_trip(
    state: TripGPTState,
) -> dict:

    return {
        "messages": [
            AIMessage(
                content=(
                    "Continue-trip handling "
                    "is not implemented yet."
                )
            )
        ]
    }


def build_missing_fields_message(
        missing_fields: list[str]
) -> str:
    field_questions = {
        "origin_country":
            "Which country will you be travelling from?",

        "nationality":
            "What passport/nationality will you be travelling with?",

        "budget":
            "What is your approximate travel budget?",

        "budget_currency":
            "What currency is your budget in?",

        "departure_date":
            "When are you planning to travel?",

        "trip_duration_days":
            "How many days do you have available for the trip?",

        "interests":
            "What activities or travel interests do you have, if any?",

        "preferred_languages":
            "Do you have any preferred languages for the trip?",

        "health_requirements":
            "Do you have any health requirements or conditions to consider?",

        "accessibility_requirements":
            "Do you have any accessibility requirements?",
    }

    questions = [
        field_questions[field]
        for field in missing_fields
        if field in field_questions
    ]

    return "\n".join(questions)
