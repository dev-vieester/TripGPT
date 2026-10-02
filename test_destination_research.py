import asyncio
import time

from app.graph.destination.workflow import (
    country_research_graph,
)

from app.schemas.trip import TripProfile


async def main():

    initial_state = {
        "country": "Kenya",

        "trip_profile": TripProfile(
            origin_country="Nigeria",
            nationality="Nigerian",
            budget=1500,
            budget_currency="USD",
            trip_duration_days=7,
        ),

        "visa": None,
        "visa_processing": None,
        "budget": None,
        "safety": None,
        "health": None,
        "outbreak": None,
        "weather": None,
        "language": None,
        "attractions": None,

        "dossier": None,
    }

    start = time.perf_counter()

    result = await country_research_graph.ainvoke(
        initial_state
    )

    elapsed = time.perf_counter() - start

    print("\n--- COUNTRY DOSSIER ---")
    print(result["dossier"])

    print(
        f"\nResearch completed in "
        f"{elapsed:.2f} seconds"
    )


asyncio.run(main())