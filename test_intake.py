import asyncio
from uuid import uuid4

from langchain_core.messages import HumanMessage

from app.graph.workflow import graph
from app.schemas.conversation import ConversationStage
from app.schemas.trip import TripProfile


async def main():
    # One thread_id = one TripGPT conversation
    thread_id = str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("=" * 60)
    print("TripGPT Conversation Test")
    print("=" * 60)
    print(f"Thread ID: {thread_id}")
    print("Type 'exit' to stop.\n")

    first_turn = True

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("\nConversation ended.")
            break

        if not user_input:
            continue

        # On the first invocation, initialize our TripGPT state.
        if first_turn:
            input_state = {
                "messages": [
                    HumanMessage(content=user_input)
                ],
                "thread_id": thread_id,
                "current_stage": ConversationStage.NEW,
                "current_intent": None,
                "trip_profile": TripProfile(),
                "missing_required_fields": [],
                "pending_fields": [],
                "intake_complete": False,
                "candidate_destinations": [],
                "destination_assessments": [],
                "selected_destination": None,
                "errors": [],
            }

            first_turn = False

        else:
            # After the first invocation, the checkpointer already
            # contains the existing state.
            #
            # We only need to add the new user message.
            input_state = {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            }

        try:
            result = await graph.ainvoke(
                input_state,
                config=config,
            )

        except Exception as exc:
            print("\n[ERROR]")
            print(type(exc).__name__)
            print(str(exc))
            print()
            continue

        print("\n" + "-" * 60)

        # Latest AI response
        messages = result.get("messages", [])

        if messages:
            latest_message = messages[-1]

            print(
                f"TripGPT: "
                f"{getattr(latest_message, 'content', '')}"
            )

        # Debug information
        print("\n[DEBUG STATE]")

        current_intent = result.get("current_intent")
        current_stage = result.get("current_stage")

        print(
            "Intent:",
            getattr(current_intent, "value", current_intent)
        )

        print(
            "Stage:",
            getattr(current_stage, "value", current_stage)
        )

        print(
            "Pending fields:",
            result.get("pending_fields")
        )

        print(
            "Missing fields:",
            result.get("missing_required_fields")
        )

        print(
            "Intake complete:",
            result.get("intake_complete")
        )

        trip_profile = result.get("trip_profile")

        if trip_profile:
            print("\nTrip Profile:")

            for field, value in trip_profile.model_dump().items():
                print(f"  {field}: {value}")

        print("-" * 60)
        print()


if __name__ == "__main__":
    asyncio.run(main())