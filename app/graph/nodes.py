from app.agents.profile_update_agent import identify_profile_update_field
from app.schemas.trip import LIST_TRIP_FIELDS, REQUIRED_TRIP_FIELDS
from app.agents.intake_agent import extract_trip_information
from app.schemas.intake import TripInformationExtraction
from app.schemas.trip import TripProfile

from langchain_core.messages import HumanMessage, AIMessage
from app.agents.conversation_router_agent import (
    classify_conversation_intent
)
from app.graph.state import TripGPTState
from app.schemas.conversation import ConversationStage, ConversationIntent


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
        trip_profile=state.get("trip_profile"),
        profile_update_field = state.get(
            "profile_update_field"
        ),
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
) -> dict:

    messages = state["messages"]
    latest_message = messages[-1]

    if not isinstance(latest_message, HumanMessage):
        return {}

    extraction = await extract_trip_information(
        latest_message.content
    )

    updates = {
        "trip_profile": merge_trip_profile(
            state["trip_profile"],
            extraction,
        )
    }

    if (
        state["current_intent"]
        == ConversationIntent.UPDATE_TRIP_INFORMATION
    ):
        updates["profile_update_field"] = None

    return updates

async def check_missing_fields(
        state: TripGPTState
) -> dict:
    trip_profile = state["trip_profile"]

    missing_fields = []

    for field in REQUIRED_TRIP_FIELDS:
        value = getattr(trip_profile, field)

        if value is None:
            missing_fields.append(field)
            continue

        if field not in LIST_TRIP_FIELDS and isinstance(value, str) and value.strip() == "":
            missing_fields.append(field)

    return {
        "missing_required_fields": missing_fields,
        "intake_complete": len(missing_fields) == 0
    }

async def prepare_intake_response(
        state: TripGPTState
) -> dict:

    missing = state["missing_required_fields"]

    if not missing:
        return {
            "pending_fields": [],
            "intake_complete": True,
            "current_stage": (
                ConversationStage.READY_FOR_RESEARCH
            ),
            "messages": [
                AIMessage(
                    content=(
                        "(Great, your trip profile is complete. Would you like me to "
                        "start researching destinations that match your requirements?)"
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

async def handle_trip_update_request(
    state: TripGPTState,
) -> dict:

    messages = state["messages"]
    latest_message = messages[-1]

    if not isinstance(latest_message, HumanMessage):
        return {}

    result = await identify_profile_update_field(
        latest_message.content
    )

    field = result.field

    if field is None:
        return {
            "profile_update_field": None,
            "messages": [
                AIMessage(
                    content=(
                        "Of course. What would you like "
                        "to change in your trip profile?"
                    )
                )
            ],
        }

    field_questions = {
        "origin_country":
            "Which country will you now be travelling from?",

        "nationality":
            "What passport or nationality would you like to use?",

        "budget":
            "What would you like your new travel budget to be?",

        "budget_currency":
            "What currency would you like to use for your budget?",

        "departure_date":
            "What would you like your new departure date to be?",

        "trip_duration_days":
            "How many days would you now like the trip to be?",

        "interests":
            "What travel interests would you like to use instead?",

        "preferred_languages":
            "What language preferences would you like to use?",

        "health_requirements":
            "What health requirements should I consider instead?",

        "accessibility_requirements":
            "What accessibility requirements should I consider instead?",
    }

    return {
        "profile_update_field": field,
        "messages": [
            AIMessage(
                content=field_questions[field]
            )
        ],
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


