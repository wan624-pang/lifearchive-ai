# Contributing to LifeArchive AI

感谢你对 LifeArchive AI 的关注！

## 如何贡献

### 报告 Bug
- 使用 GitHub Issues 提交 bug 报告
- 请包含复现步骤、期望行为和实际行为
- 附上截图或错误日志

### 功能建议
- 在 Issues 中使用 "Feature Request" 标签
- 描述使用场景和期望的解决方案

### 提交代码
1. Fork 本仓库
2. 创建功能分支: `git checkout -b feature/your-feature`
3. 提交更改: `git commit -m "feat: add your feature"`
4. 推送分支: `git push origin feature/your-feature`
5. 创建 Pull Request

## 开发环境

```bash
# 后端
cd apps/api
pip install -r requirements.txt
python main.py

# 前端
cd apps/web
npm install
npm run dev
```

## 代码规范
- Python: 使用 type hints，清晰的函数命名
- TypeScript: 严格模式，避免 `any`
- 提交信息遵循 Conventional Commits 格式

## 行为准则
- 尊重所有参与者
- 建设性地讨论问题
- 聚焦于技术本身
