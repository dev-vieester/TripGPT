from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import VisaProcessingAssessment


visa_processing_llm = research_llm.with_structured_output(
    VisaProcessingAssessment
)


async def research_visa_processing(
    country: str,
    trip_profile,
) -> VisaProcessingAssessment:

    prompt = f"""
You are the Visa Processing Research Agent for TripGPT.

Your responsibility is to evaluate whether the traveller
can realistically complete the visa application process
before their planned departure date.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

RESEARCH CONTEXT:

This is currently a development architecture test.

No external immigration or visa-processing tools have
been connected yet.

Rules:
- do not invent visa processing times
- do not invent application methods
- do not guess whether expedited processing exists
- do not claim current immigration policies
- use null when factual information is unavailable
- use empty collections where appropriate
- sources must be empty when no source was provided

Return the structured VisaProcessingAssessment.
"""

    return await execute_research_agent(
        agent_name="Visa Processing Research Agent",
        structured_llm=visa_processing_llm,
        prompt=prompt,
    )
