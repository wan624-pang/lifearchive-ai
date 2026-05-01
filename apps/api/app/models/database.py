from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.db.database import Base


def gen_id():
    return str(uuid.uuid4())[:12]


class Archive(Base):
    __tablename__ = "archives"

    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    document_count = Column(Integer, default=0)

    documents = relationship("Document", back_populates="archive", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="archive", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=gen_id)
    archive_id = Column(String, ForeignKey("archives.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, default=0)
    extracted_text = Column(Text, default="")
    summary = Column(Text, default="")
    category = Column(String, default="待确认")
    tags_json = Column(Text, default="[]")
    people_json = Column(Text, default="[]")
    organizations_json = Column(Text, default="[]")
    important_dates_json = Column(Text, default="[]")
    sensitivity_level = Column(String, default="low")
    recommended_folder = Column(String, default="")
    confidence = Column(Float, default=0.0)
    needs_review = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    archive = relationship("Archive", back_populates="documents")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=gen_id)
    archive_id = Column(String, ForeignKey("archives.id"), nullable=False)
    content_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    archive = relationship("Archive", back_populates="reports")
