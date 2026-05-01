import json

from app.models.database import Document
from app.models.schemas import DocumentDetail, DocumentOut


def _json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def document_to_out(doc: Document) -> DocumentOut:
    return DocumentOut(
        id=doc.id,
        archive_id=doc.archive_id,
        original_filename=doc.original_filename,
        file_type=doc.file_type,
        file_size=doc.file_size,
        summary=doc.summary or "",
        category=doc.category or "未分类",
        tags=_json_list(doc.tags_json),
        people=_json_list(doc.people_json),
        organizations=_json_list(doc.organizations_json),
        important_dates=_json_list(doc.important_dates_json),
        sensitivity_level=doc.sensitivity_level or "low",
        recommended_folder=doc.recommended_folder or "",
        confidence=doc.confidence or 0.0,
        needs_review=bool(doc.needs_review),
        created_at=doc.created_at,
    )


def document_to_detail(doc: Document) -> DocumentDetail:
    return DocumentDetail(
        **document_to_out(doc).model_dump(),
        extracted_text=doc.extracted_text or "",
        file_path=doc.file_path,
    )
