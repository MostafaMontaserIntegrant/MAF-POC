import asyncio
from typing import Any
from agent_framework import   AgentSession, Message, SessionContext
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from agent_framework import ContextProvider

# 1. Use the official handler class provided by the underlying copilot package
from copilot.session import PermissionHandler

# 1. Properly inherit from ContextProvider
class FormattingMemoryProvider(ContextProvider):
    def __init__(self):
        super().__init__("formatting_memory_provider")

    # The framework passes these exact keyword-only arguments using *
    async def before_run(
        self, 
        *, 
        agent: Any, 
        session: AgentSession | None, 
        context: SessionContext, 
        state: dict[str, Any]
    ) -> None:
        # Instead of returning a value, mutate the provided context object directly
        context.extend_instructions(
            self.source_id, 
            "CRITICAL RULE: You must always output your response as bullet points with emojis."
        )

async def main():
    # 2. Assign the built-in approve_all helper method directly
    agent = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Memory Agent",
        instructions="You Are a Memory Helpful Assistant.",
        context_providers=[FormattingMemoryProvider()]
    )
    print("Agent configured")
    prompt = (
            "Give Me some points for microsoft agent framework in AI"
            )

    user_message1= Message(
        role="user",
        contents= [prompt]
        )
  
        
    result = await agent.run(user_message1)
    print(result.text)



if __name__ == "__main__":
    asyncio.run(main())
    

