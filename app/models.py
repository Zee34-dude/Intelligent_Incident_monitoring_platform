# models.py
from datetime import datetime, timedelta, timezone
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Enum as SqlEnum
from app.database import Base
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False
        )
class User(Base,TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_code = Column(String, nullable=True)
    verification_expires_at = Column(DateTime, nullable=True)
    role = Column(String, default="user")
    organizations = relationship("Organization", back_populates="users")



class EmailVerification(Base,TimestampMixin):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    code = Column(String, index=True)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    
    
class Organization(Base,TimestampMixin):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # Owner relationship (separate from members)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email=Column(String,unique=True,index=True)
    users = relationship(
        "User",
        back_populates="organizations",
    )

    services = relationship(
        "Service",
        back_populates="organizations",
        cascade="all, delete-orphan"
    )

    incidents = relationship(
        "Incident",
        back_populates="organizations",
        cascade="all, delete-orphan"
    )
class IncidentStatus(Enum):
    OPEN='OPEN'
    INVESTIGATING='INVESTIGATING'
    RESOLVED='RESOLVED'
    
class Incident(Base,TimestampMixin):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SqlEnum(IncidentStatus), default="OPEN")  
    severity = Column(String, nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    organization_id = Column(
        Integer, 
        ForeignKey("organizations.id"),
        nullable=False
    )
    resolved_at=Column(DateTime, nullable=True)
    acknowledged_at=Column(DateTime,nullable=True)
    service_id=Column(Integer,ForeignKey("services.id"))
    started_at=Column(DateTime, nullable=True)
    organizations = relationship("Organization", back_populates="incidents")
    services=relationship("Service",back_populates="incidents")
    investigated_by=Column(Integer,ForeignKey("users.id"))
    investigation_note=Column(String,nullable=True)
    
class Service(Base,TimestampMixin):
    __tablename__='services'
    id=Column(Integer,primary_key=True,index=True)
    website_name=Column(String,index=True)
    organization_Id=Column(Integer,ForeignKey('organizations.id'),nullable=False)
    status=Column(String,default='UP')
    url=Column(String)
    last_checked_at = Column(DateTime, nullable=True)
    last_status = Column(String, nullable=True)
    response_time = Column(Integer, nullable=True)  # ms
    error_reason = Column(String, nullable=True)
    organizations=relationship('Organization',back_populates='services')
    incidents = relationship(
        "Incident",
        back_populates="services",
        cascade="all, delete-orphan"
    )