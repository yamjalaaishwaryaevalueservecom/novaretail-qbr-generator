from pathlib import Path
from google.adk.agents import Agent

from tools.data_analysis import analyze_data


PROMPT = Path(__file__).with_name(
    "prompt.md"
).read_text(encoding="utf-8")


def get_novaretail_analysis() -> dict:
    """
    Return verified NovaRetail analysis.
    """
    try:
        return {
            "status": "success",
            "analysis": analyze_data(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


root_agent = Agent(
    name="nova_retail_qbr_agent",
    model="gemini-3.5-flash-lite",
    description=(
        "Creates a structured executive QBR content plan "
        "from verified NovaRetail analysis."
    ),
    instruction=PROMPT,
    tools=[get_novaretail_analysis],
)