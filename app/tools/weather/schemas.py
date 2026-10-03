from datetime import date, datetime

from pydantic import BaseModel, Field


class WeatherForecastInput(BaseModel):
    location: str = Field(
        description="Country, city, or destination to retrieve weather for."
    )

    start_date: date = Field(
        description="First date of the requested weather forecast."
    )

    end_date: date = Field(
        description="Last date of the requested weather forecast."
    )


class DailyWeather(BaseModel):
    date: date

    temperature_max_c: float | None = None
    temperature_min_c: float | None = None

    precipitation_probability_max: float | None = None

    weather_code: int | None = None

    condition: str | None = None


class WeatherForecastResult(BaseModel):
    location: str

    latitude: float
    longitude: float

    timezone: str | None = None

    daily: list[DailyWeather] = Field(
        default_factory=list,
        max_length=14,
    )

    source_name: str
    source_url: str
    retrieved_at: datetime