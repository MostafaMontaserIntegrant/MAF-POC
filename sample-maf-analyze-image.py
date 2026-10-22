import asyncio
import subprocess
import time
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from agent_framework import Content, Message
# 1. Use the official handler class provided by the underlying copilot package
from copilot.session import PermissionHandler

async def main():
    with open("/Users/yn21968/Downloads/image.png", "rb") as image_file:
        image_data = image_file.read()
    # 2. Assign the built-in approve_all helper method directly
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
    name="Assistant Agent",
    instructions="You Are Helpful Assistant.",
        
    )
    print("Agent configured")

    
    user_message= Message(
        role="user",
        contents= [
            Content.from_data(data=image_data, media_type="image/png"),
            Content.from_text("Provide an analysis of the image and provide interesting facts"),
            ],
        )   
    stream = await agent.run(user_message ,stream=True)
    async for chunk in stream:
        print(chunk.text,end="" , flush=True)


if __name__ == "__main__":
    asyncio.run(main())
