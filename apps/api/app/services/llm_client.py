import os
import json
import logging
from typing import Optional

from app.services.ai_classifier import (
    classify_document_mock,
    ClassificationResult,
    result_to_dict,
)

logger = logging.getLogger(__name__)

AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")


async def classify_document(
    filename: str,
    file_type: str,
    extracted_text: str,
    file_size: int,
) -> ClassificationResult:
    """Classify a document using configured AI provider."""
    if AI_PROVIDER == "mock":
        return classify_document_mock(filename, file_type, extracted_text, file_size)

    try:
        return await _classify_with_llm(filename, file_type, extracted_text, file_size)
    except Exception as e:
        logger.warning(f"LLM classification failed for {filename}, falling back to mock: {e}")
        return classify_document_mock(filename, file_type, extracted_text, file_size)


async def generate_archive_report(
    documents: list[dict],
    category_stats: dict,
    important_dates: list[str],
    high_sensitivity_count: int,
    needs_review_count: int,
) -> dict:
    """Generate archive report using configured AI provider."""
    if AI_PROVIDER == "mock":
        return _generate_report_mock(documents, category_stats, important_dates,
                                     high_sensitivity_count, needs_review_count)
    try:
        return await _generate_report_llm(documents, category_stats, important_dates,
                                          high_sensitivity_count, needs_review_count)
    except Exception as e:
        logger.warning(f"LLM report generation failed, falling back to mock: {e}")
        return _generate_report_mock(documents, category_stats, important_dates,
                                     high_sensitivity_count, needs_review_count)


async def parse_search_intent(query: str, categories: list[str]) -> dict:
    """Parse search intent using configured AI provider."""
    if AI_PROVIDER == "mock":
        return _parse_search_intent_mock(query, categories)
    try:
        return await _parse_search_intent_llm(query, categories)
    except Exception as e:
        logger.warning(f"LLM search intent parsing failed, falling back to mock: {e}")
        return _parse_search_intent_mock(query, categories)


# ── LLM Implementation (OpenAI-compatible) ──


async def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call OpenAI-compatible LLM API."""
    import httpx

    api_key = os.getenv("AI_API_KEY", "")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("AI_MODEL", "gpt-4o")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def _classify_with_llm(filename, file_type, extracted_text, file_size) -> ClassificationResult:
    system_prompt = """你是一个个人资料分类助手。分析用户上传的文件，输出JSON分类结果。
输出格式：
{"category":"","summary":"","tags":[],"people":[],"organizations":[],"important_dates":[],"sensitivity_level":"low|medium|high","recommended_folder":"","needs_review":true,"confidence":0.0}
类别：身份与证件、合同与法律、医疗与健康、保险与资产、房屋与车辆、学习与证书、工作资料、发票与报销、家庭纪念、旅行与照片、待确认"""

    user_prompt = f"文件名: {filename}\n类型: {file_type}\n大小: {file_size}字节\n\n内容:\n{extracted_text[:3000]}"

    raw = await _call_llm(system_prompt, user_prompt)
    data = json.loads(raw)
    return ClassificationResult(**data)


async def _generate_report_llm(documents, category_stats, important_dates,
                               high_sensitivity_count, needs_review_count) -> dict:
    system_prompt = """你是一个资料库报告生成助手。根据所有文件的分类结果生成总览报告。
