import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def clean_json_response(response_text):
    """
    Extract valid JSON from Gemini response, removing markdown formatting.
    """
    # Remove markdown code block markers if present
    if response_text.startswith("```json"):
        response_text = response_text.strip()[7:-3].strip()  # Remove ```json ... ```
    elif response_text.startswith("```"):
        response_text = response_text.strip()[3:-3].strip()  # Remove ``` ... ```

    # Now find the first `{` and trim to last `}` to avoid extra explanation
    start = response_text.find('{')
    end = response_text.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("No valid JSON object found.")

    return response_text[start:end+1]

def parse_intent(user_input):
    prompt = f"""
You are an AI assistant for OpenStack cloud operations. 
Detect the intent and return a structured JSON with this exact format:

{{
  "intent": "<one of: create_vm, delete_vm, create_volume, delete_volume, resize_vm, usage, unknown>",
  "entities": {{
    "name": "<resource_name>",
    "flavor": "<flavor_name>",
    "size": "<size_value>",
    "type": "<vm|volume>"
  }},
  "requires_confirmation": true,
  "confirmation_message": "<confirmation message>"
}}

Only return the raw JSON. No explanation or extra text.

User Instruction: {user_input}
"""

    try:
        response = model.generate_content(prompt)
        print("GEMINI RAW RESPONSE:\n", response.text)
        cleaned_json = clean_json_response(response.text)
        return json.loads(cleaned_json)
    except Exception as e:
        print("ERROR PARSING RESPONSE:", e)
        return {
            "intent": "unknown",
            "entities": {},
            "requires_confirmation": False,
            "confirmation_message": "Could not parse the request."
        }
