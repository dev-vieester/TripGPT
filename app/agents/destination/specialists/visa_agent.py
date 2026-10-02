from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import VisaAssessment


visa_llm = research_llm.with_structured_output(
    VisaAssessment
)


async def research_visa(
    country: str,
    trip_profile,
) -> VisaAssessment:

    prompt = f"""
You are the Visa Research Agent for TripGPT.

Your responsibility is to evaluate visa and entry
requirements for the traveller.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

RESEARCH CONTEXT:

This is currently a development test.

No external visa research tool has been connected yet.

Therefore:
- do not invent visa requirements
- do not guess visa types
- do not claim current entry requirements
- use null where factual information is unavailable
- sources should be empty when no source was provided

Return the structured VisaAssessment.
"""

    return await execute_research_agent(
        agent_name="Visa Research Agent",
        structured_llm=visa_llm,
        prompt=prompt,
    )
