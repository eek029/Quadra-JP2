import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base

# Enums
class UserRole(str, Enum):
    MORADOR = "morador"
    PORTEIRO = "porteiro"
    SUBSINDICO = "subsindico"
    SINDICO_GERAL = "sindico_geral"
    SUPERUSER = "superuser"

class UserStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"

class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class EventType(str, Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    REMINDER = "reminder"
    MODIFIED = "modified"
    CANCELLED = "cancelled"
    CHECKIN = "checkin"
    CHECKOUT = "checkout"

# Models
class Tower(Base):
    __tablename__ = "towers"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    users = relationship("User", back_populates="tower")
    units = relationship("Unit", back_populates="tower")

class Unit(Base):
    __tablename__ = "units"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tower_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("towers.id"))
    number: Mapped[str] = mapped_column(String)
    resident_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    tower = relationship("Tower", back_populates="units")
    # resident = relationship("User", foreign_keys=[resident_user_id]) # Circular dependency if not careful

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String)
    unit_number: Mapped[str | None] = mapped_column(String, nullable=True)
    birth_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[UserStatus] = mapped_column(String, default=UserStatus.PENDING, index=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(String, default=UserRole.MORADOR, index=True)
    tower_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("towers.id"), nullable=True)
    auth_provider: Mapped[str] = mapped_column(String, default="google")
    totp_secret: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tower = relationship("Tower", back_populates="users")
    reservations = relationship("Reservation", back_populates="user")
    profile_requests = relationship("ProfileChangeRequest", foreign_keys="ProfileChangeRequest.user_id", back_populates="user")

class Court(Base):
    __tablename__ = "courts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Reservation(Base):
    __tablename__ = "reservations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    court_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courts.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[ReservationStatus] = mapped_column(String, default=ReservationStatus.PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cancelled_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="reservations")
    created_by = relationship("User", foreign_keys=[created_by_user_id])
    events = relationship("ReservationEvent", back_populates="reservation", cascade="all, delete")

class BlackoutWindow(Base):
    __tablename__ = "blackout_windows"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    reason: Mapped[str] = mapped_column(String)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

class ReservationEvent(Base):
    __tablename__ = "reservation_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reservation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reservations.id"))
    type: Mapped[EventType] = mapped_column(String)
    payload: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    reservation = relationship("Reservation", back_populates="events")


class SignupApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class SignupApprovalRequest(Base):
    __tablename__ = "signup_approval_requests"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    tower_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("towers.id"), index=True)
    unit_number: Mapped[str] = mapped_column(String)
    status: Mapped[SignupApprovalStatus] = mapped_column(String, default=SignupApprovalStatus.PENDING, index=True)
    approved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    note: Mapped[str | None] = mapped_column(String, nullable=True)

    applicant = relationship("User", foreign_keys=[applicant_user_id])
    approved_by = relationship("User", foreign_keys=[approved_by_user_id])
    tower = relationship("Tower")

class ProfileChangeRequest(Base):
    __tablename__ = "profile_change_requests"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    field: Mapped[str] = mapped_column(String, default="name")
    old_value: Mapped[str] = mapped_column(String)
    new_value: Mapped[str] = mapped_column(String)
    status: Mapped[RequestStatus] = mapped_column(String, default=RequestStatus.PENDING, index=True)
    approver_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    justification: Mapped[str | None] = mapped_column(String, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="profile_requests")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String)
    entity_type: Mapped[str] = mapped_column(String)
    entity_id: Mapped[str] = mapped_column(String)
    meta: Mapped[dict] = mapped_column("metadata", JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
