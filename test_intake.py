import asyncio
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.graph.workflow import graph
from app.schemas.trip import TripProfile


async def main():

    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print(f"\nThread ID: {thread_id}")
    print("-" * 50)

    first_message = input("\nYou: ")

    initial_state = {
        "messages": [
            HumanMessage(content=first_message)
        ],
        "thread_id": thread_id,
        "trip_profile": TripProfile(),
        "missing_required_fields": [],
        "intake_complete": False,
        "candidate_destinations": [],
        "destination_assessments": [],
        "errors": [],
    }

    result = await graph.ainvoke(
        initial_state,
        config=config,
    )

    while "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0].value

        print(
            f"\nTripGPT: "
            f"{interrupt_data['message']}"
        )

        user_response = input("\nYou: ")

        result = await graph.ainvoke(
            Command(resume=user_response),
            config=config,
        )

    print("\n" + "=" * 50)
    print("FINAL STATE")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