输出JSON格式：
{"overview":"","category_summary":[],"important_timeline":[],"missing_materials":[],"risk_notes":[],"handoff_checklist":[],"next_actions":[]}"""

    user_prompt = json.dumps({
        "document_count": len(documents),
        "category_stats": category_stats,
        "important_dates": important_dates[:20],
        "high_sensitivity_count": high_sensitivity_count,
        "needs_review_count": needs_review_count,
        "documents_summary": [{"filename": d.get("filename", ""), "category": d.get("category", "")} for d in documents[:30]],
    }, ensure_ascii=False)

    raw = await _call_llm(system_prompt, user_prompt)
    return json.loads(raw)


async def _parse_search_intent_llm(query: str, categories: list[str]) -> dict:
    system_prompt = """分析用户搜索意图，输出JSON：
{"intent":"","category_filter":"","date_filter":"","sensitivity_filter":"","keywords":[]}"""

    user_prompt = f"用户查询: {query}\n可用分类: {', '.join(categories)}"

    raw = await _call_llm(system_prompt, user_prompt)
    return json.loads(raw)


# ── Mock Implementations ──


def _generate_report_mock(documents, category_stats, important_dates,
                          high_sensitivity_count, needs_review_count) -> dict:
    total = len(documents)
    categories = list(category_stats.keys())

    overview = f"本次共整理 {total} 份文件，识别出 {len(categories)} 个类别。"
    if high_sensitivity_count > 0:
        overview += f"其中 {high_sensitivity_count} 份为高敏感文件，请妥善保管。"
    if needs_review_count > 0:
        overview += f"有 {needs_review_count} 份文件需要人工确认分类。"

    category_summary = [
        {"category": cat, "count": count}
        for cat, count in category_stats.items()
    ]

    missing = []
    all_categories = {"身份与证件", "合同与法律", "医疗与健康", "保险与资产",
                      "房屋与车辆", "学习与证书", "工作资料", "发票与报销"}
    present = set(category_stats.keys())
    missing_cats = all_categories - present
    for cat in missing_cats:
        missing.append(f"未发现「{cat}」类文件，建议检查是否需要补充")

    risk_notes = []
    if high_sensitivity_count > 0:
        risk_notes.append(f"发现 {high_sensitivity_count} 份高敏感文件，建议加密存储")
    if needs_review_count > 0:
        risk_notes.append(f"{needs_review_count} 份文件分类置信度较低，建议人工复查")

    handoff = [
        "整理所有身份与证件文件的副本",
        "确保保险保单信息完整且在有效期内",
        "记录重要合同的到期时间和续签提醒",
        "备份医疗健康记录",
        "整理家庭紧急联系人信息",
    ]

    next_actions = []
    if needs_review_count > 0:
        next_actions.append(f"复查 {needs_review_count} 份待确认文件")
    next_actions.append("补充缺失类别的资料")
    next_actions.append("定期更新资料库")

    return {
        "overview": overview,
        "category_summary": category_summary,
        "important_timeline": important_dates[:10],
        "missing_materials": missing,
        "risk_notes": risk_notes,
        "handoff_checklist": handoff,
        "next_actions": next_actions,
    }


def _parse_search_intent_mock(query: str, categories: list[str]) -> dict:
    intent = "search"
    category_filter = ""
    date_filter = ""
    sensitivity_filter = ""
    keywords = []

    # Category matching
    for cat in categories:
        if cat in query:
            category_filter = cat
            break

    category_keywords = {
        "保险": "保险与资产", "合同": "合同与法律", "医疗": "医疗与健康",
        "体检": "医疗与健康", "发票": "发票与报销", "证件": "身份与证件",
        "身份证": "身份与证件", "毕业": "学习与证书", "旅行": "旅行与照片",
        "车辆": "房屋与车辆", "家庭": "家庭纪念", "工作": "工作资料",
    }
    if not category_filter:
        for kw, cat in category_keywords.items():
            if kw in query:
                category_filter = cat
                break

    # Sensitivity filter
    if "敏感" in query or "高敏感" in query:
        sensitivity_filter = "high"
    elif "需要确认" in query or "人工确认" in query:
        intent = "filter_review"

    # Date filter
    import re
    year_match = re.search(r"(\d{4})年?", query)
    if year_match:
        date_filter = year_match.group(1)

    # Keywords
    for word in query.split():
        if len(word) >= 2:
            keywords.append(word)

    return {
        "intent": intent,
        "category_filter": category_filter,
        "date_filter": date_filter,
        "sensitivity_filter": sensitivity_filter,
        "keywords": keywords,
    }
