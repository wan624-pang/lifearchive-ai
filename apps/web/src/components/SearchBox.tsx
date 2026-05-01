"use client";

import { useState } from "react";

interface SearchBoxProps {
  onSearch: (query: string) => void;
  loading?: boolean;
}

const SUGGESTIONS = [
  "找出所有保险相关文件",
  "我有没有上传身份证",
  "列出所有2024年的医疗资料",
  "哪些文件需要人工确认",
  "哪些文件敏感等级最高",
];

export default function SearchBox({ onSearch, loading }: SearchBoxProps) {
  const [query, setQuery] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim()) onSearch(query.trim());
  }

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索文件... 例如「找出所有保险相关文件」"
          className="flex-1 px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-5 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 text-sm font-medium transition-colors"
        >
          {loading ? "搜索中..." : "搜索"}
        </button>
      </form>
      <div className="flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => { setQuery(s); onSearch(s); }}
            className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full text-gray-600 transition-colors"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
