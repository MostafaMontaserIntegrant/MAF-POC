import asyncio
import subprocess
import time
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from agent_framework import Message
# 1. Use the official handler class provided by the underlying copilot package
from copilot.session import PermissionHandler

async def main():
    # 2. Assign the built-in approve_all helper method directly
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
    name="Assistant Agent",
    instructions="You Are Helpful Assistant.",
        
    )
    print("Agent configured")

    prompt = (
            "Give Me some bullet points for microsoft agent framework in AI"
            )
    user_message= Message(
        role="user",
        contents= [prompt],
        )   
    result = await agent.run(user_message )
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
