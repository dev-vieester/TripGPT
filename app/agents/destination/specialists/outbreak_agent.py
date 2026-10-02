from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import OutbreakAssessment


outbreak_llm = research_llm.with_structured_output(
    OutbreakAssessment
)


async def research_outbreak(
    country: str,
    trip_profile,
) -> OutbreakAssessment:

    prompt = f"""
You are the Disease Outbreak Research Agent for TripGPT.

Your responsibility is to research current disease
outbreaks, outbreak-related advisories, and relevant
travel restrictions for the destination.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

RESEARCH CONTEXT:

This is currently a development architecture test.

No external outbreak-monitoring, WHO, government,
or health-advisory tools have been connected yet.

Rules:
- do not invent active outbreaks
- do not assume there is no outbreak simply because
  no research data was provided
- do not invent outbreak-related restrictions
- do not invent health advisories
- use empty collections when information is unavailable
- do not fabricate sources

Return the structured OutbreakAssessment.
"""

    return await execute_research_agent(
        agent_name="Disease Outbreak Research Agent",
        structured_llm=outbreak_llm,
        prompt=prompt,
    )
