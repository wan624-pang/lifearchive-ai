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
  content: ReportContent;
  created_at: string;
}

export interface ReportContent {
  overview: string;
  category_summary: CategorySummary[];
  important_timeline: TimelineEvent[];
  missing_materials: string[];
  risk_notes: string[];
  handoff_checklist: HandoffItem[];
  next_actions: string[];
}

export interface CategorySummary {
  category: string;
  count: number;
  description?: string;
}

export interface TimelineEvent {
  date: string;
  event: string;
  source?: string;
}

export interface HandoffItem {
  item: string;
  status: string;
  related_files?: string[];
}

export interface SearchResult {
  documents: Document[];
  intent: string | null;
  total: number;
}

export const CATEGORIES = [
  "身份与证件",
  "合同与法律",
  "医疗与健康",
  "保险与资产",
  "房屋与车辆",
  "学习与证书",
  "工作资料",
  "发票与报销",
  "家庭纪念",
  "旅行与照片",
  "待确认",
] as const;

export type Category = (typeof CATEGORIES)[number];
