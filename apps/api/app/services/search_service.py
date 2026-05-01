import json
from sqlalchemy.orm import Session
from app.models.database import Document
from app.services.llm_client import parse_search_intent


async def search_documents(db: Session, archive_id: str, query: str) -> dict:
    """Search documents using keyword matching and metadata filtering."""
    documents = db.query(Document).filter(Document.archive_id == archive_id).all()

    if not documents:
        return {"documents": [], "intent": None, "total": 0}

    # Get categories for intent parsing
    categories = list(set(d.category for d in documents))

    # Parse search intent
    intent = await parse_search_intent(query, categories)

    # Filter documents
    results = []
    for doc in documents:
        score = _score_document(doc, query, intent)
        if score > 0:
            results.append((score, doc))

    # Sort by relevance
    results.sort(key=lambda x: x[0], reverse=True)
    matched_docs = [doc for _, doc in results]

    return {
        "documents": matched_docs,
        "intent": intent.get("intent", "search"),
        "total": len(matched_docs),
    }


def _score_document(doc: Document, query: str, intent: dict) -> float:
    """Score a document's relevance to the search query."""
    score = 0.0
    query_lower = query.lower()

    # Category filter
    category_filter = intent.get("category_filter", "")
    if category_filter and doc.category != category_filter:
        return 0.0

    # Sensitivity filter
    sensitivity_filter = intent.get("sensitivity_filter", "")
    if sensitivity_filter == "high" and doc.sensitivity_level != "high":
        return 0.0

    # Review filter
    if intent.get("intent") == "filter_review":
        if doc.needs_review:
            return 1.0
        return 0.0

    # Date filter
    date_filter = intent.get("date_filter", "")
    if date_filter:
        dates = json.loads(doc.important_dates_json) if doc.important_dates_json else []
        if not any(date_filter in d for d in dates):
            if date_filter not in (doc.extracted_text or ""):
                return 0.0
        else:
            score += 2.0

    # Keyword matching
    searchable = f"{doc.original_filename} {doc.summary} {doc.extracted_text or ''} {doc.category}".lower()
    keywords = intent.get("keywords", [])
    for kw in keywords:
        if kw.lower() in searchable:
            score += 1.0

    # Direct query matching
    if query_lower in searchable:
        score += 3.0

    # Tag matching
    tags = json.loads(doc.tags_json) if doc.tags_json else []
    for tag in tags:
        if query_lower in tag.lower():
            score += 1.5

    return score
