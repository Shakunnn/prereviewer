# AI PR Reviewer Agent 

![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success.svg)
![LLM Support](https://img.shields.io/badge/LLM-OpenAI%20%7C%20DeepSeek%20%7C%20Kimi-orange.svg)

基于大语言模型（LLM）与多 Agent 协作架构的自动化代码审查机器人。该项目深度集成于 GitHub CI/CD 工作流，旨在通过长链推理自动分析 Pull Request (PR) 的代码变更，识别潜在缺陷、安全漏洞并提供优化建议，从而大幅降低人工 Code Review 成本。

## 核心特性

- **零侵入自动化集成**：基于 GitHub Actions 原生触发，当开发者提交或更新 PR 时自动运行，无需额外部署服务器。
- **深度代码缺陷审查**：不仅检查代码规范（Lint），更能通过上下文推理发现潜在的逻辑死循环、并发风险及安全漏洞（如 SQL 注入、越权访问）。
- **友好的交互反馈**：分析完成后，Agent 会以 Markdown 格式自动将结构化的审查报告（包含总结、问题点、代码修改建议）发送至 PR 评论区。
- **多模型底层兼容**：标准兼容 OpenAI API 格式，支持快速切换至 DeepSeek、Kimi (Moonshot)、智谱 GLM 等高性能国产大模型。

## 系统架构与 Agent 工作流

本项目旨在构建一个全局感知的代码智能系统，核心包含以下逻辑环节：

1. **Diff 获取与预处理**：自动拉取 PR 的增量代码，进行长度截断与格式化，确保满足 LLM 上下文窗口要求。
2. **Reviewer Agent 推理**：设定严格的系统提示词（System Prompt），赋予 AI 资深架构师的角色，使其按照性能、安全、可读性等多维度进行辩论与交叉验证。
3. **闭环反馈**：通过 GitHub REST API 自动回调，将 AI 的“思考结果”落地为研发流水线上的关键审查凭证。

## 快速部署指南

只需 3 分钟，即可在你的代码仓库中激活该 AI 审查助手：

### 1. 拷贝核心文件
将本仓库的以下文件放入你需要启用审查的目标项目中：
- `pr_reviewer.py` (核心脚本，放于根目录)
- `requirements.txt` (依赖清单，放于根目录)
- `.github/workflows/ai-review.yml` (Actions 配置文件)

### 2. 配置大模型 API 密钥 (Secrets)
1. 进入你的 GitHub 仓库主页，点击 **Settings**。
2. 在左侧导航栏找到 **Secrets and variables** -> **Actions**。
3. 点击右上角的 **New repository secret**：
   - **Name**: 填写 `AI_API_KEY`
   - **Secret**: 填写你的大模型 API 密钥。

### 3. (可选) 切换底层大模型
默认使用 OpenAI 接口配置。若使用其他模型（如 DeepSeek），请修改 `.github/workflows/ai-review.yml` 中的环境变量配置：
```yaml
env:
  # 取消注释并修改为你使用的模型 API 地址
  AI_BASE_URL: "https://api.deepseek.com/v1"
