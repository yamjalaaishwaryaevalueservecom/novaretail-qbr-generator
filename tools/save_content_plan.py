import json
from pathlib import Path


# Paste the ADK response JSON here
with open("adk_response.json", "r", encoding="utf-8") as f:
    response = json.load(f)

# Extract the JSON string returned by Gemini
json_text = response["content"]["parts"][0]["text"]

# Convert string to Python object
content_plan = json.loads(json_text)

# Create output folder if missing
Path("output").mkdir(exist_ok=True)

# Save clean JSON
with open(
    "output/content_plan.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        content_plan,
        f,
        indent=2,
        ensure_ascii=False
    )

print("✅ Saved: output/content_plan.json")