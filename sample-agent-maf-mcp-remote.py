import asyncio
import os

from agent_framework import Message
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.session import PermissionHandler


async def main():
    mcp_url = os.environ.get(
        "MCP_SERVER_URL",
        "https://remote.mcpservers.org/fetch/mcp",
    )

    mcp_headers = {}
    mcp_token = os.environ.get("MCP_TOKEN")
    if mcp_token:
        mcp_headers["Authorization"] = f"Bearer {mcp_token}"

    async with (
        GitHubCopilotAgent(
            default_options=GitHubCopilotOptions(
                on_permission_request=PermissionHandler.approve_all,
                mcp_servers={
                    "Remote Fetch MCP": {
                        "type": "http",
                        "url": mcp_url,
                        "headers": mcp_headers,
                        "tools": ["*"],
                    }
                },
            ),
            name="WebResearchAgent",
            instructions=(
                "You are a web research assistant. "
                "Use the Fetch MCP server to retrieve and inspect web pages. "
                "Only report information you can verify from the page."
            ),
        ) as agent,
    ):
        session = agent.create_session()
        print("Agent configured")

        prompt = "Fetch https://learn.microsoft.com/en-us/agent-framework/ and summarize the main concepts."
        user_message = Message(role="user", contents=[prompt])
        result = await agent.run(user_message, session=session)
        print(result.text)
        
        print("Second PROMPT ACTION")

        prompt = "Fetch https://www.python.org/ and report the latest Python release shown on the page."
        user_message = Message(role="user", contents=[prompt])
        result = await agent.run(user_message, session=session)
        print(result.text) 

if __name__ == "__main__":
    asyncio.run(main())
    

