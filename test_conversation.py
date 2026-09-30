import asyncio

from app.agents.conversation_router_agent import (
    classify_conversation_intent,
)
from app.schemas.conversation import ConversationStage
from app.schemas.trip import TripProfile


async def main():

    print("=" * 60)
    print("TripGPT Stateful Conversation Router Test")
    print("=" * 60)

    print(
        "\nCommands:"
        "\n  exit    - stop"
        "\n  state   - show current test state"
        "\n"
    )

    current_stage = ConversationStage.NEW

    pending_fields = None

    trip_profile = TripProfile()

    while True:

        message = input("\nYou: ").strip()

        if not message:
            continue

        if message.lower() in {"exit", "quit"}:
            print("\nExiting router test.")
            break

        if message.lower() == "state":

            print("\n--- Current State ---")
            print(f"Stage: {current_stage.value}")
            print(f"Pending: {pending_fields}")
            print(
                "Trip Profile:",
                trip_profile.model_dump(mode="json"),
            )
            print("---------------------")

            continue

        try:

            result = await classify_conversation_intent(
                message=message,
                current_stage=current_stage,
                pending_fields=pending_fields,
                trip_profile=trip_profile,
            )

            print("\n--- Router Result ---")
            print(
                f"Intent: {result.intent.value}"
            )
            print(
                f"Reason: {result.reasoning}"
            )
            print("---------------------")

        except Exception as exc:
            print(
                f"\nRouter error: {exc}"
            )


if __name__ == "__main__":
    asyncio.run(main())