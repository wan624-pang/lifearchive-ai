import os
import json
import shutil
import zipfile
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database import Archive, Document
from app.models.schemas import ArchiveOut, DocumentOut, ReportOut
from app.services.file_parser import extract_zip, parse_file, list_extracted_files
from app.services.llm_client import classify_document
from app.services.report_generator import generate_report

router = APIRouter(prefix="/api", tags=["archives"])


@router.post("/upload", response_model=ArchiveOut)
async def upload_archive(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a ZIP file, extract, parse, classify, and store all documents."""
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="只支持上传 ZIP 文件")

    # Create archive record
    archive = Archive(name=file.filename)
    db.add(archive)
    db.commit()
    db.refresh(archive)

    # Save uploaded ZIP
    upload_dir = os.path.join("uploads", archive.id)
    os.makedirs(upload_dir, exist_ok=True)
    zip_path = os.path.join(upload_dir, file.filename)

    with open(zip_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract and process
    extract_dir = os.path.join(upload_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        extracted_paths = extract_zip(zip_path, extract_dir)
        file_paths = list_extracted_files(extract_dir)

        doc_count = 0
        for fp in file_paths:
            parsed = parse_file(fp)

            # AI classification
            classification = await classify_document(
                filename=parsed.filename,
                file_type=parsed.file_type,
                extracted_text=parsed.extracted_text,
                file_size=parsed.file_size,
            )

            # Create document record
            doc = Document(
                archive_id=archive.id,
                original_filename=parsed.filename,
                file_path=fp,
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
            doc_count += 1

        archive.document_count = doc_count
        db.commit()
        db.refresh(archive)

        return archive

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.get("/archives/{archive_id}", response_model=ArchiveOut)
async def get_archive(archive_id: str, db: Session = Depends(get_db)):
    """Get archive overview."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="资料库未找到")
    return archive


@router.get("/archives/{archive_id}/documents", response_model=list[DocumentOut])
async def get_documents(archive_id: str, db: Session = Depends(get_db)):
    """Get all documents in an archive."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="资料库未找到")
    return archive.documents


@router.get("/archives/{archive_id}/report", response_model=ReportOut)
async def get_report(archive_id: str, db: Session = Depends(get_db)):
    """Generate and return the archive report."""
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="资料库未找到")

    report_content = await generate_report(db, archive_id)

    # Get the latest report
    from app.models.database import Report
    report = db.query(Report).filter(Report.archive_id == archive_id).order_by(Report.created_at.desc()).first()

    return ReportOut(
        id=report.id,
        archive_id=archive_id,
        content=report_content,
        created_at=report.created_at,
    )


@router.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}


@router.post("/demo")
async def load_demo(db: Session = Depends(get_db)):
    """Load sample archive data for demo."""
    # Try multiple paths to find the sample_archive directory
    candidates = [
        os.path.normpath(os.path.join(os.getcwd(), "..", "..", "examples", "sample_archive")),
        os.path.join(os.getcwd(), "examples", "sample_archive"),
        os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "examples", "sample_archive")),
    ]
    sample_dir = None
    for candidate in candidates:
        if os.path.exists(candidate):
            sample_dir = candidate
            break

    if not sample_dir:
        raise HTTPException(status_code=404, detail="示例数据目录未找到")

    if not os.path.exists(sample_dir):
        raise HTTPException(status_code=404, detail=f"示例数据目录未找到: {sample_dir}")

    # Create zip from sample files
    archive = Archive(name="示例资料库 - 张三的个人档案")
    db.add(archive)
    db.commit()
    db.refresh(archive)

    upload_dir = os.path.join("uploads", archive.id)
    os.makedirs(upload_dir, exist_ok=True)

    # Process each sample file directly
    doc_count = 0
    for fname in os.listdir(sample_dir):
        fpath = os.path.join(sample_dir, fname)
        if not os.path.isfile(fpath):
            continue

        parsed = parse_file(fpath)

        classification = await classify_document(
            filename=parsed.filename,
            file_type=parsed.file_type,
            extracted_text=parsed.extracted_text,
            file_size=parsed.file_size,
        )

        doc = Document(
            archive_id=archive.id,
            original_filename=parsed.filename,
            file_path=fpath,
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
        doc_count += 1

    archive.document_count = doc_count
    db.commit()
    db.refresh(archive)

    return archive
