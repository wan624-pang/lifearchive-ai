import re
import json
from dataclasses import dataclass, field


@dataclass
class ClassificationResult:
    category: str = "待确认"
    summary: str = ""
    tags: list[str] = field(default_factory=list)
    people: list[str] = field(default_factory=list)
    organizations: list[str] = field(default_factory=list)
    important_dates: list[str] = field(default_factory=list)
    sensitivity_level: str = "low"
    recommended_folder: str = "待确认"
    needs_review: bool = True
    confidence: float = 0.5


CATEGORY_RULES: list[tuple[list[str], str, str, str]] = [
    # (keywords, category, sensitivity, folder)
    (["合同", "租房", "租赁", "协议", "甲方", "乙方", "签署", "签约"],
     "合同与法律", "high", "合同与法律/"),
    (["体检", "医院", "诊断", "病历", "医疗", "处方", "检查报告", "化验"],
     "医疗与健康", "high", "医疗与健康/"),
    (["保险", "保单", "理赔", "投保", "被保险", "受益人", "保障"],
     "保险与资产", "high", "保险与资产/"),
    (["发票", "报销", "费用", "开票", "税额"],
     "发票与报销", "medium", "发票与报销/"),
    (["毕业", "证书", "学位", "学历", "学校", "毕业证"],
     "学习与证书", "medium", "学习与证书/"),
    (["身份证", "护照", "户口", "证件", "身份证明"],
     "身份与证件", "high", "身份与证件/"),
    (["房产", "房屋", "产权", "不动产", "购房"],
     "房屋与车辆", "high", "房屋与车辆/"),
    (["车辆", "汽车", "保养", "维修", "驾照", "行驶证", "保养记录"],
     "房屋与车辆", "medium", "房屋与车辆/"),
    (["紧急联系人", "家庭", "家属", "亲属", "家人"],
     "家庭纪念", "medium", "家庭纪念/"),
    (["旅行", "旅游", "行程", "机票", "酒店", "景点"],
     "旅行与照片", "low", "旅行与照片/"),
    (["工作", "项目", "周报", "绩效", "同事"],
     "工作资料", "medium", "工作资料/"),
]


def classify_document_mock(
    filename: str,
    file_type: str,
    extracted_text: str,
    file_size: int,
) -> ClassificationResult:
    """Classify a document using keyword rules (mock mode)."""
    text = f"{filename} {extracted_text}".lower()
    result = ClassificationResult()

    # Category classification
    best_match = None
    best_score = 0
    for keywords, category, sensitivity, folder in CATEGORY_RULES:
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_match = (category, sensitivity, folder)

    if best_match and best_score > 0:
        result.category = best_match[0]
        result.sensitivity_level = best_match[1]
        result.recommended_folder = best_match[2]
        result.confidence = min(0.95, 0.5 + best_score * 0.1)
        result.needs_review = best_score < 2
    else:
        result.category = "待确认"
        result.sensitivity_level = "low"
        result.recommended_folder = "待确认/"
        result.confidence = 0.2
        result.needs_review = True

    # Summary generation
    result.summary = _generate_summary(filename, extracted_text, result.category)

    # Tags extraction
    result.tags = _extract_tags(text, result.category)

    # People extraction
    result.people = _extract_people(extracted_text)

    # Organizations extraction
    result.organizations = _extract_organizations(extracted_text)

    # Date extraction
    result.important_dates = _extract_dates(extracted_text)

    return result


def _generate_summary(filename: str, text: str, category: str) -> str:
    name = filename.rsplit(".", 1)[0] if "." in filename else filename
    clean_name = name.replace("_", " ").replace("-", " ")

    if len(text) > 50:
        snippet = text[:200].replace("\n", " ").strip()
        return f"{category}类文件「{clean_name}」。{snippet}..."
    return f"{category}类文件「{clean_name}」"


def _extract_tags(text: str, category: str) -> list[str]:
    tags = [category]
    tag_keywords = {
        "合同": "合同", "保险": "保险", "医疗": "医疗", "体检": "体检",
        "发票": "发票", "报销": "报销", "旅行": "旅行", "工作": "工作",
        "家庭": "家庭", "车辆": "车辆", "证件": "证件", "证书": "证书",
    }
    for kw, tag in tag_keywords.items():
        if kw in text and tag not in tags:
            tags.append(tag)
    return tags[:6]


def _extract_people(text: str) -> list[str]:
    people = []
    name_patterns = [
        r"(?:姓名|患者|承租人|出租人|投保人|被保险人|受益人)[：:]\s*(\S+)",
        r"(?:甲方|乙方)[：:]\s*(\S+)",
        r"(\S{2,4})(?:先生|女士|医生)",
    ]
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            if m not in people and len(m) >= 2:
                people.append(m)
    return people[:5]


def _extract_organizations(text: str) -> list[str]:
    orgs = []
    org_patterns = [
        r"([\u4e00-\u9fa5]{2,}(?:公司|集团|医院|大学|学院|保险|银行|局|院|所|中心))",
    ]
    for pattern in org_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            if m not in orgs:
                orgs.append(m)
    return orgs[:5]


def _extract_dates(text: str) -> list[str]:
    dates = []
    patterns = [
        r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})",
        r"(\d{4}年\d{1,2}月\d{1,2}日)",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            normalized = m.replace("/", "-")
            if normalized not in dates:
                dates.append(normalized)
    return dates[:10]


def result_to_dict(result: ClassificationResult) -> dict:
    return {
        "category": result.category,
        "summary": result.summary,
        "tags": result.tags,
        "people": result.people,
        "organizations": result.organizations,
        "important_dates": result.important_dates,
        "sensitivity_level": result.sensitivity_level,
        "recommended_folder": result.recommended_folder,
        "needs_review": result.needs_review,
        "confidence": result.confidence,
    }
