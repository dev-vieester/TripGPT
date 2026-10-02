from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from app.schemas.trip import TripProfile
from app.schemas.conversation import (
    ConversationIntent,
    ConversationStage
)

class TripGPTState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

    thread_id: str

    current_stage: ConversationStage
    current_intent: ConversationIntent | None

    trip_profile: TripProfile
    profile_update_field: str | None
    missing_required_fields: list[str]
    pending_fields: list[str]
    intake_complete: bool
    candidate_destinations: list[dict]
    destination_assessments: list[dict]
    selected_destination: str | None

    errors: List[str]