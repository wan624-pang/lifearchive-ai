import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Document
from app.models.schemas import DocumentDetail

router = APIRouter(prefix="/api", tags=["documents"])


@router.get("/documents/{document_id}", response_model=DocumentDetail)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get document detail."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="文件未找到")

    return DocumentDetail(
        id=doc.id,
        archive_id=doc.archive_id,
        original_filename=doc.original_filename,
        file_path=doc.file_path,
        file_type=doc.file_type,
        file_size=doc.file_size,
        extracted_text=doc.extracted_text or "",
        summary=doc.summary or "",
        category=doc.category or "待确认",
        tags=json.loads(doc.tags_json) if doc.tags_json else [],
        people=json.loads(doc.people_json) if doc.people_json else [],
        organizations=json.loads(doc.organizations_json) if doc.organizations_json else [],
        important_dates=json.loads(doc.important_dates_json) if doc.important_dates_json else [],
        sensitivity_level=doc.sensitivity_level or "low",
        recommended_folder=doc.recommended_folder or "",
        confidence=doc.confidence or 0.0,
        needs_review=doc.needs_review,
        created_at=doc.created_at,
    )
