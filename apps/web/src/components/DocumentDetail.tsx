import { DocumentDetail as DocDetail } from "@/lib/api";

interface DocumentDetailProps {
  document: DocDetail;
  onClose: () => void;
}

export default function DocumentDetail({ document: doc, onClose }: DocumentDetailProps) {
  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/30" onClick={onClose} />

      {/* Drawer */}
      <div className="ml-auto w-full max-w-lg bg-white shadow-xl overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900 truncate">{doc.original_filename}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 p-1">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="p-6 space-y-6">
          <InfoRow label="分类" value={doc.category} />
          <InfoRow label="敏感等级" value={
            <span className={doc.sensitivity_level === "high" ? "text-red-600 font-medium" : ""}>
              {doc.sensitivity_level === "high" ? "高敏感" : doc.sensitivity_level === "medium" ? "中敏感" : "低敏感"}
            </span>
          } />
          <InfoRow label="置信度" value={`${(doc.confidence * 100).toFixed(0)}%`} />
          <InfoRow label="推荐目录" value={doc.recommended_folder || "无"} />

          <div>
            <p className="text-xs text-gray-500 mb-1">摘要</p>
            <p className="text-sm text-gray-800 leading-relaxed">{doc.summary}</p>
          </div>

          <div>
            <p className="text-xs text-gray-500 mb-2">标签</p>
            <div className="flex flex-wrap gap-1.5">
              {doc.tags.map((tag) => (
                <span key={tag} className="px-2 py-0.5 bg-primary-50 text-primary-700 rounded text-xs">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {doc.people.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-2">涉及人物</p>
              <div className="flex flex-wrap gap-1.5">
                {doc.people.map((p) => (
                  <span key={p} className="px-2 py-0.5 bg-purple-50 text-purple-700 rounded text-xs">{p}</span>
                ))}
              </div>
            </div>
          )}

          {doc.organizations.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-2">涉及机构</p>
              <div className="flex flex-wrap gap-1.5">
                {doc.organizations.map((o) => (
                  <span key={o} className="px-2 py-0.5 bg-orange-50 text-orange-700 rounded text-xs">{o}</span>
                ))}
              </div>
            </div>
          )}

          {doc.important_dates.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-2">重要日期</p>
              <div className="flex flex-wrap gap-1.5">
                {doc.important_dates.map((d) => (
                  <span key={d} className="px-2 py-0.5 bg-green-50 text-green-700 rounded text-xs font-mono">{d}</span>
                ))}
              </div>
            </div>
          )}

          <div>
            <p className="text-xs text-gray-500 mb-1">文件类型</p>
            <p className="text-sm text-gray-800">{doc.file_type}</p>
          </div>

          <div>
            <p className="text-xs text-gray-500 mb-2">提取文本</p>
            <pre className="text-xs text-gray-600 bg-gray-50 rounded-lg p-4 whitespace-pre-wrap max-h-60 overflow-y-auto leading-relaxed">
              {doc.extracted_text || "（无文本内容）"}
            </pre>
          </div>

          {doc.needs_review && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-yellow-800 font-medium">需要人工确认</p>
              <p className="text-xs text-yellow-700 mt-1">
                此文件的自动分类置信度较低，请确认分类是否正确。
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div>
      <p className="text-xs text-gray-500 mb-0.5">{label}</p>
      <p className="text-sm text-gray-800">{value}</p>
    </div>
  );
}
