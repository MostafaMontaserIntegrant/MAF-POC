import asyncio
import threading
import uvicorn 
import time

from agent_framework import Message
from agent_framework.a2a import A2AExecutor 
from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
from copilot.session import PermissionHandler

FOUNDER_PORT=9999
FOUNDER_URL=f"http://localhost:{FOUNDER_PORT}"



def start_founder():
    from a2a.server.request_handlers import DefaultRequestHandler
    from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
    from a2a.server.tasks import InMemoryTaskStore
    from a2a.types import AgentCapabilities, AgentCard, AgentInterface
    from starlette.applications import Starlette

    # 1. Create the AI agent with its personality
    agent = GitHubCopilotAgent(
        name="Founder Mostafa",
        instructions=(
            "You are Mostafa, a hyper-confident startup founder. "
            "When given a theme, invent a startup with: "
            "a catchy name, a one-line elevator pitch, "
            "a business model, and a funding ask (e.g. '$2M seed'). "
            "Be creative and slightly over-the-top. Keep it under 100 words."
        ),
    )

    # 2. Define the Agent Card — this is how other agents discover you
    card = AgentCard(
        name="Founder Mostafa",
        description="A startup founder who pitches bold ideas.",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[
            AgentInterface(url=f"{FOUNDER_URL}/", protocol_binding="JSONRPC")
        ],
        skills=[],
    )

    # Wire the agent into the A2A request handler and HTTP routes.
    handler = DefaultRequestHandler(
        agent_executor=A2AExecutor(agent),
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )

    app = Starlette(
        routes=[
            *create_agent_card_routes(card),
            *create_jsonrpc_routes(handler, rpc_url="/"),
        ]
    )

    # 4. Start serving on port 9999
    uvicorn.run(app, host="0.0.0.0", port=FOUNDER_PORT, log_level="warning")


# ─────────────────────────────────────────────────────────────
# PART 2: The VC Shark Agent  (runs as an A2A client)
#
# This agent doesn't need a server — it just calls the Founder
# over A2A, gets the pitch, and reviews it locally.
# ────────────────────────
    
    
    
async def run_shark_tank():
    from agent_framework.a2a import A2AAgent           # Wraps a remote A2A agent as a client
    shark = GitHubCopilotAgent(
            default_options=GitHubCopilotOptions(
                on_permission_request=PermissionHandler.approve_all,   
            ),
            name="Shark Agent",
            instructions=(
            "You are Shark, a ruthless but fair VC investor. "
            "You will be given a startup pitch. Evaluate it:\n"
            "- Verdict: FUND or PASS\n"
            "- If FUND: state your offer (amount for equity %)\n"
            "- If PASS: state the fatal flaw\n"
            "- End with a witty one-liner\n"
            "Be sharp and dramatic. Keep it under 80 words."
          ),
        )   
    themes= ["Pitch me a cryptocurrency startup"]
    
    
    #connect to the Founder's A2A Server
    async with A2AAgent(name="Founder Mostafa", url=FOUNDER_URL) as founder:
        for i,theme in enumerate(themes):
            print(f"\n{'━' * 55}")
            print(f"  🎬  ROUND {i}")
            print(f"{'━' * 55}")
            print(f"📣  Theme: {theme}\n")
            # Step A — Send the theme to the Founder via A2A
            founder_response = await founder.run(theme)

            # Extract text from the A2A response messages
            pitch = ""
            for msg in founder_response.messages:
                if msg.text:
                    pitch += msg.text
            print(f"🚀  Founder Mostafa:\n{pitch}\n")

            # Step B — Feed the pitch to the Shark for evaluation
            review = await shark.run(
                f"A founder just pitched you this startup:\n\n{pitch}"
            )
            print(f"🦈  Shark Agent:\n{review}")

print(f"\n{'━' * 55}")
print("  🎬  THAT'S A WRAP!")
print(f"{'━' * 55}\n")
    
    
    
    
if __name__ == "__main__":
    # Start the Founder as a background thread (daemon=True means
    # it dies when the main process exits)
    print(f"🚀 Starting Founder Mostafa on port {FOUNDER_PORT}...")
    threading.Thread(target=start_founder, daemon=True).start()

    # Give the server a few seconds to start up
    time.sleep(3)
    print("✅ Founder ready! Shark Agent entering the tank...\n")

    # Run the async conversation
    asyncio.run(run_shark_tank())