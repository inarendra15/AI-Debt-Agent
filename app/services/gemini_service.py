import json
import traceback

from google import genai

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.core.prompts import SYSTEM_PROMPT
from app.services.conversation_service import get_history
from app.services.workflow_service import apply_ai_workflow

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(customer: dict, customer_message: str) -> dict:
    """
    Generate a structured AI response using:
    - Customer details
    - Conversation history
    - Professional debt collection prompt

    Returns:
        dict
    """

    # Fetch previous conversation
    history = get_history(customer.customer_id)

    conversation = ""

    for msg in history:
        if msg["role"] == "customer":
            conversation += f"Customer: {msg['message']}\n"
        else:
            conversation += f"Agent: {msg['message']}\n"

    # Build prompt
    prompt = f"""
{SYSTEM_PROMPT}

--------------------------------------------------
CUSTOMER INFORMATION
--------------------------------------------------

Customer ID: {customer.customer_id}
Name: {customer.name}
Loan Type: {customer.loan_type}
Loan Amount: {customer.loan_amount}
EMI: {customer.emi}
Outstanding: {customer.outstanding}
Days Overdue: {customer.days_overdue}

--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------

{conversation}

--------------------------------------------------
CURRENT CUSTOMER MESSAGE
--------------------------------------------------

Customer: {customer_message}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = (
                response_text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        elif response_text.startswith("```"):
            response_text = (
                response_text.replace("```", "")
                .strip()
            )

        result = json.loads(response_text)

        required_keys = [
            "reply",
            "intent",
            "sentiment",
            "payment_commitment",
            "followup_days",
            "risk_level",
            "need_human_agent",
        ]

        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing key: {key}")

        apply_ai_workflow(customer.customer_id, result)

        return result

    except json.JSONDecodeError:
        print("\n========== JSON Decode Error ==========")
        print(response_text)
        print("=======================================\n")
        raise

    except Exception:
        print("\n========== Gemini Error ==========")
        traceback.print_exc()
        print("==================================\n")
        raise