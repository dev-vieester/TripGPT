from pydantic import BaseModel, Field, field_validator
from datetime import date

LIST_TRIP_FIELDS = {
    "interests",
    "preferred_languages",
    "health_requirements",
    "accessibility_requirements",
}

REQUIRED_TRIP_FIELDS = [
    "origin_country",
    "nationality",
    "budget",
    "budget_currency",
    "departure_date",
    "trip_duration_days",
    "interests",
    "preferred_languages",
    "health_requirements",
    "accessibility_requirements",
]

class TripProfile(BaseModel):
    origin_country: str | None = None
    nationality: str | None = None

    budget: float | None = Field(default=None, gt = 0)
    budget_currency: str | None = None

    departure_date: date | None = None
    trip_duration_days: int | None = Field(default=None, gt=0)

    interests: list[str] | None = None
    preferred_languages: list[str] | None = None

    health_requirements: list[str] | None = None
    accessibility_requirements: list[str] | None = None

    @field_validator(
        "interests",
        "preferred_languages",
        "health_requirements",
        "accessibility_requirements",
        mode="before",
    )
    @classmethod
    def normalize_empty_list_fields(cls, value):
        if isinstance(value, str) and value.strip() == "":
            return []

        return value
