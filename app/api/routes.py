from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.customer_service import get_customer
from app.services.gemini_service import ask_gemini
from app.services.business_rules import evaluate_case
from app.services.conversation_service import (
    add_message,
    get_history,
)

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

    # Fetch customer
    customer = get_customer(request.customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Save customer message
    add_message(
        request.customer_id,
        "customer",
        request.message
    )

    # Get AI response
    result = ask_gemini(
        customer,
        request.message
    )

    # Save only the AI reply in conversation history
    add_message(
        request.customer_id,
        "agent",
        result["reply"]
    )

    # Return the complete structured JSON
    workflow = evaluate_case(result)

    return {
    **result,
    "workflow": workflow
    }


@router.get("/history/{customer_id}")
def history(customer_id: int):

    customer = get_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "customer_id": customer_id,
        "history": get_history(customer_id)
    }