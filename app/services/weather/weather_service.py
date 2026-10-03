from datetime import date, datetime, timezone

import httpx

from app.tools.weather.schemas import (
    DailyWeather,
    WeatherForecastResult,
)


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


class WeatherServiceError(Exception):
    """Base exception for weather service failures."""


class LocationNotFoundError(WeatherServiceError):
    """Raised when a destination cannot be geocoded."""


class WeatherProviderError(WeatherServiceError):
    """Raised when the weather provider request fails."""

async def geocode_location(
    location: str,
    client: httpx.AsyncClient,
) -> dict:

    try:
        response = await client.get(
            GEOCODING_URL,
            params={
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json",
            },
        )

        response.raise_for_status()

    except httpx.HTTPError as exc:
        raise WeatherProviderError(
            "Failed to geocode destination."
        ) from exc

    data = response.json()

    results = data.get("results", [])

    if not results:
        raise LocationNotFoundError(
            f"Could not find location: {location}"
        )

    result = results[0]

    return {
        "name": result.get("name"),
        "country": result.get("country"),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone"),
    }

async def fetch_weather_forecast(
    location: str,
    start_date: date,
    end_date: date,
) -> WeatherForecastResult:

    timeout = httpx.Timeout(
        10.0,
        connect=5.0,
    )

    async with httpx.AsyncClient(
        timeout=timeout
    ) as client:

        coordinates = await geocode_location(
            location,
            client,
        )

        try:
            response = await client.get(
                FORECAST_URL,
                params={
                    "latitude": coordinates["latitude"],
                    "longitude": coordinates["longitude"],
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "daily": (
                        "temperature_2m_max,"
                        "temperature_2m_min,"
                        "precipitation_probability_max,"
                        "weather_code"
                    ),
                    "timezone": "auto",
                },
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise WeatherProviderError(
                "Failed to retrieve weather forecast."
            ) from exc

        data = response.json()

        daily_data = data.get("daily", {})

        dates = daily_data.get("time", [])
        max_temps = daily_data.get(
            "temperature_2m_max",
            [],
        )
        min_temps = daily_data.get(
            "temperature_2m_min",
            [],
        )
        precipitation = daily_data.get(
            "precipitation_probability_max",
            [],
        )
        weather_codes = daily_data.get(
            "weather_code",
            [],
        )

        daily_weather = []

        for index, day in enumerate(dates):
            daily_weather.append(
                DailyWeather(
                    date=date.fromisoformat(day),

                    temperature_max_c=(
                        max_temps[index]
                        if index < len(max_temps)
                        else None
                    ),

                    temperature_min_c=(
                        min_temps[index]
                        if index < len(min_temps)
                        else None
                    ),

                    precipitation_probability_max=(
                        precipitation[index]
                        if index < len(precipitation)
                        else None
                    ),

                    weather_code=(
                        weather_codes[index]
                        if index < len(weather_codes)
                        else None
                    ),
                )
            )
        return WeatherForecastResult(
            location=location,
            latitude=coordinates["latitude"],
            longitude=coordinates["longitude"],
            timezone=data.get(
                "timezone",
                coordinates.get("timezone"),
            ),
            daily=daily_weather,
            source_name="Open-Meteo",
            source_url=str(response.url),
            retrieved_at=datetime.now(timezone.utc),
        )

def weather_code_to_condition(
    code: int | None,
) -> str | None:

    if code is None:
        return None

    conditions = {
        0: "clear_sky",
        1: "mainly_clear",
        2: "partly_cloudy",
        3: "overcast",
        45: "fog",
        48: "rime_fog",
        51: "light_drizzle",
        53: "moderate_drizzle",
        55: "dense_drizzle",
        56: "light_freezing_drizzle",
        57: "dense_freezing_drizzle",
        61: "slight_rain",
        63: "moderate_rain",
        65: "heavy_rain",
        66: "light_freezing_rain",
        67: "heavy_freezing_rain",
        71: "slight_snow",
        73: "moderate_snow",
        75: "heavy_snow",
        77: "snow_grains",
        80: "slight_rain_showers",
        81: "moderate_rain_showers",
        82: "violent_rain_showers",
        85: "slight_snow_showers",
        86: "heavy_snow_showers",
        95: "thunderstorm",
        96: "thunderstorm_with_slight_hail",
        99: "thunderstorm_with_heavy_hail",
    }

    return conditions.get(
        code,
        "unknown",
    )