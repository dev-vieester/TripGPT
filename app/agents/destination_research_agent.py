from app.graph.state import TripGPTState
from app.schemas.conversation import ConversationStage
from langchain_core.messages import AIMessage

async def destination_research_agent(
        state: TripGPTState
) -> dict:

    trip_profile = state["trip_profile"]

    return {
        "current_stage": ConversationStage.DESTINATION_RESEARCH,
        "messages": [
            AIMessage(
                content=(
                    "Destination research has started. "
                    "I will use your trip profile to find "
                    "destinations that match your requirements."
                )
            )
        ],
    }