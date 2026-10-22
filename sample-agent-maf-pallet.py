import asyncio
import os
import deepeval # Import root module
from deepeval.tracing import observe, update_current_trace 

# Correct Microsoft Agent Framework core class imports
from agent_framework import Message
from agent_framework.orchestrations import SequentialBuilder
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.session import PermissionHandler

# 1. CONFIGURE WORKSPACE VIA ENVIRONMENT VARIABLES
# Place your new API key here:
os.environ["CONFIDENT_API_KEY"] = "confident_us_proj_BSQbtkK94zsfBFTlJ1u+cnIupyMk0YMQ2GwV9kBZ0mk="

# 💡 FIXED: Tell the engine to map this file run to "My first project"
os.environ["DEEPEVAL_PROJECT_NAME"] = "My first project"
# 2. LOGIN USING KEY VALUE POINTER (Pass only the string, no keywords)
deepeval.login(os.environ["CONFIDENT_API_KEY"])

@observe()
async def run_monitored_agents(prompt_text: str) -> str:
    """
    Executes a sequential multi-agent pipeline using Microsoft Agent Framework (MAF).
    Streams tracing telemetry safely up to your Confident AI cloud dashboard.
    """
    update_current_trace(
        name="MAF Course Execution",
        tags=["production", "maf-v1"],
        metric_collection="MAF Production Traces"
    )

    # Define Agent 1: The Researcher
    researcher = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Data_Researcher",
        instructions="You are a research assistant. Collect short, bulleted factual data points about the topic.",
    )

    # Define Agent 2: The Emoji Formatter
    formatter = GitHubCopilotAgent(
        default_options=GitHubCopilotOptions(
            on_permission_request=PermissionHandler.approve_all
        ),
        name="Emoji_Formatter",
        instructions="You are an editor. Take the provided text and add context-appropriate emojis to it.",
    )

    print("🧩 Building the Sequential Orchestration Graph...")
    pipeline = SequentialBuilder(participants=[researcher, formatter]).build()

    print(f"🚀 Invoking pipeline with prompt: '{prompt_text}'...")
    response = await pipeline.run(prompt_text)
    
    # Safely extract messages from the outputs array
    pipeline_outputs = response.get_outputs()
    if pipeline_outputs:
        output_text_chunks = []
        for item in pipeline_outputs:
            if hasattr(item, "text") and item.text:
                output_text_chunks.append(str(item.text))
            elif hasattr(item, "content") and item.content:
                output_text_chunks.append(str(item.content))
            elif hasattr(item, "data") and item.data:
                output_text_chunks.append(str(item.data))
            else:
                output_text_chunks.append(str(item))
                
        if output_text_chunks:
            print("📡 Streaming pipeline telemetry events up to Confident AI cloud...")
            # Enforce delay so background telemetry threads don't get terminated early
            await asyncio.sleep(4)
            return "\n".join(output_text_chunks)
            
    return "Pipeline execution finished but returned an empty response."

async def main():
    prompt = "Give me 3 short facts about Mars."
    try:
        final_answer = await run_monitored_agents(prompt)
        print("\n================ FINAL PIPELINE OUTPUT ================")
        print(final_answer)
        print("========================================================\n")
        print("✓ Done! Check your ://confident-ai.com trace dashboard.")
    except Exception as e:
        print(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
