from app.graph.destination.state import CountryResearchState

from app.schemas.destination import CountryResearchDossier

from app.agents.destination.specialists.visa_agent import (
    research_visa,
)
from app.agents.destination.specialists.visa_processing_agent import (
    research_visa_processing,
)
from app.agents.destination.specialists.budget_agent import (
    research_budget,
)
from app.agents.destination.specialists.safety_agent import (
    research_safety,
)
from app.agents.destination.specialists.health_agent import (
    research_health,
)
from app.agents.destination.specialists.outbreak_agent import (
    research_outbreak,
)
from app.agents.destination.specialists.weather_agent import (
    research_weather,
)
from app.agents.destination.specialists.language_agent import (
    research_language,
)
from app.agents.destination.specialists.attractions_agent import (
    research_attractions,
)


async def visa_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_visa(
        state["country"],
        state["trip_profile"],
    )

    return {"visa": result}


async def visa_processing_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_visa_processing(
        state["country"],
        state["trip_profile"],
    )

    return {"visa_processing": result}


async def budget_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_budget(
        state["country"],
        state["trip_profile"],
    )

    return {"budget": result}


async def safety_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_safety(
        state["country"],
        state["trip_profile"],
    )

    return {"safety": result}


async def health_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_health(
        state["country"],
        state["trip_profile"],
    )

    return {"health": result}


async def outbreak_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_outbreak(
        state["country"],
        state["trip_profile"],
    )

    return {"outbreak": result}


async def weather_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_weather(
        state["country"],
        state["trip_profile"],
    )

    return {"weather": result}


async def language_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_language(
        state["country"],
        state["trip_profile"],
    )

    return {"language": result}


async def attractions_agent(
    state: CountryResearchState,
) -> dict:
    result = await research_attractions(
        state["country"],
        state["trip_profile"],
    )

    return {"attractions": result}


async def build_country_dossier(
    state: CountryResearchState,
) -> dict:

    dossier = CountryResearchDossier(
        country=state["country"],
        visa=state["visa"],
        visa_processing=state["visa_processing"],
        budget=state["budget"],
        safety=state["safety"],
        health=state["health"],
        outbreak=state["outbreak"],
        weather=state["weather"],
        language=state["language"],
        attractions=state["attractions"],
    )

    return {
        "dossier": dossier
    }