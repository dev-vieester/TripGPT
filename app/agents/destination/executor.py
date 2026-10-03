import asyncio
import logging
from typing import Any, TypeVar

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

async def execute_llm_call(
    *,
    agent_name: str,
    llm,
    input_data: Any,
    timeout_seconds: float = 45,
):
    try:
        async with research_semaphore:

            async with asyncio.timeout(
                timeout_seconds
            ):
                return await llm.ainvoke(
                    input_data
                )

    except TimeoutError as exc:
        logger.exception(
            "%s timed out after %s seconds",
            agent_name,
            timeout_seconds,
        )

        raise ResearchAgentTimeoutError(
            f"{agent_name} timed out"
        ) from exc

    except ResearchAgentError:
        raise

    except Exception as exc:
        logger.exception(
            "%s failed",
            agent_name,
        )

        raise ResearchAgentError(
            f"{agent_name} failed"
        ) from exc

async def execute_research_agent(
    *,
    agent_name: str,
    structured_llm,
    prompt: str,
    timeout_seconds: float = 45,
) -> T:

    validate_prompt_size(prompt)

    result = await execute_llm_call(
        agent_name=agent_name,
        llm=structured_llm,
        input_data=prompt,
        timeout_seconds=timeout_seconds,
    )

    if not isinstance(result, BaseModel):
        raise ResearchAgentOutputError(
            f"{agent_name} did not return "
            f"a Pydantic model."
        )

    return result