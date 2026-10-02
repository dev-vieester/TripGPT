from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import AttractionAssessment


attractions_llm = research_llm.with_structured_output(
    AttractionAssessment
)


async def research_attractions(
    country: str,
    trip_profile,
) -> AttractionAssessment:

    prompt = f"""
You are the Attractions Research Agent for TripGPT.

Your responsibility is to research attractions and
activities at the destination that may match the
traveller's interests.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

Pay particular attention to the traveller's interests
when they are available.

RESEARCH CONTEXT:

This is currently a development architecture test.

No places API, tourism API, RAG source, or external
attraction research tool has been connected yet.

Rules:
- do not invent attractions
- do not invent activities
- do not fabricate opening hours, prices, or availability
- do not claim an attraction matches the traveller unless
  supported by available information
- use empty collections when factual information is unavailable
- do not fabricate sources

Return the structured AttractionAssessment.
"""

    return await execute_research_agent(
        agent_name="Attractions Research Agent",
        structured_llm=attractions_llm,
        prompt=prompt,
    )
