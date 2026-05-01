import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Archive
from app.models.schemas import SearchQuery, SearchResult, DocumentOut
from app.services.search_service import search_documents

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/archives/{archive_id}/search", response_model=SearchResult)
async def search(archive_id: str, body: SearchQuery, db: Session = Depends(get_db)):
    """Search documents in an archive using natural language."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="资料库未找到")

    result = await search_documents(db, archive_id, body.query)

    # Convert documents to output schema
    doc_outs = []
    for doc in result["documents"]:
        doc_outs.append(DocumentOut(
            id=doc.id,
            archive_id=doc.archive_id,
            original_filename=doc.original_filename,
            file_type=doc.file_type,
            file_size=doc.file_size,
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
        ))

    return SearchResult(
        documents=doc_outs,
        intent=result.get("intent"),
        total=result["total"],
    )
