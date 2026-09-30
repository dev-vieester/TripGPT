class TripGPTError(Exception):
    """Base exception for TripGPT."""

class LLMProviderError(TripGPTError):
    """Raised when the LLM provider request fails."""

class LLMStructuredOutputError(TripGPTError):
    """Raised when structured LLM output cannot be validated."""