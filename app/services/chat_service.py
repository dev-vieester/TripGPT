from uuid import uuid4
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.graph.workflow import graph
from app.schemas.trip import TripProfile

def build_config(thread_id: str) -> dict:
    return {
        "configurable":{
            "thread_id": thread_id
        }
    }

def build_initial_state(
        thread_id: str,
        message: str
) -> dict:
    return {
        "messages": [
            HumanMessage(content=message)
        ],
        "thread_id": thread_id,
        "trip_profile": TripProfile(),
        "missing_required_fields": [],
        "intake_complete": False,
        "candidate_destinations": [],
        "destination_assessments": [],
        "errors": [],
    }