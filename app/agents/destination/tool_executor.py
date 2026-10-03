import asyncio
import logging

from langchain_core.messages import (
    BaseMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool

from app.agents.destination.executor import (
    execute_llm_call,
    ResearchAgentError,
)


logger = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 5
DEFAULT_TOOL_TIMEOUT_SECONDS = 15

class ToolExecutionError(ResearchAgentError):
    pass


class ToolExecutionTimeoutError(
    ToolExecutionError
):
    pass


class UnknownToolError(
    ToolExecutionError
):
    pass


class ToolIterationLimitError(
    ToolExecutionError
):
    pass


def build_tool_registry(
    tools: list[BaseTool],
) -> dict[str, BaseTool]:

    registry = {}

    for tool in tools:

        if tool.name in registry:
            raise ToolExecutionError(
                f"Duplicate tool name: {tool.name}"
            )

        registry[tool.name] = tool

    return registry

async def execute_tool_call(
    *,
    tool_call: dict,
    tool_registry: dict[str, BaseTool],
    timeout_seconds: float = DEFAULT_TOOL_TIMEOUT_SECONDS,
) -> ToolMessage:

    tool_name = tool_call["name"]

    tool = tool_registry.get(tool_name)

    if tool is None:
        raise UnknownToolError(
            f"Unknown tool requested: {tool_name}"
        )

    try:
        async with asyncio.timeout(
            timeout_seconds
        ):
            result = await tool.ainvoke(
                tool_call["args"]
            )

    except TimeoutError as exc:

        logger.exception(
            "Tool '%s' timed out after %s seconds",
            tool_name,
            timeout_seconds,
        )

        raise ToolExecutionTimeoutError(
            f"Tool '{tool_name}' timed out"
        ) from exc

    except ToolExecutionError:
        raise

    except Exception as exc:

        logger.exception(
            "Tool '%s' failed",
            tool_name,
        )

        raise ToolExecutionError(
            f"Tool '{tool_name}' failed"
        ) from exc

    return ToolMessage(
        content=str(result),
        name=tool_name,
        tool_call_id=tool_call["id"],
    )

async def execute_tool_calls(
    *,
    tool_calls: list[dict],
    tool_registry: dict[str, BaseTool],
) -> list[ToolMessage]:

    results = []

    for tool_call in tool_calls:

        result = await execute_tool_call(
            tool_call=tool_call,
            tool_registry=tool_registry,
        )

        results.append(result)

    return results

async def run_tool_loop(
    *,
    agent_name: str,
    llm_with_tools,
    messages: list[BaseMessage],
    tools: list[BaseTool],
    max_iterations: int = MAX_TOOL_ITERATIONS,
    llm_timeout_seconds: float = 45,
) -> list[BaseMessage]:

    messages = list(messages)

    tool_registry = build_tool_registry(
        tools
    )

    for iteration in range(
        max_iterations
    ):

        ai_message = await execute_llm_call(
            agent_name=(
                f"{agent_name}"
                f"_tool_iteration_{iteration + 1}"
            ),
            llm=llm_with_tools,
            input_data=messages,
            timeout_seconds=llm_timeout_seconds,
        )

        messages.append(
            ai_message
        )

        if not ai_message.tool_calls:
            return messages

        tool_messages = await execute_tool_calls(
            tool_calls=ai_message.tool_calls,
            tool_registry=tool_registry,
        )

        messages.extend(
            tool_messages
        )

    raise ToolIterationLimitError(
        f"{agent_name} exceeded maximum "
        f"tool iterations ({max_iterations})."
    )