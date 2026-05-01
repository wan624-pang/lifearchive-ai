interface StatsCardsProps {
  totalDocs: number;
  highSensitivity: number;
  needsReview: number;
  categories: number;
}

export default function StatsCards({ totalDocs, highSensitivity, needsReview, categories }: StatsCardsProps) {
  const cards = [
    { label: "文件总数", value: totalDocs, color: "text-primary-600", bg: "bg-primary-50" },
    { label: "高敏感文件", value: highSensitivity, color: "text-red-600", bg: "bg-red-50" },
    { label: "待确认文件", value: needsReview, color: "text-yellow-600", bg: "bg-yellow-50" },
    { label: "分类数", value: categories, color: "text-green-600", bg: "bg-green-50" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div key={card.label} className={`${card.bg} rounded-xl p-4 border border-gray-100`}>
          <p className="text-sm text-gray-500 mb-1">{card.label}</p>
          <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
        </div>
      ))}
    </div>
  );
}
