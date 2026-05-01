const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Archive {
  id: string;
  name: string;
  created_at: string;
  document_count: number;
}

export interface Document {
  id: string;
  archive_id: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  summary: string;
  category: string;
  tags: string[];
  people: string[];
  organizations: string[];
  important_dates: string[];
  sensitivity_level: "low" | "medium" | "high";
  recommended_folder: string;
  confidence: number;
  needs_review: boolean;
  created_at: string;
}

export interface DocumentDetail extends Document {
  extracted_text: string;
  file_path: string;
}

export interface Report {
  id: string;
  archive_id: string;
  content: {
    overview: string;
    category_summary: { category: string; count: number; description?: string }[];
    important_timeline: { date: string; event: string; source?: string }[];
    missing_materials: string[];
    risk_notes: string[];
    handoff_checklist: { item: string; status: string; related_files?: string[] }[];
    next_actions: string[];
  };
  created_at: string;
}

export interface SearchResult {
  documents: Document[];
  intent: string | null;
  total: number;
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API Error");
  }
  return res.json();
}

export async function uploadArchive(file: File): Promise<Archive> {
  const form = new FormData();
  form.append("file", file);
  return apiFetch<Archive>("/api/upload", { method: "POST", body: form });
}

export async function loadDemo(): Promise<Archive> {
  return apiFetch<Archive>("/api/demo", { method: "POST" });
}

export async function getArchive(id: string): Promise<Archive> {
  return apiFetch<Archive>(`/api/archives/${id}`);
}

export async function getDocuments(archiveId: string): Promise<Document[]> {
  return apiFetch<Document[]>(`/api/archives/${archiveId}/documents`);
}

export async function getDocument(id: string): Promise<DocumentDetail> {
  return apiFetch<DocumentDetail>(`/api/documents/${id}`);
}

export async function getReport(archiveId: string): Promise<Report> {
  return apiFetch<Report>(`/api/archives/${archiveId}/report`);
}

export async function searchDocuments(archiveId: string, query: string): Promise<SearchResult> {
  return apiFetch<SearchResult>(`/api/archives/${archiveId}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
}
