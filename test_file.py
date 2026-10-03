import asyncio
import time
from datetime import date

from app.agents.destination.specialists.weather_agent import (
    research_weather,
)
from app.schemas.trip import TripProfile


async def main():
    # Keep these dates inside Open-Meteo's available
    # forecast window while testing.
    trip_profile = TripProfile(
        origin_country="Nigeria",
        nationality="Nigerian",
        budget=1500,
        budget_currency="USD",

        departure_date=date(2026, 10, 5),
        trip_duration_days=3,

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

    country = "France"

    print("\nStarting Weather Agent test...")
    print("--------------------------------")

    start_time = time.perf_counter()

    try:
        assessment = await research_weather(
            country=country,
            trip_profile=trip_profile,
        )

    except Exception as exc:
        elapsed = time.perf_counter() - start_time

        print("\n❌ WEATHER AGENT FAILED")
        print("--------------------------------")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error: {exc}")
        print(f"Time before failure: {elapsed:.2f}s")

        raise

    elapsed = time.perf_counter() - start_time

    print("\n--------------------------------")
    print("WEATHER AGENT COMPLETE")
    print("--------------------------------")

    print(f"Country: {assessment.country}")
    print(f"Total time: {elapsed:.2f}s")

    print("\nFULL ASSESSMENT")
    print("--------------------------------")

    print(
        assessment.model_dump_json(
            indent=2
        )
    )

    # Basic validation
    assert isinstance(
        assessment.country,
        str,
    )

    assert assessment.country == country

    print("\n✓ WeatherAssessment returned successfully.")
    print("✓ Country matches requested destination.")


if __name__ == "__main__":
    asyncio.run(main())