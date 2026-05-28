# 📝 企业制度智能问答系统 - README.md

```markdown
# 企业制度智能问答系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange.svg)](https://deepseek.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-red.svg)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于RAG（检索增强生成）架构的企业内部制度智能问答助手。系统能够上传解析PDF/Word文档，自动建立知识库，并根据员工提问检索相关制度内容，生成准确回答。

## 核心功能

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| 用户管理 | 注册、登录、Token认证 | 完成 |
| 文档管理 | 上传PDF/Word，自动解析存储 | 完成 |
| 智能问答 | 基于DeepSeek大模型的语义理解 | 完成 |
| 知识库检索 | 向量化存储，语义相似度搜索 | 完成 |
| 对话管理 | 保存历史对话，支持多轮问答 | 完成 |
| 文档去重 | MD5自动去重，避免重复上传 | 完成 |

## 系统架构

```
用户注册 → 用户登录 → 获取Token → 上传文档 → 提问 → AI回答
                ↓                           ↓
           认证中间件                    检索+生成
```

详细架构流程：

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用户请求                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    API路由层 (routers/)                              │
│              接收请求、Token验证、返回响应                            │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    业务逻辑层 (services/)                            │
│              检索知识库、构建提示词、调用AI                           │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
        ┌───────────────────┐           ┌───────────────────┐
        │   知识库检索       │           │   大模型调用       │
        │   ChromaDB        │           │   DeepSeek        │
        │   向量相似度搜索   │           │   生成回答         │
        └───────────────────┘           └───────────────────┘
                    ↓                               ↓
        ┌───────────────────┐           ┌───────────────────┐
        │   文档解析         │           │   对话保存         │
        │   PDF/Word        │           │   MySQL           │
        │   文本切块         │           │   历史记录         │
        └───────────────────┘           └───────────────────┘
```

## 项目结构

```
rag-agent/
│
├── .env                      # 配置文件（API密钥、数据库密码）
├── requirements.txt          # 依赖清单
├── main.py                   # 程序入口
│
├── models/                   # 数据库模型
│   ├── base.py              # 基础模型
│   ├── user.py              # 用户表、Token表
│   ├── conversation.py      # 会话表
│   └── message.py           # 消息表
│
├── schemas/                  # Pydantic模型
│   ├── user.py              # 用户请求/响应格式
│   ├── conversation.py      # 会话格式
│   └── message.py           # 消息格式
│
├── crud/                     # 数据库操作
│   ├── user.py              # 用户CRUD
│   ├── conversation.py      # 会话CRUD
│   └── message.py           # 消息CRUD
│
├── routers/                  # API路由
│   ├── user.py              # 用户接口
│   ├── conversation.py      # 会话接口
│   └── chat.py              # 问答接口
│
├── services/                 # 业务逻辑层
│   └── chat_service.py      # 问答核心逻辑
│
├── utils/                    # 工具函数
│   ├── config.py            # 配置文件
│   ├── auth.py              # 密码加密、Token验证
│   ├── response.py          # 统一响应格式
│   ├── handle_text.py       # 知识库核心
│   └── document_service.py  # 文档解析服务
│
├── stock/                    # 数据库连接
│   └── db.py                # 异步数据库引擎
│
├── knowledge_data/           # 知识库文件存放目录
├── uploads/                  # 上传文件临时存放
├── data/                     # 数据文件目录
│   └── md5_records.txt      # MD5去重记录
│
└── db/                       # 向量数据库
    └── chroma_db/           # ChromaDB持久化目录
```

## 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 后端框架 | FastAPI | 高性能异步Web框架 |
| 数据库 | MySQL + SQLAlchemy | 关系型数据存储 |
| 向量数据库 | ChromaDB | 知识库向量存储和检索 |
| AI模型 | DeepSeek Chat | 大语言模型生成回答 |
| 向量化模型 | DashScope Embedding | 文本向量化 |
| 文档解析 | pdfplumber + python-docx | PDF和Word解析 |
| 文本切分 | LangChain RecursiveCharacterTextSplitter | 智能文本切块 |
| 认证方式 | Bearer Token | 用户身份认证 |

