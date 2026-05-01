"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getReport, Report } from "@/lib/api";

export default function ReportPage() {
  const params = useParams();
  const archiveId = params.id as string;
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getReport(archiveId)
      .then(setReport)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [archiveId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-gray-500">正在生成报告...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <p className="text-red-500 mb-4">{error}</p>
        <Link href={`/archives/${archiveId}`} className="text-primary-600 hover:underline">
          返回资料库
        </Link>
      </div>
    );
  }

  if (!report) return null;
  const { content } = report;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-900">资料库总览报告</h1>
        <Link
          href={`/archives/${archiveId}`}
          className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm font-medium transition-colors"
        >
          返回资料库
        </Link>
      </div>

      {/* Overview */}
      <Section title="总览摘要">
        <p className="text-gray-700 leading-relaxed">{content.overview}</p>
      </Section>

      {/* Category Summary */}
      {content.category_summary.length > 0 && (
        <Section title="分类统计">
          <div className="grid sm:grid-cols-2 gap-3">
            {content.category_summary.map((cat) => (
              <div key={cat.category} className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-3">
                <span className="text-sm text-gray-700">{cat.category}</span>
                <span className="text-sm font-bold text-primary-600">{cat.count} 份</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Important Timeline */}
      {content.important_timeline.length > 0 && (
        <Section title="重要时间线">
          <div className="space-y-3">
            {content.important_timeline.map((event, i) => (
              <div key={i} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 bg-primary-500 rounded-full" />
                  {i < content.important_timeline.length - 1 && <div className="w-0.5 h-full bg-primary-200" />}
                </div>
                <div className="pb-4">
                  <p className="font-mono text-xs text-primary-600">{event.date}</p>
                  <p className="text-sm text-gray-800">{event.event}</p>
                  {event.source && <p className="text-xs text-gray-400">来源: {event.source}</p>}
                </div>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Missing Materials */}
      {content.missing_materials.length > 0 && (
        <Section title="缺失材料提醒">
          <ul className="space-y-2">
            {content.missing_materials.map((item, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <span className="text-yellow-500 mt-0.5">!</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Risk Notes */}
      {content.risk_notes.length > 0 && (
        <Section title="风险提示">
          <ul className="space-y-2">
            {content.risk_notes.map((note, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-red-700 bg-red-50 rounded-lg px-4 py-2">
                <span className="font-bold">!</span>
                {note}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Handoff Checklist */}
      {content.handoff_checklist.length > 0 && (
        <Section title="家庭交接清单">
          <div className="space-y-2">
            {content.handoff_checklist.map((item, i) => (
              <div key={i} className="flex items-center gap-3 bg-gray-50 rounded-lg px-4 py-3">
                <input type="checkbox" className="w-4 h-4 text-primary-600 rounded" />
                <span className="text-sm text-gray-800">{typeof item === 'string' ? item : item.item || String(item)}</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Next Actions */}
      {content.next_actions.length > 0 && (
        <Section title="下一步建议">
          <div className="space-y-2">
            {content.next_actions.map((action, i) => (
              <div key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <span className="text-primary-500 font-bold">{i + 1}.</span>
                {action}
              </div>
            ))}
          </div>
        </Section>
      )}
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-6 mb-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">{title}</h2>
      {children}
    </div>
  );
}
