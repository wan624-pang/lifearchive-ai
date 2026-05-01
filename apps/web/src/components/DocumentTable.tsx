import { Document } from "@/lib/api";

interface DocumentTableProps {
  documents: Document[];
  onSelect: (doc: Document) => void;
  selectedId?: string;
}

function sensitivityBadge(level: string) {
  const styles: Record<string, string> = {
    high: "sensitivity-high",
    medium: "sensitivity-medium",
    low: "sensitivity-low",
  };
  const labels: Record<string, string> = {
    high: "高",
    medium: "中",
    low: "低",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${styles[level] || styles.low}`}>
      {labels[level] || level}
    </span>
  );
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function DocumentTable({ documents, onSelect, selectedId }: DocumentTableProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left">
              <th className="px-4 py-3 font-medium text-gray-600">文件名</th>
              <th className="px-4 py-3 font-medium text-gray-600">类别</th>
              <th className="px-4 py-3 font-medium text-gray-600 hidden md:table-cell">摘要</th>
              <th className="px-4 py-3 font-medium text-gray-600">敏感度</th>
              <th className="px-4 py-3 font-medium text-gray-600 hidden sm:table-cell">大小</th>
              <th className="px-4 py-3 font-medium text-gray-600">状态</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {documents.map((doc) => (
              <tr
                key={doc.id}
                onClick={() => onSelect(doc)}
                className={`cursor-pointer hover:bg-primary-50 transition-colors
                  ${selectedId === doc.id ? "bg-primary-50" : ""}`}
              >
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <FileTypeIcon type={doc.file_type} />
                    <span className="font-medium text-gray-900 truncate max-w-[200px]">
                      {doc.original_filename}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 bg-gray-100 rounded text-xs text-gray-700">
                    {doc.category}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-600 hidden md:table-cell">
                  <p className="truncate max-w-[300px]">{doc.summary}</p>
                </td>
                <td className="px-4 py-3">{sensitivityBadge(doc.sensitivity_level)}</td>
                <td className="px-4 py-3 text-gray-500 hidden sm:table-cell">{formatSize(doc.file_size)}</td>
                <td className="px-4 py-3">
                  {doc.needs_review ? (
                    <span className="text-yellow-600 text-xs font-medium">待确认</span>
                  ) : (
                    <span className="text-green-600 text-xs font-medium">已确认</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function FileTypeIcon({ type }: { type: string }) {
  const colors: Record<string, string> = {
    ".txt": "bg-gray-100 text-gray-600",
    ".md": "bg-blue-100 text-blue-600",
    ".pdf": "bg-red-100 text-red-600",
    ".docx": "bg-blue-100 text-blue-600",
    ".jpg": "bg-green-100 text-green-600",
    ".jpeg": "bg-green-100 text-green-600",
    ".png": "bg-green-100 text-green-600",
  };
  const labels: Record<string, string> = {
    ".txt": "TXT",
    ".md": "MD",
    ".pdf": "PDF",
    ".docx": "DOC",
    ".jpg": "IMG",
    ".jpeg": "IMG",
    ".png": "IMG",
  };

  return (
    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${colors[type] || colors[".txt"]}`}>
      {labels[type] || "FILE"}
    </span>
  );
}