## 快速开始

### 环境要求

- Python 3.9+
- MySQL 5.7+
- DeepSeek API Key
- 阿里云DashScope API Key

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/pppyyz1233/rag-agent.git
cd rag-agent
```

#### 2. 创建虚拟环境

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

创建 `.env` 文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# 阿里云百炼配置（用于向量化）
DASHSCOPE_API_KEY=sk-your-dashscope-key-here

# 数据库配置
ASYNC_DATABASE_URL=mysql+aiomysql://root:123456@localhost:3306/rag_agent?charset=utf8
```

#### 5. 初始化数据库

```sql
-- 创建数据库
CREATE DATABASE rag_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE rag_agent;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) DEFAULT 'user',
    phone VARCHAR(12),
    avatar VARCHAR(255) DEFAULT 'default_avatar.png',
    bio VARCHAR(100) DEFAULT '这个人很懒，什么都没写',
    gender ENUM('male', 'female', 'unknow') DEFAULT 'unknow',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建Token表
CREATE TABLE IF NOT EXISTS user_token (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建会话表
CREATE TABLE IF NOT EXISTS conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NULL,
    title VARCHAR(100) DEFAULT '新对话',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
);

-- 创建消息表
CREATE TABLE IF NOT EXISTS messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    sources JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_conversation_id (conversation_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

#### 6. 启动服务

```bash
python main.py
```

服务启动后访问：
- API文档: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API接口文档

### 用户管理

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| POST | /api/user/register | 用户注册 | 否 |
| POST | /api/user/login | 用户登录 | 否 |
| GET | /api/user/info | 获取用户信息 | 是 |
| PUT | /api/user/revise | 修改用户信息 | 是 |
| PUT | /api/user/revise_password | 修改密码 | 是 |

### 会话管理

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| GET | /api/conversations/all_conversations | 获取会话列表 | 是 |
| POST | /api/conversations/creat_conversation | 创建会话 | 是 |
| PUT | /api/conversations/rename_conversation | 重命名会话 | 是 |
| DELETE | /api/conversations/{conversation_id} | 删除会话 | 是 |

### 智能问答

| 方法 | 路径 | 功能 | 认证 |
|------|------|------|------|
| POST | /api/chat | 智能问答 | 是 |
| GET | /api/chat/history/{conversation_id} | 获取聊天历史 | 是 |

## 使用示例

### 1. 注册用户

```bash
curl -X POST "http://127.0.0.1:8000/api/user/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"zhangsan","password":"123456"}'
```

响应：
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "username": "zhangsan",
    "nickname": "user"
  }
}
```

### 2. 用户登录

```bash
curl -X POST "http://127.0.0.1:8000/api/user/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"zhangsan","password":"123456"}'
```

响应：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "username": "zhangsan",
    "nickname": "user",
    "avatar": "default_avatar.png"
  }
}
```

### 3. 创建会话

```bash
curl -X POST "http://127.0.0.1:8000/api/conversations/creat_conversation" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"年假咨询"}'
```

响应：
```json
{
  "code": 200,
  "message": "创建会话成功",
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "年假咨询",
    "created_at": "2026-05-28T10:00:00",
    "updated_at": "2026-05-28T10:00:00"
  }
}
```

### 4. 智能问答

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"question":"公司年假有几天？","conversation_id":1}'
```

响应：
```json
{
  "code": 200,
  "message": "问答成功",
  "data": {
    "answer": "根据公司制度，入职满1年的员工享有5天带薪年假，满5年享有10天，满10年享有15天。",
    "sources": ["员工手册第3章第2条"],
    "conversation_id": 1,
    "message_id": 2,
    "is_new_conversation": false
  }
}
```

### 5. 上传文档到知识库

创建 `upload_knowledge.py`：

```python
import os
from utils.document_service import pdf_service, word_service

KNOWLEDGE_DIR = "knowledge_data"

def upload_all():
    files = os.listdir(KNOWLEDGE_DIR)
    for filename in files:
        file_path = os.path.join(KNOWLEDGE_DIR, filename)
        if filename.endswith('.pdf'):
            result = pdf_service(file_path, filename)
            print(f"PDF {filename}: {result}")
        elif filename.endswith('.docx'):
            result = word_service(file_path, filename)
            print(f"Word {filename}: {result}")

if __name__ == "__main__":
    upload_all()
```

