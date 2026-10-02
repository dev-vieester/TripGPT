from enum import Enum
from pydantic import BaseModel, Field

class ConversationStage(str, Enum):
    NEW = "new"
    INTAKE = "intake"
    READY_FOR_RESEARCH = "ready_for_research"
    DESTINATION_RESEARCH = "destination_research"
    DESTINATION_SELECTION = "destination_selection"
    TRIP_PLANNING = "trip_planning"

class ConversationIntent(str, Enum):
    START_TRIP = "start_trip"
    PROVIDE_TRIP_INFORMATION = "provide_trip_information"
    UPDATE_TRIP_INFORMATION = "update_trip_information"
    REQUEST_TRIP_INFORMATION_UPDATE = (
        "request_trip_information_update"
    )
    GENERAL_QUESTION = "general_question"
    TRAVEL_INFORMATION_QUERY = "travel_information_query"
    CONTINUE_TRIP = "continue_trip"

class ConversationRoute(BaseModel):
    intent: ConversationIntent = Field(
        description=(
            "The intent of the user's latest message "
            "within the current TripGPT conversation."
        )
    )

    reasoning: str = Field(
        description=(
            "A short explanation of why this intent "
            "was selected."
    )
    )