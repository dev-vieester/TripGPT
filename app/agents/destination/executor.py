import asyncio
import logging
from typing import TypeVar

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

MAX_PROMPT_CHARS = 25_000

MAX_CONCURRENT_RESEARCH_CALLS = 6

research_semaphore = asyncio.Semaphore(
    MAX_CONCURRENT_RESEARCH_CALLS
)

class ResearchAgentError(Exception):
    pass


class ResearchAgentTimeoutError(ResearchAgentError):
    pass


class ResearchAgentOutputError(ResearchAgentError):
    pass

class ResearchAgentInputError(ResearchAgentError):
    pass

def validate_prompt_size(
    prompt: str,
    max_chars: int = MAX_PROMPT_CHARS,
) -> None:
    if len(prompt) > max_chars:
        raise ResearchAgentInputError(
            f"Prompt exceeds maximum size of "
            f"{max_chars:,} characters."
        )


async def execute_research_agent(
        *,
        agent_name: str,
        structured_llm,
        prompt:str,
        timeout_seconds: float = 45
) -> T:

    validate_prompt_size(prompt)
    try:
        async with research_semaphore:
            async with asyncio.timeout(timeout_seconds):
                result = await structured_llm.ainvoke(prompt)

            if not isinstance(result, BaseModel):
                raise ResearchAgentOutputError(
                    f"{agent_name} did not return "
                    "a Pydantic model."
                )

            return result

    except TimeoutError as exc:
        logger.exception(
            "%s timed out after %s seconds",
            agent_name,
            timeout_seconds,
        )

        raise ResearchAgentTimeoutError(
            f"{agent_name} timed out"
        ) from exc

    except ValidationError as exc:
        logger.exception(
            "%s returned invalid structured output",
            agent_name,
        )

        raise ResearchAgentOutputError(
            f"{agent_name} returned invalid output"
        ) from exc

    except Exception as exc:
        logger.exception(
            "%s failed",
            agent_name,
        )

        raise ResearchAgentError(
            f"{agent_name} failed"
        ) from exc