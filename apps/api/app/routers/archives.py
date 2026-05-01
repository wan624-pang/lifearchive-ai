import json
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Archive, Document
from app.models.schemas import ArchiveOut, DocumentOut, ReportOut
from app.models.serializers import document_to_out
from app.services.file_parser import extract_zip, list_extracted_files, parse_file
from app.services.llm_client import classify_document
from app.services.report_generator import generate_report

router = APIRouter(prefix="/api", tags=["archives"])


def _safe_upload_filename(filename: str | None) -> str:
    safe_filename = os.path.basename(filename or "")
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Invalid upload filename")
    if not safe_filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are supported")
    return safe_filename


async def _create_document(db: Session, archive_id: str, file_path: str) -> int:
    parsed = parse_file(file_path)
    classification = await classify_document(
        filename=parsed.filename,
        file_type=parsed.file_type,
        extracted_text=parsed.extracted_text,
        file_size=parsed.file_size,
    )
    doc = Document(
        archive_id=archive_id,
        original_filename=parsed.filename,
        file_path=file_path,
        file_type=parsed.file_type,
        file_size=parsed.file_size,
        extracted_text=parsed.extracted_text[:10000],
        summary=classification.summary,
        category=classification.category,
        tags_json=json.dumps(classification.tags, ensure_ascii=False),
        people_json=json.dumps(classification.people, ensure_ascii=False),
        organizations_json=json.dumps(classification.organizations, ensure_ascii=False),
        important_dates_json=json.dumps(classification.important_dates, ensure_ascii=False),
        sensitivity_level=classification.sensitivity_level,
        recommended_folder=classification.recommended_folder,
        confidence=classification.confidence,
        needs_review=classification.needs_review,
    )
    db.add(doc)
    return 1


@router.post("/upload", response_model=ArchiveOut)
async def upload_archive(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a ZIP file, extract, parse, classify, and store all documents."""
    safe_filename = _safe_upload_filename(file.filename)

    archive = Archive(name=safe_filename)
    db.add(archive)
    db.commit()
    db.refresh(archive)

    upload_dir = os.path.join("uploads", archive.id)
    os.makedirs(upload_dir, exist_ok=True)
    zip_path = os.path.join(upload_dir, safe_filename)

    with open(zip_path, "wb") as f:
        f.write(await file.read())

    extract_dir = os.path.join(upload_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        extract_zip(zip_path, extract_dir)
        file_paths = list_extracted_files(extract_dir)

        doc_count = 0
        for file_path in file_paths:
            doc_count += await _create_document(db, archive.id, file_path)

        archive.document_count = doc_count
        db.commit()
        db.refresh(archive)
        return archive
    except Exception as exc:
        db.delete(archive)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Archive processing failed: {exc}") from exc


@router.get("/archives/{archive_id}", response_model=ArchiveOut)
async def get_archive(archive_id: str, db: Session = Depends(get_db)):
    """Get archive overview."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")
    return archive


@router.get("/archives/{archive_id}/documents", response_model=list[DocumentOut])
async def get_documents(archive_id: str, db: Session = Depends(get_db)):
    """Get all documents in an archive."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")
    return [document_to_out(doc) for doc in archive.documents]


@router.get("/archives/{archive_id}/report", response_model=ReportOut)
async def get_report(archive_id: str, db: Session = Depends(get_db)):
    """Generate and return the archive report."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")

    report_content = await generate_report(db, archive_id)

    from app.models.database import Report

    report = (
        db.query(Report)
        .filter(Report.archive_id == archive_id)
        .order_by(Report.created_at.desc())
        .first()
    )
    if not report:
        raise HTTPException(status_code=500, detail="Report generation failed")

    return ReportOut(
        id=report.id,
        archive_id=archive_id,
        content=report_content,
        created_at=report.created_at,
    )


@router.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}


@router.post("/demo", response_model=ArchiveOut)
async def load_demo(db: Session = Depends(get_db)):
    """Load sample archive data for demo."""
    candidates = [
        os.path.normpath(os.path.join(os.getcwd(), "..", "..", "examples", "sample_archive")),
        os.path.join(os.getcwd(), "examples", "sample_archive"),
        os.path.normpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "..",
                "..",
                "..",
                "..",
                "examples",
                "sample_archive",
            )
        ),
    ]
    sample_dir = next((candidate for candidate in candidates if os.path.exists(candidate)), None)
    if not sample_dir:
        raise HTTPException(status_code=404, detail="Sample archive directory not found")

    archive = Archive(name="Sample archive")
    db.add(archive)
    db.commit()
    db.refresh(archive)

    try:
        doc_count = 0
        for fname in os.listdir(sample_dir):
            file_path = os.path.join(sample_dir, fname)
            if os.path.isfile(file_path):
                doc_count += await _create_document(db, archive.id, file_path)

        archive.document_count = doc_count
        db.commit()
        db.refresh(archive)
        return archive
    except Exception as exc:
        db.delete(archive)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Demo loading failed: {exc}") from exc
