import os
import zipfile
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedFile:
    filename: str
    file_path: str
    file_type: str
    file_size: int
    extracted_text: str = ""
    parse_status: str = "ok"


SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".pdf", ".docx", ".jpg", ".jpeg", ".png",
}


def extract_zip(zip_path: str, extract_to: str) -> list[str]:
    """Extract ZIP file and return list of extracted file paths."""
    extracted = []
    target_dir = Path(extract_to).resolve()
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            destination = (target_dir / member.filename).resolve()
            if target_dir != destination and target_dir not in destination.parents:
                raise ValueError(f"Unsafe ZIP entry path: {member.filename}")
            zf.extract(member, target_dir)
            if destination.is_file():
                extracted.append(str(destination))
    return extracted


def parse_file(file_path: str) -> ParsedFile:
    """Parse a single file and extract text content."""
    path = Path(file_path)
    ext = path.suffix.lower()
    file_size = os.path.getsize(file_path)

    parsed = ParsedFile(
        filename=path.name,
        file_path=file_path,
        file_type=ext,
        file_size=file_size,
    )

    try:
        if ext in (".txt", ".md"):
            parsed.extracted_text = _parse_text(file_path)
        elif ext == ".pdf":
            parsed.extracted_text = _parse_pdf(file_path)
        elif ext == ".docx":
            parsed.extracted_text = _parse_docx(file_path)
        elif ext in (".jpg", ".jpeg", ".png"):
            parsed.extracted_text = f"[图片文件: {path.name}]"
            parsed.parse_status = "needs_ocr"
        else:
            parsed.extracted_text = ""
            parsed.parse_status = "unsupported_format"
    except Exception as e:
        parsed.extracted_text = ""
        parsed.parse_status = f"error: {str(e)}"

    return parsed


def _parse_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _parse_pdf(file_path: str) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n".join(text_parts)
    except ImportError:
        return "[PDF解析需要 pypdf 库]"
    except Exception as e:
        return f"[PDF解析失败: {str(e)}]"


def _parse_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except ImportError:
        return "[DOCX解析需要 python-docx 库]"
    except Exception as e:
        return f"[DOCX解析失败: {str(e)}]"


def list_extracted_files(extract_dir: str) -> list[str]:
    """List all files in the extracted directory."""
    files = []
    for root, _, filenames in os.walk(extract_dir):
        for fname in filenames:
            full_path = os.path.join(root, fname)
            if Path(full_path).suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(full_path)
    return files
