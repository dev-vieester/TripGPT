from pydantic import ValidationError
from app.core.exceptions import (
    LLMProviderError,
    LLMStructuredOutputError
)
from app.prompts import SYSTEM_PROMPT

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.schemas.intake import TripInformationExtraction

llm = ChatGoogleGenerativeAI(
    model=settings.google_model,
    temperature=0,
    api_key=settings.google_api_key,
    timeout=30,
    max_retries=2,
)

structured_llm = llm.with_structured_output(TripInformationExtraction)
SYSTEM_PROMPT = SYSTEM_PROMPT

async def extract_trip_information(
        message:str,
) -> TripInformationExtraction:
    try:
        result = await structured_llm.ainvoke(
            [
                ("system", SYSTEM_PROMPT),
                ("human", message)
            ]
        )
        return result
    except ValidationError as exc:
        raise LLMStructuredOutputError(
            "The LLM returned an invalid trip information structure."
        ) from exc
    except(
        TimeoutError,
        ConnectionError
    ) as exc:
        raise LLMProviderError(
            "The LLM provider could not be reached."
        ) from exc
    except Exception as exc:
        raise LLMProviderError(
            "The LLM provider failed while extracting trip information."
        ) from exc




