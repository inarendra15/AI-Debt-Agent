from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


# =====================================================
# Customer
# =====================================================

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    loan_type = Column(String, nullable=False)

    loan_amount = Column(Float)

    emi = Column(Float)

    outstanding = Column(Float)

    days_overdue = Column(Integer)

    conversations = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete",
    )


# =====================================================
# Conversation
# =====================================================

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
    )

    sender = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    customer = relationship(
        "Customer",
        back_populates="conversations",
    )


# =====================================================
# User
# =====================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    hashed_password = Column(String, nullable=False)

    role = Column(
        String,
        default="agent",
    )


# =====================================================
# Collection Case
# =====================================================

class CollectionCase(Base):
    __tablename__ = "collection_cases"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
    )

    assigned_agent = Column(String, nullable=True)

    status = Column(
        String,
        default="OPEN",
    )

    priority = Column(
        String,
        default="MEDIUM",
    )

    next_followup = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    customer = relationship("Customer")

    # Timeline relationship
    timeline = relationship(
        "TimelineEvent",
        back_populates="case",
        cascade="all, delete",
    )


# =====================================================
# Timeline Events
# =====================================================

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        nullable=False,
    )

    case_id = Column(
        Integer,
        ForeignKey("collection_cases.id"),
        nullable=True,
    )

    event_type = Column(
        String,
        nullable=False,
    )

    description = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    case = relationship(
        "CollectionCase",
        back_populates="timeline",
    )