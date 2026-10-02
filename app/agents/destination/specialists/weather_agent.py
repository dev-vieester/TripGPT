from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import WeatherAssessment


weather_llm = research_llm.with_structured_output(
    WeatherAssessment
)


async def research_weather(
    country: str,
    trip_profile,
) -> WeatherAssessment:

    prompt = f"""
You are the Weather Research Agent for TripGPT.

Your responsibility is to evaluate expected weather
conditions for the traveller's planned travel period.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

Pay particular attention to:
- departure date
- trip duration
- weather-related traveller preferences when available

RESEARCH CONTEXT:

This is currently a development architecture test.

No weather API or external weather research tool has
been connected yet.

Rules:
- do not invent temperatures
- do not invent weather forecasts
- do not invent rainfall probabilities
- do not invent severe-weather risks
- do not substitute generic climate knowledge for a
  current weather forecast
- use null when numeric information is unavailable
- use empty collections where appropriate
- do not fabricate sources

Return the structured WeatherAssessment.
"""

    return await execute_research_agent(
        agent_name="Weather Research Agent",
        structured_llm=weather_llm,
        prompt=prompt,
    )
