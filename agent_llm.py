import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from agent_core import evaluate_and_checkout, audit_log, log_action

load_dotenv()

# Load catalog
with open("catalog.json") as f:
    CATALOG = json.load(f)

# Initialize official Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define Python Functions for Gemini Tools
def search_catalog(query: str) -> str:
    """Searches the product catalog based on user query and returns matching items."""
    log_action("SEARCH_CATALOG", f"Gemini Tool Call searching for: '{query}'", "EXECUTING")
    results = [item for item in CATALOG if query.lower() in item['name'].lower() or query.lower() in item['category'].lower()]
    if not results:
        results = CATALOG
    log_action("SEARCH_CATALOG", f"Found {len(results)} items.", "SUCCESS")
    return json.dumps(results)

def process_checkout(product_ids: list[str], max_budget: float) -> str:
    """Validates user budget gating and creates a Razorpay payment order."""
    selected_items = [p for p in CATALOG if p['id'] in product_ids]
    if not selected_items:
        return json.dumps({"status": "FAILED", "reason": "No valid products found"})
    response = evaluate_and_checkout(selected_items, max_budget)
    return json.dumps(response)

class RealGeminiAgentExecutor:
    def invoke(self, inputs: dict):
        user_input = inputs["input"]
        
        system_instruction = (
            "You are an Agentic Commerce Sales Engine.\n"
    "1. Use search_catalog to find matching products for the user's request.\n"
    "2. If the user only asks for a primary item, show the primary item price and SUGGEST a cross-sell/upsell accessory verbally. DO NOT add the cross-sell item to process_checkout unless the user explicitly confirms or agrees to add it.\n"
    "3. When suggesting a cross-sell item, briefly explain the value context (e.g., 'Pairs well with a mechanical keyboard for long typing sessions').\n"
    "4. Never say 'Payment Successful' upon order creation. Say 'Razorpay Order Created: {order_id}. Ready for checkout!'\n"
    "5. Only pass the product IDs to process_checkout that the user has explicitly requested or confirmed to buy."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[search_catalog, process_checkout],
            temperature=0
        )

        # Call Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=user_input,
            config=config
        )

        # Handle Function Calling
        if response.function_calls:
            function_call = response.function_calls[0]
            name = function_call.name
            args = function_call.args

            if name == "search_catalog":
                result = search_catalog(args.get("query", ""))
            elif name == "process_checkout":
                result = process_checkout(
                    args.get("product_ids", []),
                    float(args.get("max_budget", 99999))
                )

            # Follow up with tool result
            followup_response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=[
                    user_input,
                    response.candidates[0].content,
                    types.Content(
                        parts=[
                            types.Part.from_function_response(
                                name=name,
                                response={"result": result}
                            )
                        ]
                    )
                ],
                config=config
            )
            return {"output": followup_response.text}

        return {"output": response.text}

agent_executor = RealGeminiAgentExecutor()