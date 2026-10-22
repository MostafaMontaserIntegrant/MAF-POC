import asyncio

from agent_framework import tool, AgentMiddleware
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot import PermissionHandler
from copilot.generated.rpc import PermissionDecisionApproveOnce, PermissionDecisionReject
from fastapi import security



class SecurityMiddleware(AgentMiddleware):
    def __init__(self):
        super().__init__()
        self.current_input = ""

    async def process(self, context, call_next):
        # Check for banned words
        banned_words = ["hack", "password", "secret"]
        if any(word in self.current_input.lower() for word in banned_words):
            raise ValueError("Request blocked: sensitive content detected")

        print(f"[SECURITY] Input: {self.current_input}")

        await call_next()
        print(f"[SECURITY] Response sent: {context.result}")
    
    


async def main():
    security = SecurityMiddleware()
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all,
        ),
        name="Secure-agent",
        middleware=[security],
        instructions="You are a helpful assistant.",
    )
    print("Agent configured")
    try:
        user_input = input("Enter your prompt: ")
        security.current_input = user_input
        result = await agent.run(user_input)
        print(f"\nResponse: {getattr(result, 'text', str(result))}")
    except ValueError as e:
        print(f"\n {e}")


if __name__ == "__main__":
    asyncio.run(main())