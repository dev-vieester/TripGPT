from langchain_core.tools import tool

from app.tools.weather.schemas import (
    WeatherForecastInput,
)
from app.services.weather.weather_service import (
    fetch_weather_forecast,
)


@tool(
    "get_weather_forecast",
    args_schema=WeatherForecastInput,
)
async def get_weather_forecast(
    location: str,
    start_date,
    end_date,
) -> str:
    """
    Retrieve daily weather forecast information for a destination
    over a specified date range.

    Use this tool when current forecast data is needed for travel
    planning. Do not use it for historical climate information or
    dates outside the provider's supported forecast range.
    """

    result = await fetch_weather_forecast(
        location=location,
        start_date=start_date,
        end_date=end_date,
    )

    return result.model_dump_json()