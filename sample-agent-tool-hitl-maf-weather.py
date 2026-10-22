import asyncio

from agent_framework import tool
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.generated.rpc import PermissionDecisionApproveOnce, PermissionDecisionReject


@tool(approval_mode="always_require")
async def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny with a high of 25°C."


async def ask_for_approval(request, invocation):
    print(f"\nApproval required for: {request}")
    answer = await asyncio.to_thread(input, "Approve this request? (y/n): ")

    if answer.strip().lower() == "y":
        return PermissionDecisionApproveOnce()
    return PermissionDecisionReject(feedback="The user denied this request.")


async def main():
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=ask_for_approval,
        ),
        name="simple-agent-hitl",
        description="An agent with human-in-the-loop tool approval.",
        instructions="You are a helpful assistant which generates 1 page weather report with emojis.",
        tools=[get_weather],
    )
    print("Agent configured")
    session = agent.create_session()

    user_input = input("Enter your prompt: ")
    result = await agent.run(user_input, session=session)

    print(f"\nResponse: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())