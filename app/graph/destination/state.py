import operator
from typing import TypedDict, Annotated
from app.schemas.trip import TripProfile
from app.schemas.destination import (
    VisaAssessment,
    VisaProcessingAssessment,
    BudgetAssessment,
    SafetyAssessment,
    HealthAssessment,
    OutbreakAssessment,
    WeatherAssessment,
    LanguageAssessment,
    AttractionAssessment,
    CountryResearchDossier,
)

class CountryResearchState(TypedDict):
    country: str
    trip_profile: TripProfile

    visa: VisaAssessment | None
    visa_processing: VisaProcessingAssessment | None
    budget: BudgetAssessment | None
    safety: SafetyAssessment | None
    health: HealthAssessment | None
    outbreak: OutbreakAssessment | None
    weather: WeatherAssessment | None
    language: LanguageAssessment | None
    attractions: AttractionAssessment | None

    dossier: CountryResearchDossier | None

class DestinationResearchState(TypedDict):
    trip_profile: TripProfile

    destination_research: Annotated[
        list[CountryResearchDossier],
        operator.add
    ]

