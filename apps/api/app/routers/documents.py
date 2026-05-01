from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Document
from app.models.schemas import DocumentDetail
from app.models.serializers import document_to_detail

router = APIRouter(prefix="/api", tags=["documents"])


@router.get("/documents/{document_id}", response_model=DocumentDetail)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get document detail."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return document_to_detail(doc)
