# README.md
# 🏢 企业制度智能问答 Agent

基于 RAG（检索增强生成）技术的企业级智能问答系统。

## ✨ 功能特性

- 📄 **文档管理**：支持上传 PDF/Word 文档，自动解析并向量化存储
- 🔍 **智能检索**：Query 改写 + 混合检索（向量 + BM25）+ Cross-Encoder 精排
- 💬 **多轮对话**：支持会话管理，保存完整对话历史
- 🔐 **用户认证**：JWT Token 认证，密码加密存储
- 📊 **引用溯源**：回答附带文档来源，解决 AI 幻觉问题
- 🚀 **高性能**：FastAPI 异步框架，支持高并发

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 | MySQL + SQLAlchemy (async) |
| 向量数据库 | Chroma |
| 大语言模型 | DeepSeek |
| 向量化 | 阿里云 DashScope |
| 文档解析 | pdfplumber, python-docx |
| 关键词检索 | BM25 (rank-bm25) |
| 精排模型 | Cross-Encoder (sentence-transformers) |
| 中文分词 | jieba |

## 📁 项目结构

\`\`\`
rag-agent/
├── models/          # 数据库模型
├── schemas/         # Pydantic 数据验证
├── crud/            # 数据库操作
├── routers/         # API 路由
├── services/        # 业务逻辑
├── utils/           # 工具函数（含检索优化器）
├── stock/           # 数据库连接
├── knowledge_data/  # 文档存放目录
├── main.py          # 程序入口
└── requirements.txt # 依赖清单
\`\`\`

## 🚀 快速开始

### 1. 克隆项目
\`\`\`bash
git clone https://github.com/你的用户名/rag-agent.git
cd rag-agent
\`\`\`

### 2. 创建虚拟环境
\`\`\`bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/Mac
source .venv/bin/activate
\`\`\`

### 3. 安装依赖
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. 配置环境变量
\`\`\`bash
cp .env.example .env
# 编辑 .env，填入你的 API 密钥
\`\`\`

### 5. 创建数据库
\`\`\`sql
CREATE DATABASE rag_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
\`\`\`

### 6. 启动服务
\`\`\`bash
python main.py
\`\`\`

### 7. 访问
- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/

## 🔍 检索优化说明

本系统在传统 RAG 基础上增加了三层优化：

1. **Query 改写**：用 LLM 把口语化问题改写成精准检索查询
2. **混合检索**：Chroma 向量检索 + BM25 关键词检索，互补召回
3. **Cross-Encoder 精排**：对粗排候选重新打分，提升 Top-K 准确率

\`\`\`
用户问题 → Query 改写 → 向量检索 + BM25 → 合并去重 → 精排 → LLM 生成
\`\`\`

## 📝 许可证

MIT License