运行：
```bash
python upload_knowledge.py
```

## 核心机制详解

### RAG工作流程

```
用户提问："年假有几天？"
    ↓
1. 知识库检索
   在ChromaDB中搜索相关制度内容
   返回最相似的3个文本片段
    ↓
2. 构建提示词
   系统提示词 + 检索到的制度内容 + 用户问题
    ↓
3. 调用DeepSeek
   大模型基于制度内容生成回答
    ↓
4. 保存对话
   保存用户问题和AI回答到MySQL
    ↓
5. 返回回答
   "根据公司制度，入职满1年的员工享有5天带薪年假..."
```

### 文本切块配置

| 参数 | 值 | 说明 |
|------|-----|------|
| CHUNK_SIZE | 500 | 每块最大500字 |
| CHUNK_OVERLAP | 100 | 重叠100字，防止切断重要内容 |
| MAX_SPLIT_CHAR_NUMBER | 1000 | 少于1000字不切割 |

### MD5去重机制

```
上传文档 → 计算MD5 → 检查记录文件 → 已存在则跳过 → 不存在则存入知识库
```

## 配置说明

### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| DEEPSEEK_API_KEY | DeepSeek API密钥 | sk-xxx |
| DASHSCOPE_API_KEY | 阿里云百炼密钥 | sk-xxx |
| ASYNC_DATABASE_URL | 数据库连接URL | mysql+aiomysql://... |

### 知识库配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| CHUNK_SIZE | 500 | 文本切块大小 |
| CHUNK_OVERLAP | 100 | 切块重叠大小 |
| TOP_K | 3 | 检索返回数量 |
| COLLECTION_NAME | knowledge-chroma | 向量集合名称 |

## 数据库设计

### 核心表结构

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| users | 用户表 | id, username, password |
| user_token | Token表 | user_id, token, expires_at |
| conversations | 会话表 | id, user_id, title |
| messages | 消息表 | conversation_id, role, content, sources |

### 表关系图

```
users (1) ──────< (N) user_token
   │
   └────────────< (N) conversations
                        │
                        └────────────< (N) messages
```

## 常见问题

### 1. 密码字段长度不够

错误：`Data too long for column 'password'`

解决：修改字段长度为255
```python
password: Mapped[str] = mapped_column(String(255), nullable=False)
```

### 2. Emoji无法存储

错误：`Incorrect string value: '\xF0\x9F\x98\x8A'`

解决：使用utf8mb4字符集
```sql
ALTER DATABASE rag_agent CHARACTER SET utf8mb4;
```

### 3. 文档解析失败

原因：PDF可能是扫描图片，没有文字层

解决：使用OCR工具先识别文字，或上传带文字层的PDF

### 4. 向量数据库连接失败

错误：`ChromaDB connection error`

解决：检查 `db/chroma_db/` 目录权限，确保有写入权限

## 扩展开发

### 添加新的文档格式支持

1. 在 `utils/document_service.py` 中添加解析函数

```python
def excel_service(file_path: str, filename: str):
    """解析Excel文件"""
    import pandas as pd
    df = pd.read_excel(file_path)
    text = df.to_string()
    return kb_service.upload_by_str(text, filename)
```

2. 在主函数中调用

### 调整检索参数

修改 `utils/config.py` 中的配置：

```python
TOP_K = 5           # 返回更多相关片段
CHUNK_SIZE = 800    # 更大的切块
```

## 许可证

MIT License

## 作者

pppyyz1233

- GitHub: [@pppyyz1233](https://github.com/pppyyz1233)

## 致谢

- FastAPI - 现代化Web框架
- DeepSeek - 大语言模型
- LangChain - LLM应用开发框架
- Chroma - 向量数据库
- SQLAlchemy - Python SQL工具包

---

如果这个项目对你有帮助，请给个Star。
```
