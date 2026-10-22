import asyncio
from agent_framework.orchestrations import SequentialBuilder
from agent_framework import Message
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.session import PermissionHandler
from agent_framework.devui import serve 

async def build_pipeline():
    researcher = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Researcher_Agent", # Use underscores or simple text strings
        instructions="You Are Helpful Weather Assistant.",
    )

    print("Researcher configured")
    
    formatter = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Formatter_Agent",
        instructions="You Are a Formatter Agent that adds emojis to the response.",
    )

    #  FIXED: Pass participants directly into the constructor
    pipeline = SequentialBuilder(participants=[researcher, formatter]).build()
    return pipeline

if __name__ == "__main__":
    # Resolve the orchestration graph asynchronously
    pipeline_instance = asyncio.run(build_pipeline())
    
    # Run the DevUI outside the asyncio.run block to prevent loop collisions
    print("Starting MAF DevUI on localhost...")
    # 💡 BYPASS AUTH TOKEN PROMPT: Force auth_enabled to False
    serve(entities=[pipeline_instance], auto_open=True, auth_enabled=False)