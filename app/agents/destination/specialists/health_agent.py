from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import HealthAssessment


health_llm = research_llm.with_structured_output(
    HealthAssessment
)


async def research_health(
    country: str,
    trip_profile,
) -> HealthAssessment:

    prompt = f"""
You are the Health Research Agent for TripGPT.

Your responsibility is to research travel-related health
requirements and relevant health considerations for the
destination.

You do not diagnose medical conditions and you do not
determine whether a traveller is medically fit to travel.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

RESEARCH CONTEXT:

This is currently a development architecture test.

No external health, government, WHO, CDC, or other
health-information tools have been connected yet.

Rules:
- do not invent vaccination requirements
- do not invent health-entry requirements
- do not invent destination health risks
- do not make medical diagnoses
- do not claim that the traveller is medically fit to travel
- use empty collections when verified information is unavailable
- do not fabricate sources

Return the structured HealthAssessment.
"""

    return await execute_research_agent(
        agent_name="Health Research Agent",
        structured_llm=health_llm,
        prompt=prompt,
    )
