from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import LanguageAssessment


language_llm = research_llm.with_structured_output(
    LanguageAssessment
)


async def research_language(
    country: str,
    trip_profile,
) -> LanguageAssessment:

    prompt = f"""
You are the Language Research Agent for TripGPT.

Your responsibility is to evaluate language accessibility
for the traveller at the destination.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

RESEARCH CONTEXT:

This is currently a development architecture test.

No external country-information or language research
tools have been connected yet.

Rules:
- do not invent official languages
- do not invent statistics about language usage
- do not guess tourist language accessibility
- distinguish verified facts from analysis
- use empty collections when factual information
  is unavailable
- do not fabricate sources

Return the structured LanguageAssessment.
"""

    return await execute_research_agent(
        agent_name="Language Research Agent",
        structured_llm=language_llm,
        prompt=prompt,
    )
