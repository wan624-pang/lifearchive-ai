import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LifeArchive AI",
  description: "个人与家庭数字资料库整理助手",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="bg-gray-50 min-h-screen">
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-14 items-center">
              <a href="/" className="flex items-center gap-2">
                <span className="text-xl font-bold text-primary-600">LifeArchive AI</span>
              </a>
              <div className="flex items-center gap-4">
                <a href="/privacy" className="text-sm text-gray-500 hover:text-gray-700">
                  隐私说明
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
