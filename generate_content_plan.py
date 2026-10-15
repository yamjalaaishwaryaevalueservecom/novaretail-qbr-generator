import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env first
ENV_PATH = (
    Path(__file__).parent
    / "nova_retail_agent"
    / ".env"
)

load_dotenv(ENV_PATH)

print(
    "API Key Found:",
    bool(os.getenv("GOOGLE_API_KEY"))
)

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError(
        "GOOGLE_API_KEY not found in .env"
    )

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from nova_retail_agent.agent import root_agent


async def main():

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name="novaretail",
        user_id="aishwarya",
        session_id="session1"
    )

    runner = Runner(
        agent=root_agent,
        app_name="novaretail",
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
                    "Call get_novaretail_analysis. "
                    "Generate the complete five-slide executive QBR content plan. "
                    "Return only valid JSON."
                )
            )
        ]
    )

    final_response = None

    async for event in runner.run_async(
        user_id="aishwarya",
        session_id=session.id,
        new_message=message
    ):

        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
        ):
            final_response = event.content.parts[0].text

    if not final_response:
        raise Exception(
            "No response received from ADK"
        )

    content_plan = json.loads(final_response)
    # Prevent overwriting valid content with errors

    if "slide1" not in content_plan:

        print(
            "[WARNING] Invalid content received from ADK."
        )

        print(content_plan)

        return
    Path("output").mkdir(
        exist_ok=True
    )

    output_file = (
        Path("output")
        / "content_plan.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            content_plan,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"✅ Saved: {output_file}"
    )


if __name__ == "__main__":
    asyncio.run(main())