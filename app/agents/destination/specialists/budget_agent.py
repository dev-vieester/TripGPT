from app.agents.destination.executor import execute_research_agent
from app.agents.destination.research_llm import research_llm
from app.schemas.destination import BudgetAssessment


budget_llm = research_llm.with_structured_output(
    BudgetAssessment
)


async def research_budget(
    country: str,
    trip_profile,
) -> BudgetAssessment:

    prompt = f"""
You are the Budget Research Agent for TripGPT.

Your responsibility is to evaluate the likely financial
feasibility of travelling to the destination.

Destination:
{country}

Traveller profile:
{trip_profile.model_dump_json(indent=2)}

No external pricing tools are connected yet.

This is an architecture test.

Rules:
- do not invent flight prices
- do not invent hotel prices
- do not invent food prices
- do not invent transport prices
- use null when information is unavailable
- do not fabricate sources

Return the structured BudgetAssessment.
"""

    return await execute_research_agent(
        agent_name="Budget Research Agent",
        structured_llm=budget_llm,
        prompt=prompt,
    )
