from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas.profile_update import ProfileUpdateRequest
from app.core.config import settings
from app.prompts import PROFILE_UPDATE_SYSTEM_PROMPT

llm = ChatGoogleGenerativeAI(
    model=settings.google_model,
    temperature=0,
    api_key=settings.google_api_key,
)

structured_llm = llm.with_structured_output(
    ProfileUpdateRequest
)

async def identify_profile_update_field(
    message: str,
) -> ProfileUpdateRequest:

    return await structured_llm.ainvoke(
        [
            ("system", PROFILE_UPDATE_SYSTEM_PROMPT),
            ("human", message),
        ]
    )