from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest
from app.services.customer_service import get_customer
from app.services.gemini_service import ask_gemini
from app.services.business_rules import evaluate_case
from app.services.analytics_service import generate_analytics
from fastapi import Depends
from app.core.auth import get_current_user
from app.core.roles import require_admin
from app.services.dashboard_service import get_dashboard
from app.core.roles import require_admin

from app.services.conversation_service import (
    add_message,
    get_history,
)

router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user)
):

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

    # Save AI reply
    add_message(
        request.customer_id,
        "agent",
        result["reply"]
    )

    # Generate workflow
    workflow = evaluate_case(result)

    # Generate analytics
    analytics = generate_analytics(result)

    # Return complete structured response
    return {
        **result,
        "analytics": analytics,
        "workflow": workflow
    }


@router.get("/history/{customer_id}")
def history(
    customer_id: int,
    current_user=Depends(get_current_user)
):

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

from app.schemas.auth_schema import TokenResponse
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth_service import (
    authenticate_user,
    create_access_token,
)
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
#------------admin/user---------------
@router.get("/admin/users")
def list_users(current_user=Depends(require_admin)):
    return {
        "message": "Welcome Admin!",
        "current_user": current_user
    }
#------------Dashboard--------------
@router.get("/dashboard")
def dashboard(current_user=Depends(require_admin)):
    return get_dashboard()

#---------customer service--------
from app.services.customer_list_service import get_customers
@router.get("/customers")
def customers(
    page: int = 1,
    limit: int = 10,
    name: str = None,
    loan_type: str = None,
    min_overdue: int = None,
    sort_by: str = None,
    current_user=Depends(require_admin),
):
    return get_customers(
        page=page,
        limit=limit,
        name=name,
        loan_type=loan_type,
        min_overdue=min_overdue,
        sort_by=sort_by,
    )
#----------dashboard analytics--------
from app.services.dashboard_analytics import get_dashboard_analytics
@router.get("/analytics")
def analytics(
    current_user=Depends(require_admin)
):
    return get_dashboard_analytics()

#-------report service---------
from app.services.report_service import get_reports
@router.get("/reports")
def reports(
    current_user=Depends(require_admin)
):
    return get_reports()

#---------chart service----------
from app.services.chart_service import get_chart_data
@router.get("/charts")
def charts(
    current_user=Depends(require_admin)
):
    return get_chart_data()