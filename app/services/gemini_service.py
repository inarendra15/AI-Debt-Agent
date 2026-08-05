import json
import time
import traceback

from google import genai
from google.genai.errors import ServerError

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.core.prompts import SYSTEM_PROMPT
from app.services.conversation_service import get_history
from app.services.workflow_service import apply_ai_workflow


# ==========================================================
# Gemini Configuration
# ==========================================================

client = genai.Client(api_key=GEMINI_API_KEY)

# Backup model used when the primary model is temporarily
# unavailable because of high demand.
FALLBACK_MODEL_NAME = "gemini-3.1-flash-lite"

MAX_RETRIES = 2
RETRY_DELAY = 2


# ==========================================================
# Common Gemini Request Handler
# ==========================================================

def generate_with_fallback(prompt: str):
    """
    Send a request to Gemini with automatic retry and
    fallback-model support.

    Flow:
        Primary model
            -> retry on 503
            -> fallback model
            -> retry on 503
    """

    models = [
        MODEL_NAME,
        FALLBACK_MODEL_NAME,
    ]

    last_error = None

    for model in models:

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                print(
                    f"\nGemini request: "
                    f"model={model}, "
                    f"attempt={attempt}/{MAX_RETRIES}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                print(
                    f"Gemini request successful "
                    f"using model: {model}"
                )

                return response

            except ServerError as error:

                last_error = error

                print(
                    f"Gemini server error "
                    f"(model={model}, attempt={attempt}): "
                    f"{error}"
                )

                # Retry the same model
                if attempt < MAX_RETRIES:

                    print(
                        f"Retrying in {RETRY_DELAY} seconds..."
                    )

                    time.sleep(RETRY_DELAY)

                else:

                    print(
                        f"Model {model} unavailable. "
                        f"Trying fallback model..."
                    )

    # All models failed
    print(
        "\nAll configured Gemini models are unavailable."
    )

    if last_error:
        raise last_error

    raise RuntimeError(
        "Gemini request failed without a specific error."
    )


# ==========================================================
# Clean Gemini JSON Response
# ==========================================================

def parse_json_response(response) -> dict:
    """
    Convert Gemini response text into a Python dictionary.
    Also removes Markdown JSON code blocks when Gemini
    includes them.
    """

    if not response or not response.text:
        raise ValueError("Gemini returned an empty response.")

    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = (
            response_text
            .replace("```json", "", 1)
            .replace("```", "")
            .strip()
        )

    elif response_text.startswith("```"):
        response_text = (
            response_text
            .replace("```", "")
            .strip()
        )

    return json.loads(response_text)


# ==========================================================
# AI Customer Conversation
# ==========================================================

def ask_gemini(customer, customer_message: str) -> dict:
    """
    Generate a structured AI response for debt collection
    conversations.

    Uses:
        - Customer information
        - Previous conversation history
        - Debt collection system prompt
        - Gemini retry/fallback mechanism
    """

    # ------------------------------------------------------
    # Fetch Conversation History
    # ------------------------------------------------------

    history = get_history(customer.customer_id)

    conversation = ""

    for msg in history:

        if msg["role"] == "customer":

            conversation += (
                f"Customer: {msg['message']}\n"
            )

        else:

            conversation += (
                f"Agent: {msg['message']}\n"
            )

    # ------------------------------------------------------
    # Build Gemini Prompt
    # ------------------------------------------------------

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

        # --------------------------------------------------
        # Gemini Request
        # --------------------------------------------------

        response = generate_with_fallback(prompt)

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        result = parse_json_response(response)

        # --------------------------------------------------
        # Validate Required Fields
        # --------------------------------------------------

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

                raise ValueError(
                    f"Missing key in Gemini response: {key}"
                )

        # --------------------------------------------------
        # Apply AI Workflow
        # --------------------------------------------------

        apply_ai_workflow(
            customer.customer_id,
            result,
        )

        return result

    except json.JSONDecodeError as error:

        print(
            "\n========== Gemini JSON Decode Error =========="
        )

        print(error)

        print(
            "==============================================\n"
        )

        raise

    except Exception:

        print(
            "\n========== Gemini Conversation Error =========="
        )

        traceback.print_exc()

        print(
            "================================================\n"
        )

        raise


# ==========================================================
# AI Strategy Recommendation
# ==========================================================

def recommend_collection_strategy(context: dict) -> dict:
    """
    Analyze complete customer information and recommend
    the best debt collection strategy.

    Context can contain:
        - Customer profile
        - Collection case
        - Conversation history
        - Timeline events
    """

    # ------------------------------------------------------
    # Convert Context To JSON
    # ------------------------------------------------------

    context_json = json.dumps(
        context,
        indent=2,
        default=str,
    )

    # ------------------------------------------------------
    # Strategy Prompt
    # ------------------------------------------------------

    prompt = f"""
You are an expert AI Debt Collection Advisor.

Your task is to analyze the customer's complete debt
collection profile and recommend the most appropriate
collection strategy.

Consider:

1. Outstanding debt
2. Days overdue
3. Loan information
4. Previous conversations
5. Customer payment commitments
6. Customer sentiment
7. Existing collection case status
8. Case priority
9. Previous timeline events
10. Escalation history

--------------------------------------------------
CUSTOMER COLLECTION CONTEXT
--------------------------------------------------

{context_json}

--------------------------------------------------
INSTRUCTIONS
--------------------------------------------------

Recommend the most appropriate debt collection strategy.

Return ONLY valid JSON.

Do not include Markdown.
Do not include explanations outside the JSON.

Required JSON format:

{{
    "recommended_strategy": "",
    "risk_level": "",
    "confidence": 0,
    "reason": "",
    "next_action": ""
}}
"""

    try:

        # --------------------------------------------------
        # Gemini Request
        # --------------------------------------------------

        response = generate_with_fallback(prompt)

        # --------------------------------------------------
        # Parse Response
        # --------------------------------------------------

        result = parse_json_response(response)

        # --------------------------------------------------
        # Validate Required Fields
        # --------------------------------------------------

        required_keys = [
            "recommended_strategy",
            "risk_level",
            "confidence",
            "reason",
            "next_action",
        ]

        for key in required_keys:

            if key not in result:

                raise ValueError(
                    f"Missing key in strategy response: {key}"
                )

        return result

    except json.JSONDecodeError as error:

        print(
            "\n========== Strategy JSON Error =========="
        )

        print(error)

        print(
            "=========================================\n"
        )

        raise

    except Exception:

        print(
            "\n========== Strategy Recommendation Error =========="
        )

        traceback.print_exc()

        print(
            "===================================================\n"
        )

        raise