import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

CASCADE_ALL_DELETE = "all, delete-orphan"
FK_USERS_ID = "users.id"
FK_REPORTS_ID = "reports.id"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="citizen", nullable=False)  # "citizen" or "admin"
    bio = Column(String, default="", nullable=True)
    location = Column(String, default="", nullable=True)
    latitude = Column(Float, default=-38.737, nullable=False)
    longitude = Column(Float, default=-72.591, nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    notification_radius_km = Column(Float, default=5.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    reports = relationship("Report", back_populates="author", cascade=CASCADE_ALL_DELETE)
    comments = relationship("Comment", back_populates="author", cascade=CASCADE_ALL_DELETE)
    likes = relationship("ReportLike", back_populates="user", cascade=CASCADE_ALL_DELETE)
    notifications = relationship("Notification", back_populates="user", cascade=CASCADE_ALL_DELETE)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    category = Column(String, nullable=False)  # e.g., "vandalism", "pothole", "stray_animals", etc.
    severity = Column(String, nullable=False)  # "low", "medium", "high", "critical"
    status = Column(String, default="abierto", nullable=False)  # "abierto", "derivado_muni", "resuelto", "rechazado"
    municipality_ticket = Column(String, nullable=True)  # Simulated ticket ID (e.g., MUNI-TICKET-xxxxx)
    image_urls = Column(JSON, default=list, nullable=False)  # List of strings
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    author_id = Column(Integer, ForeignKey(FK_USERS_ID), nullable=False)

    author = relationship("User", back_populates="reports")
    likes = relationship("ReportLike", back_populates="report", cascade=CASCADE_ALL_DELETE)
    comments = relationship("Comment", back_populates="report", cascade=CASCADE_ALL_DELETE)


class ReportLike(Base):
    __tablename__ = "report_likes"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey(FK_REPORTS_ID), nullable=False)
    user_id = Column(Integer, ForeignKey(FK_USERS_ID), nullable=False)

    __table_args__ = (UniqueConstraint('report_id', 'user_id', name='_report_user_like_uc'),)

    report = relationship("Report", back_populates="likes")
    user = relationship("User", back_populates="likes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey(FK_REPORTS_ID), nullable=False)
    author_id = Column(Integer, ForeignKey(FK_USERS_ID), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    report = relationship("Report", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(FK_USERS_ID), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "report_status", "new_comment", "municipal_dispatch"
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    related_report_id = Column(Integer, ForeignKey(FK_REPORTS_ID), nullable=True)

    user = relationship("User", back_populates="notifications")
