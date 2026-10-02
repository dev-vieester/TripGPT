from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import ValidationError
from app.core.config import settings
from app.prompts import CONVERSATION_SYSTEM_PROMPT

from app.core.exceptions import (
    LLMProviderError,
    LLMStructuredOutputError,
)

from app.schemas.conversation import (
    ConversationRoute,
    ConversationStage
)
from app.schemas.trip import TripProfile

llm = ChatGoogleGenerativeAI(
    model=settings.google_model,
    temperature=0,
    api_key=settings.google_api_key,
    max_tokens=None,
    timeout=30,
    max_retries=2,
)

structured_router = llm.with_structured_output(ConversationRoute)

async def classify_conversation_intent(
        message: str,
        current_stage: ConversationStage = ConversationStage.NEW,
        pending_fields: list[str] | None  = None,
        trip_profile: TripProfile | None = None,
        profile_update_field: str | None = None
) -> ConversationRoute:
    pending_context = (
        pending_fields if pending_fields else "None"
    )

    profile_context = (
        trip_profile.model_dump(mode="json")
        if trip_profile
        else "None"
    )

    update_context = (
        profile_update_field
        if profile_update_field
        else "None"
    )

    context = f"""
    CURRENT CONVERSATION CONTEXT

    Current stage:
    {current_stage.value}
    
    Pending fields:
    {pending_context}
    
    Current trip profile:
    {profile_context}
    
    Profile field currently being updated:
    {update_context}
    
    Latest user message:
    {message}

    """
    try:
        result = await structured_router.ainvoke(
            [
                ("system", CONVERSATION_SYSTEM_PROMPT),
                ("human", context),
            ]
        )

        return result

    except ValidationError as exc:
        raise LLMStructuredOutputError(
            "The conversation router returned "
            "an invalid structured response."
        ) from exc

    except (
            TimeoutError,
            ConnectionError,
    ) as exc:
        raise LLMProviderError(
            "The LLM provider could not be reached "
            "while routing the conversation."
        ) from exc

    except Exception as exc:
        raise LLMProviderError(
            "The conversation router failed."
        ) from exc