import asyncio
import time
from datetime import date

from app.graph.destination.workflow import (
    destination_research_graph,
)
from app.schemas.trip import TripProfile


async def main():
    # 1. Create the same kind of profile that would normally
    #    come from your intake flow.
    trip_profile = TripProfile(
        origin_country="Nigeria",
        nationality="Nigerian",
        budget=1500,
        budget_currency="USD",
        departure_date=date(2026, 12, 20),
        trip_duration_days=7,
        interests=[
            "nature",
            "food",
            "history",
        ],
        preferred_languages=[
            "English",
        ],
        health_requirements=[],
        accessibility_requirements=[],
    )

    print("\nStarting destination research...")
    print("--------------------------------")

    start_time = time.perf_counter()

    # 2. Invoke the PARENT destination research graph.
    result = await destination_research_graph.ainvoke(
        {
            "trip_profile": trip_profile,
            "destination_research": [],
        }
    )

    elapsed = time.perf_counter() - start_time

    # 3. Get the dossiers collected by our reducer.
    dossiers = result["destination_research"]

    print("\n--------------------------------")
    print("DESTINATION RESEARCH COMPLETE")
    print("--------------------------------")

    print(f"Countries researched: {len(dossiers)}")
    print(f"Total time: {elapsed:.2f} seconds")

    # 4. Print each collected country.
    print("\nCountries:")

    for dossier in dossiers:
        print(f"- {dossier.country}")

    # 5. Verify that we actually collected 7 dossiers.
    assert len(dossiers) == 7, (
        f"Expected 7 dossiers, got {len(dossiers)}"
    )

    # 6. Make sure each dossier is for a unique country.
    countries = [
        dossier.country
        for dossier in dossiers
    ]

    assert len(set(countries)) == 7, (
        f"Expected 7 unique countries, got: {countries}"
    )

    print("\n✓ All 7 dossiers were collected successfully.")
    print("✓ All 7 countries are unique.")


if __name__ == "__main__":
    asyncio.run(main())