from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar("T")

class SourceType(str, Enum):
    GOVERNMENT = "government"
    OFFICIAL_API = "official_api"
    INTERNATIONAL_ORGANIZATION = "international_organization"
    COMMERCIAL_API = "commercial_api"
    RAG_DOCUMENT = "rag_document"
    WEB = "web"

class ResearchSource(BaseModel):
    name: str
    publisher: str | None = None
    url: str | None = None

    source_type: SourceType

    retrieved_at: datetime
    published_at: datetime | None = None

class SourcedFact(BaseModel, Generic[T]):
    value: T

    sources: list[ResearchSource] = Field(
        default_factory=list
    )

class CandidateDestination(BaseModel):
    country: str
    reason: str


class CandidateDestinationList(BaseModel):
    destinations: list[CandidateDestination] = Field(
        min_length=1,
        max_length=15,
    )

class VisaAssessment(BaseModel):
    country: str

    visa_required: SourcedFact[bool | None]

    visa_type: SourcedFact[str | None]

    entry_requirements: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    notes: str | None = None

class VisaProcessingAssessment(BaseModel):
    country: str

    processing_time_days: SourcedFact[int | None]

    application_method: SourcedFact[str | None]

    expedited_processing_available: SourcedFact[
        bool | None
    ]

    processing_notes: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

class BudgetAssessment(BaseModel):
    country: str

    estimated_flight_cost: SourcedFact[float | None]

    estimated_accommodation_cost_per_night: SourcedFact[
        float | None
    ]

    estimated_daily_food_cost: SourcedFact[float | None]

    estimated_daily_transport_cost: SourcedFact[float | None]

    estimated_total_cost: float | None = None

    within_budget: bool | None = None

    calculation_notes: str | None = None

class SafetyAssessment(BaseModel):
    country: str

    advisory_level: SourcedFact[str | None]

    active_conflict: SourcedFact[bool | None]

    major_restrictions: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    safety_notes: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

class AttractionAssessment(BaseModel):
    country: str

    attractions: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    activities: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    interest_match_notes: str | None = None

class LanguageAssessment(BaseModel):
    country: str

    official_languages: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    commonly_spoken_languages: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    tourist_language_accessibility: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    language_notes: str | None = None

class WeatherAssessment(BaseModel):
    country: str

    expected_temperature_celsius: SourcedFact[
        float | None
    ]

    expected_conditions: SourcedFact[str | None]

    rainfall_probability: SourcedFact[float | None]

    severe_weather_risks: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    suitability_notes: str | None = None

class OutbreakAssessment(BaseModel):
    country: str

    active_outbreaks: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    outbreak_restrictions: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    outbreak_advisories: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

class HealthAssessment(BaseModel):
    country: str

    vaccination_requirements: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    entry_health_requirements: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    health_risks: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

    healthcare_notes: list[
        SourcedFact[str]
    ] = Field(default_factory=list)

class CountryResearchDossier(BaseModel):
    country: str

    visa: VisaAssessment
    visa_processing: VisaProcessingAssessment
    budget: BudgetAssessment
    safety: SafetyAssessment
    health: HealthAssessment
    outbreak: OutbreakAssessment
    weather: WeatherAssessment
    language: LanguageAssessment
    attractions: AttractionAssessment
