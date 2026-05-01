"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getArchive, getDocuments, getDocument, searchDocuments, Document, DocumentDetail } from "@/lib/api";
import StatsCards from "@/components/StatsCards";
import CategoryChart from "@/components/CategoryChart";
import DocumentTable from "@/components/DocumentTable";
import SearchBox from "@/components/SearchBox";
import DocumentDetailPanel from "@/components/DocumentDetail";

export default function ArchiveDashboard() {
  const params = useParams();
  const archiveId = params.id as string;

  const [archiveName, setArchiveName] = useState("");
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<DocumentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [searchIntent, setSearchIntent] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      const [archive, docs] = await Promise.all([
        getArchive(archiveId),
        getDocuments(archiveId),
      ]);
      setArchiveName(archive.name);
      setDocuments(docs);
    } catch (e) {
      console.error("Failed to load archive:", e);
    } finally {
      setLoading(false);
    }
  }, [archiveId]);

  useEffect(() => { loadData(); }, [loadData]);

  async function handleSearch(query: string) {
    setSearching(true);
    setSearchIntent(null);
    try {
      const result = await searchDocuments(archiveId, query);
      setDocuments(result.documents);
      setSearchIntent(result.intent);
    } catch (e) {
      console.error("Search failed:", e);
    } finally {
      setSearching(false);
    }
  }

  async function handleSelectDoc(doc: Document) {
    try {
      const detail = await getDocument(doc.id);
      setSelectedDoc(detail);
    } catch (e) {
      console.error("Failed to load document:", e);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const highSensitivity = documents.filter((d) => d.sensitivity_level === "high").length;
  const needsReview = documents.filter((d) => d.needs_review).length;
  const categoryMap: Record<string, number> = {};
  documents.forEach((d) => {
    categoryMap[d.category] = (categoryMap[d.category] || 0) + 1;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{archiveName}</h1>
          <p className="text-sm text-gray-500 mt-1">资料库 Dashboard</p>
        </div>
        <Link
          href={`/archives/${archiveId}/report`}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium transition-colors"
        >
          查看报告
        </Link>
      </div>

      {/* Stats */}
      <div className="mb-8">
        <StatsCards
          totalDocs={documents.length}
          highSensitivity={highSensitivity}
          needsReview={needsReview}
          categories={Object.keys(categoryMap).length}
        />
      </div>

      {/* Search */}
      <div className="mb-6">
        <SearchBox onSearch={handleSearch} loading={searching} />
        {searchIntent && (
          <p className="text-sm text-gray-500 mt-2">
            搜索意图: <span className="font-medium text-primary-600">{searchIntent}</span>
          </p>
        )}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Document Table */}
        <div className="lg:col-span-2">
          <DocumentTable documents={documents} onSelect={handleSelectDoc} selectedId={selectedDoc?.id} />
        </div>

        {/* Category Chart */}
        <div>
          <CategoryChart data={categoryMap} />
        </div>
      </div>

      {/* Document Detail Drawer */}
      {selectedDoc && (
        <DocumentDetailPanel document={selectedDoc} onClose={() => setSelectedDoc(null)} />
      )}
    </div>
  );
}
