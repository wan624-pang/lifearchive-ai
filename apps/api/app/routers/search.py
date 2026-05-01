from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Archive
from app.models.schemas import SearchQuery, SearchResult
from app.models.serializers import document_to_out
from app.services.search_service import search_documents

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/archives/{archive_id}/search", response_model=SearchResult)
async def search(archive_id: str, body: SearchQuery, db: Session = Depends(get_db)):
    """Search documents in an archive using natural language."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")

    result = await search_documents(db, archive_id, body.query)
    return SearchResult(
        documents=[document_to_out(doc) for doc in result["documents"]],
        intent=result.get("intent"),
        total=result["total"],
    )
