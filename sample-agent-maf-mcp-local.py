import asyncio
from agent_framework import Message
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.session import PermissionHandler


async def main():
    async with (
        GitHubCopilotAgent(
            default_options=GitHubCopilotOptions(
                on_permission_request=PermissionHandler.approve_all,
                mcp_servers={
                    "Playwright MCP": {
                        "type": "stdio",
                        "command": "npx",
                        "args": ["-y", "@playwright/mcp@latest"],
                        "tools": ["*"],
                    }
                },
            ),
            name="WebResearchAgent",
            instructions=(
                "You are a web research assistant. "
                "Use Playwright MCP to open web pages, inspect their content, "
                "and interact with page controls when needed. "
                "Only report information you can verify from the page."
            ),
        ) as agent,
    ):
        session = agent.create_session()
        print("Agent configured")

        prompt = "Open https://learn.microsoft.com/en-us/agent-framework/ and summarize the main concepts."
        user_message = Message(role="user", contents=[prompt])
        result = await agent.run(user_message, session=session)
        print(result.text)
        
        print("Second PROMPT ACTION")

        prompt = "Open https://www.python.org/, find the latest Python release shown on the page, and report it."
        user_message = Message(role="user", contents=[prompt])
        result = await agent.run(user_message, session=session)
        print(result.text) 

if __name__ == "__main__":
    asyncio.run(main())
    

