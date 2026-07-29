from app.database.database import SessionLocal
from app.database.models import StrategyRecommendation


def save_recommendation(customer_id: int, recommendation: dict):

    db = SessionLocal()

    record = StrategyRecommendation(
        customer_id=customer_id,
        recommended_strategy=recommendation["recommended_strategy"],
        risk_level=recommendation["risk_level"],
        confidence=recommendation["confidence"],
        reason=recommendation["reason"],
        next_action=recommendation["next_action"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    return record

def get_recommendations(customer_id: int):

    db = SessionLocal()

    recommendations = (
        db.query(StrategyRecommendation)
        .filter(
            StrategyRecommendation.customer_id == customer_id
        )
        .order_by(
            StrategyRecommendation.created_at.desc()
        )
        .all()
    )

    db.close()

    return recommendations