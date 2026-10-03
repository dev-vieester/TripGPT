from datetime import timedelta

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from app.agents.destination.executor import (
    execute_research_agent,
    ResearchAgentError,
)
from app.agents.destination.research_llm import (
    research_llm,
)
from app.agents.destination.tool_executor import (
    run_tool_loop,
)
from app.schemas.destination import WeatherAssessment
from app.tools.weather.weather_tool import (
    get_weather_forecast,
)


WEATHER_TOOLS = [
    get_weather_forecast,
]


weather_research_llm = research_llm.bind_tools(
    WEATHER_TOOLS
)


weather_synthesis_llm = (
    research_llm.with_structured_output(
        WeatherAssessment
    )
)


def calculate_trip_end_date(
    departure_date,
    duration_days: int,
):
    return departure_date + timedelta(
        days=duration_days - 1
    )


def extract_tool_evidence(
    messages,
) -> list[str]:
    """
    Extract only factual evidence returned by tools.

    We intentionally avoid passing the entire research
    conversation into the synthesis phase.
    """

    return [
        message.content
        for message in messages
        if isinstance(
            message,
            ToolMessage,
        )
    ]


def build_weather_research_messages(
    country: str,
    trip_profile,
):
    trip_end_date = calculate_trip_end_date(
        trip_profile.departure_date,
        trip_profile.trip_duration_days,
    )

    return [
        SystemMessage(
            content="""
You are the Weather Research Agent for TripGPT.

Your responsibility is to gather factual weather evidence
for the traveller's destination and travel dates.

Use the available weather tools whenever factual weather
information is required.

Rules:

- Do not invent temperatures.
- Do not invent precipitation probabilities.
- Do not invent weather conditions.
- Do not invent severe weather risks.
- Prefer tool evidence over model knowledge.
- Do not make the final destination recommendation.
- Your responsibility in this phase is research, not final
  structured synthesis.
"""
        ),

        HumanMessage(
            content=f"""
Destination:
{country}

Travel start date:
{trip_profile.departure_date}

Travel end date:
{trip_end_date}

Research the weather relevant to these travel dates.
"""
        ),
    ]

def build_weather_synthesis_prompt(
    *,
    country: str,
    trip_profile,
    evidence: list[str],
) -> str:
    trip_end_date = calculate_trip_end_date(
        trip_profile.departure_date,
        trip_profile.trip_duration_days,
    )

    evidence_text = "\n\n".join(
        evidence
    )

    return f"""
You are the Weather Synthesis Agent for TripGPT.

Your responsibility is to convert collected weather
evidence into the required WeatherAssessment structure.

Destination:
{country}

Travel dates:
{trip_profile.departure_date}
to
{trip_end_date}

WEATHER EVIDENCE:

{evidence_text}

Rules:

1. Use ONLY the supplied weather evidence.

2. Do not invent temperatures, precipitation probabilities,
   weather conditions, or severe weather risks.

3. If the supplied evidence does not support a field,
   return null or an empty list as appropriate.

4. Every externally verifiable weather fact must preserve
   the source information contained in the supplied
   evidence.

5. Do not make an overall destination recommendation.

6. suitability_notes may explain what the weather means
   for this trip, but must not introduce unsupported
   weather facts.

7. Do not claim severe weather risk unless the supplied
   evidence supports it.

8. The country field must be:
   {country}
"""

async def research_weather(
    country: str,
    trip_profile,
) -> WeatherAssessment:

    research_messages = (
        build_weather_research_messages(
            country,
            trip_profile,
        )
    )

    research_history = await run_tool_loop(
        agent_name="weather_agent",
        llm_with_tools=weather_research_llm,
        messages=research_messages,
        tools=WEATHER_TOOLS,
    )

    evidence = extract_tool_evidence(
        research_history
    )

    if not evidence:
        raise ResearchAgentError(
            "Weather agent produced no tool evidence."
        )

    synthesis_prompt = (
        build_weather_synthesis_prompt(
            country=country,
            trip_profile=trip_profile,
            evidence=evidence,
        )
    )

    assessment = await execute_research_agent(
        agent_name="weather_synthesis",
        structured_llm=weather_synthesis_llm,
        prompt=synthesis_prompt,
    )

    return assessment