import asyncio
import subprocess
import time
from agent_framework import   Message , tool
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
# 1. Use the official handler class provided by the underlying copilot package
from copilot.session import PermissionHandler

@tool
async def get_weather(location: str) -> str:
    # Simulate fetching weather information for the given location
    return f"The weather in {location} is sunny with a high of 25°C."
async def main():
    # 2. Assign the built-in approve_all helper method directly
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Weather Agent",
        instructions="You Are Helpful Weather Assistant.",
        tools=[get_weather]
    )
    print("Agent configured")
    prompt = (
                "What is the weather like in London?"
                )

    
  
        
    result = await agent.run(prompt)
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
    

