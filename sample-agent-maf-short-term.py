import asyncio
from agent_framework import   Message
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
# 1. Use the official handler class provided by the underlying copilot package
from copilot.session import PermissionHandler


async def main():
    # 2. Assign the built-in approve_all helper method directly
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Assistant Agent",
        instructions="You Are Helpful Weather Assistant.",
    )
    session= agent.create_session()
    print("Agent configured")
    prompt = (
            "Give Me some bullet points for microsoft agent framework in AI"
            )

    user_message1= Message(
        role="user",
        contents= [prompt]
        )
  
        
    result = await agent.run(user_message1,session=session)
    print(result.text)
    prompt2 = (
            "Can You Add Some Emojis to the same response"
            )

    user_message2= Message(
        role="user",
        contents= [prompt2]
        )
  
        
    result2 = await agent.run(user_message2,session=session)
    print(result2.text)


if __name__ == "__main__":
    asyncio.run(main())
    

