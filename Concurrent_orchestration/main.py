import asyncio
from collections import defaultdict

from agent_framework import AgentExecutorResponse, AgentResponse, Message
from agent_framework.orchestrations import ConcurrentBuilder
from agent_framework_github_copilot import GitHubCopilotAgent


PROMPT = "Plan a trip to Paris."

MAX_OUTPUT_RULE = (
    "\nKeep your response short.\n"
    "- Only 2 bullet points\n"
    "- Maximum 8 words per bullet\n"
    "- No extra explanation\n"
)


def aggregate_agent_responses(results: list[AgentExecutorResponse]) -> AgentResponse:
    messages: list[Message] = []
    for result in results:
        message = next(
            (message for message in reversed(result.agent_response.messages) if message.role == "assistant"),
            None,
        )
        if message is not None:
            message.author_name = message.author_name or result.executor_id
            messages.append(message)
    return AgentResponse(messages=messages)


def print_agent_block(agent_name: str, text: str) -> None:
    print("\n" + "=" * 60)
    print(f"{agent_name}")
    print("=" * 60)
    print(text.strip())
    print("=" * 60)


def print_final_report(agent_outputs: dict[str, list[str]]) -> None:
    sections = {
        "Food & Dining": "FoodExpert",
        "Accommodation": "AccommodationExpert",
        "Activities": "ActivitiesExpert",
        "Transport": "TransportExpert",
        "Budget": "BudgetExpert",
    }

    print("\n\n" + "#" * 60)
    print("FINAL PARIS TRAVEL REPORT")
    print("#" * 60)

    for section_title, agent_name in sections.items():
        text = "\n".join(agent_outputs.get(agent_name, [])).strip()

        if not text:
            continue

        print(f"\n{section_title}")
        print("-" * 60)
        print(text)

    print("\nReport generated from concurrent agent outputs.")


async def main() -> None:

    food_agent = GitHubCopilotAgent(
        name="FoodExpert",
        instructions="You are a food expert. Suggest local food options." + MAX_OUTPUT_RULE,
    )

    accommodation_agent = GitHubCopilotAgent(
        name="AccommodationExpert",
        instructions="You are an accommodation expert. Suggest places to stay." + MAX_OUTPUT_RULE,
    )

    activities_agent = GitHubCopilotAgent(
        name="ActivitiesExpert",
        instructions="You are an activities expert. Suggest things to do." + MAX_OUTPUT_RULE,
    )

    transport_agent = GitHubCopilotAgent(
        name="TransportExpert",
        instructions="You are a transport expert. Suggest how to travel." + MAX_OUTPUT_RULE,
    )

    budget_agent = GitHubCopilotAgent(
        name="BudgetExpert",
        instructions="You are a budget expert. Suggest cost tips." + MAX_OUTPUT_RULE,
    )

    workflow = ConcurrentBuilder(
        participants=[
            food_agent,
            accommodation_agent,
            activities_agent,
            transport_agent,
            budget_agent,
        ]
    ).with_aggregator(aggregate_agent_responses).build()

    print("\nStarting Concurrent Workflow")
    print(f"Prompt: {PROMPT}")
    print("-" * 60)

    agent_outputs: dict[str, list[str]] = defaultdict(list)

    async for event in workflow.run(PROMPT, stream=True):
        if event.type == "output" and isinstance(event.data, AgentResponse):
            for message in event.data.messages:
                if not message.text:
                    continue

                agent_name = message.author_name or "UnknownAgent"

                if agent_name == "user":
                    continue

                agent_outputs[agent_name].append(message.text)

    if not agent_outputs:
        print("No agent output received.")
        return

    print("\nINDIVIDUAL AGENT OUTPUTS")

    for agent_name in [
        "FoodExpert",
        "AccommodationExpert",
        "ActivitiesExpert",
        "TransportExpert",
        "BudgetExpert",
    ]:
        if agent_name in agent_outputs:
            text = "\n".join(agent_outputs[agent_name])
            print_agent_block(agent_name, text)

    print_final_report(agent_outputs)


if __name__ == "__main__":
    asyncio.run(main())