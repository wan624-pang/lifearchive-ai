export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">隐私设计说明</h1>

      <div className="space-y-8">
        <PrivacySection
          number="1"
          title="数据最小化"
          description="LifeArchive AI 只处理用户主动上传的文件。系统不会自动扫描你的设备、网盘或云端存储。所有数据处理都基于用户明确的上传操作。"
        />
        <PrivacySection
          number="2"
          title="本地优先"
          description="MVP 版本使用本地 SQLite 数据库，所有数据存储在你的设备上。文件解析和分类处理在本地完成。后续版本将支持本地向量数据库，实现完全离线的语义搜索。"
        />
        <PrivacySection
          number="3"
          title="敏感信息保护"
          description="系统会自动识别身份证号、手机号、银行卡号、地址等敏感信息，并标记敏感等级。后续版本将支持敏感字段脱敏展示，避免在界面上直接显示敏感数据。"
        />
        <PrivacySection
          number="4"
          title="AI 结果可解释"
          description="所有 AI 分类结果都会显示置信度（confidence）和是否需要人工确认（needs_review）。用户可以随时查看分类依据，并手动修正不正确的分类。AI 只是辅助工具，最终决定权在用户。"
        />
        <PrivacySection
          number="5"
          title="不保存密码"
          description="如果系统识别到包含账户或密码信息的文件，只会标记为「敏感账号资料」，不会在摘要或任何界面中展示密码明文。"
        />
        <PrivacySection
          number="6"
          title="可删除"
          description="用户可以随时删除整个资料库或单个文件。后续版本将支持一键清除所有数据，确保用户对自己的数据有完全的控制权。"
        />
        <PrivacySection
          number="7"
          title="边界声明"
          description="LifeArchive AI 不提供法律、医疗、财务建议。系统只做资料整理和检索辅助，所有分类结果都需要用户自行确认。涉及重要决策时，请咨询专业人士。"
        />

        <div className="bg-primary-50 border border-primary-200 rounded-xl p-6 mt-8">
          <h2 className="text-lg font-semibold text-primary-900 mb-2">我们的承诺</h2>
          <p className="text-sm text-primary-800 leading-relaxed">
            LifeArchive AI 的设计理念是「你的数据属于你」。我们不会收集、存储或分享你的任何个人文件。
            所有处理都在本地完成，AI 接口（如果使用真实 LLM）只会发送文件内容用于分类，不会用于训练或其他目的。
          </p>
        </div>
      </div>
    </div>
  );
}

function PrivacySection({ number, title, description }: {
  number: string;
  title: string;
  description: string;
}) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-bold">
        {number}
      </div>
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">{title}</h2>
        <p className="text-gray-600 leading-relaxed">{description}</p>
      </div>
    </div>
  );
}
