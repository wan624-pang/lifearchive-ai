from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ArchiveOut(BaseModel):
    id: str
    name: str
    created_at: datetime
    document_count: int

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: str
    archive_id: str
    original_filename: str
    file_type: str
    file_size: int
    summary: str
    category: str
    tags: list[str] = []
    people: list[str] = []
    organizations: list[str] = []
    important_dates: list[str] = []
    sensitivity_level: str
    recommended_folder: str
    confidence: float
    needs_review: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentDetail(DocumentOut):
    extracted_text: str
    file_path: str


class SearchQuery(BaseModel):
    query: str


class SearchResult(BaseModel):
    documents: list[DocumentOut]
    intent: Optional[str] = None
    total: int


class ReportOut(BaseModel):
    id: str
    archive_id: str
    content: dict
    created_at: datetime

    class Config:
        from_attributes = True


class HealthOut(BaseModel):
    status: str
    version: str
