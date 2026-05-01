import json
from sqlalchemy.orm import Session
from app.models.database import Document, Report
from app.services.llm_client import generate_archive_report


async def generate_report(db: Session, archive_id: str) -> dict:
    """Generate a full archive report from all documents."""
    documents = db.query(Document).filter(Document.archive_id == archive_id).all()

    if not documents:
        return _empty_report()

    # Build stats
    category_stats: dict[str, int] = {}
    all_dates: list[str] = []
    high_sensitivity_count = 0
    needs_review_count = 0
    doc_dicts = []

    for doc in documents:
        category_stats[doc.category] = category_stats.get(doc.category, 0) + 1
        if doc.sensitivity_level == "high":
            high_sensitivity_count += 1
        if doc.needs_review:
            needs_review_count += 1
        dates = json.loads(doc.important_dates_json) if doc.important_dates_json else []
        all_dates.extend(dates)
        doc_dicts.append({
            "filename": doc.original_filename,
            "category": doc.category,
            "sensitivity_level": doc.sensitivity_level,
            "summary": doc.summary,
        })

    # Deduplicate and sort dates
    unique_dates = sorted(set(all_dates))

    # Generate report via AI or mock
    report_content = await generate_archive_report(
        documents=doc_dicts,
        category_stats=category_stats,
        important_dates=unique_dates,
        high_sensitivity_count=high_sensitivity_count,
        needs_review_count=needs_review_count,
    )

    # Save to DB
    report = Report(
        archive_id=archive_id,
        content_json=json.dumps(report_content, ensure_ascii=False),
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return report_content


def _empty_report() -> dict:
    return {
        "overview": "资料库为空，请上传文件后重新生成报告。",
        "category_summary": [],
        "important_timeline": [],
        "missing_materials": [],
        "risk_notes": [],
        "handoff_checklist": [],
        "next_actions": ["上传文件开始整理"],
    }
