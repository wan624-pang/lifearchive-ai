"use client";

interface CategoryChartProps {
  data: Record<string, number>;
}

const CATEGORY_COLORS: Record<string, string> = {
  "身份与证件": "bg-red-400",
  "合同与法律": "bg-blue-500",
  "医疗与健康": "bg-pink-400",
  "保险与资产": "bg-purple-500",
  "房屋与车辆": "bg-orange-400",
  "学习与证书": "bg-cyan-400",
  "工作资料": "bg-indigo-400",
  "发票与报销": "bg-yellow-400",
  "家庭纪念": "bg-rose-300",
  "旅行与照片": "bg-emerald-400",
  "待确认": "bg-gray-400",
};

export default function CategoryChart({ data }: CategoryChartProps) {
  const total = Object.values(data).reduce((s, v) => s + v, 0);
  const entries = Object.entries(data).sort((a, b) => b[1] - a[1]);

  return (
    <div className="bg-white rounded-xl p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">类别分布</h3>
      <div className="space-y-3">
        {entries.map(([cat, count]) => {
          const pct = total > 0 ? (count / total) * 100 : 0;
          const color = CATEGORY_COLORS[cat] || "bg-gray-400";
          return (
            <div key={cat}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-700">{cat}</span>
                <span className="text-gray-500">{count} 份 ({pct.toFixed(0)}%)</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div className={`${color} h-2 rounded-full transition-all`} style={{ width: `${pct}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
