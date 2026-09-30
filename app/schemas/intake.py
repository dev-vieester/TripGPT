from datetime import date

from pydantic import BaseModel, Field


class TripInformationExtraction(BaseModel):
    """Travel information explicitly provided or clearly stated by the user."""

    origin_country: str | None = Field(
        default=None,
        description="Country the user will travel from."
    )

    nationality: str | None = Field(
        default=None,
        description=(
            "Nationality/passport the user will travel with. "
            "Do not infer this from their country of residence."
        )
    )

    budget: float | None = Field(
        default=None,
        description="Total travel budget as a number."
    )

    budget_currency: str | None = Field(
        default=None,
        description="ISO-style currency code such as USD, NGN, GBP or EUR."
    )

    departure_date: date | None = Field(
        default=None,
        description="Planned departure date if explicitly known."
    )

    trip_duration_days: int | None = Field(
        default=None,
        gt=0,
        description="Number of days available for the trip."
    )

    interests: list[str] | None = Field(
        default=None,
        description="Activities or travel interests explicitly mentioned."
    )

    preferred_languages: list[str] | None= Field(
        default=None,
        description="Languages the traveller prefers or speaks."
    )

    health_requirements: list[str] | None = Field(
        default=None,
        description="Health-related travel requirements explicitly mentioned."
    )

    accessibility_requirements: list[str] | None = Field(
        default=None,
        description="Accessibility requirements explicitly mentioned."
    )