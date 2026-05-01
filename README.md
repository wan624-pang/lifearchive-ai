# LifeArchive AI

**个人与家庭数字资料库整理助手**

把散落在电脑、网盘、手机里的合同、票据、照片、病历、证书、保险、房屋资料整理成一个可搜索、可总结、可交接的私人资料库。

## 为什么做这个项目

每个人的数字生活中都积累了大量重要文件：租房合同、体检报告、保险保单、毕业证书、发票收据、旅行记录……这些文件散落在各种地方，文件名混乱，格式不统一，需要时找不到，交接时理不清。

LifeArchive AI 用 AI 帮你自动分类、提取关键信息、生成摘要和标签，让你的个人资料从「一团乱麻」变成「私人档案馆」。

## 核心功能

- **ZIP 上传**：上传一个压缩包，系统自动解压、解析所有文件
- **智能分类**：自动识别合同、病历、保险、证件等 11 种类别
- **摘要生成**：为每个文件生成简短摘要和关键词标签
- **关键信息提取**：识别涉及的人物、机构、重要日期
- **敏感等级判断**：自动标记高敏感文件，提醒妥善保管
- **资料库报告**：生成总览报告，包含统计、时间线、缺失提醒、交接清单
- **自然语言搜索**：用自然语言查找文件，如「找出所有保险相关文件」
- **隐私优先**：默认本地处理，数据不离开你的设备

## 技术架构

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend    │────▶│   Database   │
│  Next.js 14  │     │   FastAPI    │     │   SQLite     │
│  TypeScript  │     │   Python     │     │              │
│  Tailwind    │     │              │     │              │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────┴───────┐
                    │  AI Service  │
                    │  Mock / LLM  │
                    └──────────────┘
```

**后端**: FastAPI + SQLAlchemy + SQLite  
**前端**: Next.js 14 + TypeScript + Tailwind CSS  
**AI**: Mock 模式（默认）/ OpenAI-compatible API

## 快速开始

### 前置条件
- Python 3.10+
- Node.js 18+
- npm 或 yarn

### 1. 启动后端

```bash
cd apps/api
pip install -r requirements.txt
cp ../../.env.example .env
python main.py
```

后端将在 http://localhost:8000 启动。

### 2. 启动前端

```bash
cd apps/web
npm install
npm run dev
```

前端将在 http://localhost:3000 启动。

### 3. 使用示例数据

打开 http://localhost:3000，点击「试试示例数据演示」按钮，系统会自动加载 `examples/sample_archive/` 中的示例文件。

### 4. 上传自己的文件

将你的个人资料打包成 ZIP 文件，拖拽到上传区域即可。

## 环境变量

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
# AI Provider: "mock" | "openai_compatible"
AI_PROVIDER=mock

# OpenAI-compatible API (仅 openai_compatible 模式需要)
AI_API_KEY=your_api_key
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o

# 数据库
DATABASE_URL=sqlite:///./lifearchive.db

# 服务器
API_HOST=0.0.0.0
API_PORT=8000

# 前端
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API 说明

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/upload` | 上传 ZIP 文件 |
| POST | `/api/demo` | 加载示例数据 |
| GET | `/api/archives/{id}` | 获取资料库信息 |
| GET | `/api/archives/{id}/documents` | 获取文件列表 |
| GET | `/api/documents/{id}` | 获取文件详情 |
| GET | `/api/archives/{id}/report` | 获取资料库报告 |
| POST | `/api/archives/{id}/search` | 自然语言搜索 |
| GET | `/api/health` | 健康检查 |

## 示例数据

`examples/sample_archive/` 包含 8 个虚构示例文件：

| 文件 | 类别 | 说明 |
|------|------|------|
| rent_contract.txt | 合同与法律 | 虚构租房合同 |
| health_check_2024.txt | 医疗与健康 | 虚构体检报告 |
| insurance_policy.txt | 保险与资产 | 虚构保险保单 |
| reimbursement_receipts.md | 发票与报销 | 虚构报销记录 |
| graduation_certificate_note.txt | 学习与证书 | 虚构毕业证说明 |
| family_emergency_contacts.txt | 家庭纪念 | 虚构紧急联系人 |
| car_maintenance_record.txt | 房屋与车辆 | 虚构车辆保养记录 |
| travel_hangzhou_2025.md | 旅行与照片 | 虚构旅行计划 |

## 路线图

### MVP (当前版本)
- ZIP 上传与文件解析
- Mock AI 分类与摘要
- 资料库报告生成
- 自然语言搜索
- Web Dashboard

### v0.2
- [ ] 真实 LLM API 接入
- [ ] OCR 图片文字识别
- [ ] 重复文件检测
- [ ] 时间线视图

### v0.3
- [ ] 本地向量数据库语义搜索
- [ ] 多语言支持
- [ ] 家庭交接清单导出
- [ ] 敏感信息脱敏

### v1.0
- [ ] 端侧隐私模式
- [ ] 移动端适配
- [ ] 批量文件管理
- [ ] 自定义分类规则

## 隐私说明

- 默认本地处理，数据不离开你的设备
- 不保存密码原文，只标记「敏感账号资料」
- AI 分类结果需要人工确认
- 支持删除资料库和单个文件
- 详见 [docs/privacy-design.md](docs/privacy-design.md)

## 项目结构

```
lifearchive-ai/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── apps/
│   ├── api/                    # 后端 (FastAPI)
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── db/             # 数据库配置
│   │       ├── models/         # ORM 和 Schema
│   │       ├── routers/        # API 路由
│   │       └── services/       # 业务逻辑
│   └── web/                    # 前端 (Next.js)
│       ├── package.json
│       └── src/
│           ├── app/            # 页面
│           ├── components/     # 组件
│           └── lib/            # API 客户端
├── docs/                       # 文档
├── examples/                   # 示例数据
└── packages/                   # 共享包
    ├── archive-schema/         # 类型定义
    └── prompts/                # Prompt 模板
```

## Token 计划申请说明

本项目是一个真实可用的个人资料管理工具，需要大量 token 用于：

1. **文档处理**：每个文件需要独立的 AI 分类调用，包含长文本上下文
2. **多轮分类**：分类 → 摘要 → 标签 → 报告，每轮都需要 LLM
3. **长上下文**：PDF、合同等文件内容较长，需要大上下文窗口
4. **持续迭代**：优化 prompt、测试不同文档类型、评估分类质量
5. **报告生成**：需要综合所有文件信息生成连贯的总览报告

## License

MIT
