from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import SafetyAssessment


safety_llm = research_llm.with_structured_output(
    SafetyAssessment
)


async def research_safety(
    country: str,
    trip_profile,
) -> SafetyAssessment:

    prompt = f"""
You are the Safety Research Agent for TripGPT.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

No external travel advisory or conflict research tool
is connected yet.

Rules:
- do not guess current advisory levels
- do not guess whether an active conflict exists
- do not fabricate travel restrictions
- use null or empty collections when evidence is unavailable
- do not fabricate sources

Return the structured SafetyAssessment.
"""

    return await execute_research_agent(
        agent_name="Safety Research Agent",
        structured_llm=safety_llm,
        prompt=prompt,
    )
