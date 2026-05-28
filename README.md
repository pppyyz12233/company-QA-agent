# 📝 企业制度智能问答系统 - README.md

直接复制以下内容到你的 `rag-agent` 项目的 `README.md` 文件中：

```markdown
# 📚 企业制度智能问答系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange.svg)](https://deepseek.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-red.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
基于 **RAG（检索增强生成）** 架构的企业内部制度智能问答助手。系统能够自动解析 PDF/Word 文档，构建知识库，并根据员工提问智能检索相关制度内容，生成准确回答。

## ✨ 核心功能

| 功能模块 | 说明 | 状态 |
|---------|------|------|
| 🔐 用户管理 | 注册、登录、Token认证 | ✅ |
| 📄 文档解析 | 支持 PDF、Word 文档自动解析 | ✅ |
| 🧠 知识库构建 | 文本切块、向量化存储、MD5去重 | ✅ |
| 💬 智能问答 | 基于DeepSeek大模型的语义理解 | ✅ |
| 🔍 语义检索 | 基于ChromaDB的向量相似度检索 | ✅ |
| 💾 对话管理 | 保存历史对话，支持多轮问答 | ✅ |
| 📊 引用来源 | 返回答案的参考来源 | ✅ |

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用户提问                                    │
│                    "年假有几天？"                                    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    API路由层 (routers/)                              │
│              接收请求、验证Token、返回响应                            │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    业务逻辑层 (services/)                            │
│              会话管理、检索上下文、构建提示词                          │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
        ┌───────────────────────────┼───────────────────────────┐
        ↓                           ↓                           ↓
┌───────────────┐       ┌───────────────────┐       ┌───────────────────┐
│  知识库检索    │       │   对话历史保存     │       │   AI生成回答       │
│  ChromaDB     │       │   MySQL          │       │   DeepSeek        │
│  向量相似度    │       │   多轮对话        │       │   流式输出         │
└───────────────┘       └───────────────────┘       └───────────────────┘
```

## 📁 项目结构

```
rag-agent/
│
├── .env                      # 🔐 配置文件（API密钥、数据库密码）
├── requirements.txt          # 📦 依赖清单
├── main.py                   # 🚪 程序入口
├── upload_knowledge.py       # 📤 知识库上传脚本
│
├── models/                   # 📊 数据库模型
│   ├── base.py              # 基础模型
│   ├── user.py              # 用户表 + Token表
│   ├── conversation.py      # 会话表
│   └── message.py           # 消息表
│
├── schemas/                  # 📝 Pydantic模型
│   ├── user.py              # 用户请求/响应格式
│   ├── conversation.py      # 会话格式
│   └── message.py           # 消息格式
│
├── crud/                     # 🗄️ CRUD操作
│   ├── user.py              # 用户注册、登录、Token管理
│   ├── conversation.py      # 会话创建、查询、删除
│   └── message.py           # 消息保存、查询
│
├── routers/                  # 🌐 API路由
│   ├── user.py              # 用户注册/登录接口
│   ├── conversation.py      # 会话管理接口
│   └── chat.py              # 智能问答接口
│
├── services/                 # 🧠 业务逻辑层
│   └── chat_service.py      # 问答核心逻辑
│
├── utils/                    # 🛠️ 工具函数
│   ├── config.py            # 配置文件读取
│   ├── auth.py              # 密码加密、Token验证
│   ├── response.py          # 统一响应格式
│   ├── handle_text.py       # 知识库核心（向量化、检索、MD5）
│   └── document_service.py  # PDF/Word文档解析
│
├── stock/                    # 🔌 数据库连接
│   └── db.py                # 异步数据库引擎
│
├── knowledge_data/           # 📁 知识库文件存放目录
├── db/chroma_db/            # 🗄️ ChromaDB向量数据库
└── data/                    # 📁 数据存储（MD5记录等）
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- MySQL 5.7+
- DeepSeek API Key
- DashScope API Key（用于文本向量化）

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
# DeepSeek API 配置
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# 阿里云百炼配置（用于向量化）
DASHSCOPE_API_KEY=sk-your-dashscope-key-here

# 数据库配置
ASYNC_DATABASE_URL=mysql+aiomysql://root:123456@localhost:3306/rag_agent?charset=utf8mb4
```

#### 5. 初始化数据库

```sql
-- 创建数据库
CREATE DATABASE rag_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE rag_agent;

-- 创建用户表
CREATE TABLE users (
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
CREATE TABLE user_token (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建会话表
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NULL,
    title VARCHAR(100) DEFAULT '新对话',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
);

-- 创建消息表
CREATE TABLE messages (
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

#### 6. 上传知识库文档

将企业制度文档（PDF/Word）放入 `knowledge_data/` 目录，然后运行：

```bash
python upload_knowledge.py
```

#### 7. 启动服务

```bash
python main.py
```

服务启动后访问：
- **API文档**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📖 API 接口文档

### 用户管理

| 方法 | 路径 | 功能 | 请求体 |
|------|------|------|--------|
| POST | `/api/user/register` | 用户注册 | `{"username":"test","password":"123456"}` |
| POST | `/api/user/login` | 用户登录 | `{"username":"test","password":"123456"}` |
| GET | `/api/user/info` | 获取用户信息 | Header: Authorization |

### 会话管理

| 方法 | 路径 | 功能 | 说明 |
|------|------|------|------|
| GET | `/api/conversations/all_conversations` | 获取会话列表 | 返回最新会话 |
| POST | `/api/conversations/creat_conversation` | 创建会话 | `{"title":"新对话"}` |
| DELETE | `/api/conversations/{id}` | 删除会话 | - |
| PUT | `/api/conversations/rename_conversation` | 重命名会话 | `?conversation_id=1` |

### 智能问答

| 方法 | 路径 | 功能 | 请求体 |
|------|------|------|--------|
| POST | `/api/chat` | 智能问答 | `{"question":"年假有几天？","conversation_id":1}` |
| GET | `/api/chat/history/{conversation_id}` | 获取历史 | - |

## 💡 使用示例

### 1. 注册用户

```bash
curl -X POST "http://127.0.0.1:8000/api/user/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"张三","password":"123456"}'
```

**响应：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "username": "张三",
    "nickname": "user"
  }
}
```

### 2. 用户登录

```bash
curl -X POST "http://127.0.0.1:8000/api/user/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"张三","password":"123456"}'
```

**响应：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 1,
    "username": "张三",
    "nickname": "user"
  }
}
```

### 3. 智能问答

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"question":"年假有几天？","conversation_id":1}'
```

**响应：**
```json
{
  "code": 200,
  "message": "问答成功",
  "data": {
    "answer": "根据公司制度，入职满1年的员工享有5天年假，满3年享有10天年假。",
    "sources": ["员工手册_第3章_休假制度.docx"],
    "conversation_id": 1,
    "message_id": 3,
    "is_new_conversation": false
  }
}
```

### 4. 获取对话历史

```bash
curl -X GET "http://127.0.0.1:8000/api/chat/history/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 核心机制详解

### RAG 工作流程

```
用户提问："年假有几天？"
    ↓
1. 向量化问题
    ↓
2. ChromaDB 语义检索
    找到最相关的3个文本片段
    ↓
3. 构建提示词
    system: "你是企业制度助手，严格根据以下内容回答..."
    context: "员工手册：入职满1年享5天年假..."
    question: "年假有几天？"
    ↓
4. DeepSeek 生成回答
    ↓
5. 保存对话并返回
```

### 知识库构建流程

```
PDF/Word 文档
    ↓
1. 提取文字内容
    ↓
2. 计算 MD5（去重检查）
    ↓
3. 文本切块（chunk_size=500, overlap=100）
    ↓
4. DashScope 向量化
    ↓
5. 存入 ChromaDB
```

### 文本切块配置

| 参数 | 值 | 说明 |
|------|-----|------|
| CHUNK_SIZE | 500 | 每块最大500字 |
| CHUNK_OVERLAP | 100 | 重叠100字（防止切断重要内容） |
| MAX_SPLIT_CHAR_NUMBER | 1000 | 少于1000字不切割 |

## 📊 数据库设计

### 核心表结构

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `users` | 用户表 | id, username, password |
| `user_token` | Token表 | user_id, token, expires_at |
| `conversations` | 会话表 | id, user_id, title |
| `messages` | 消息表 | conversation_id, role, content, sources |

### 消息表 sources 字段示例

```json
[
  "员工手册_第3章_休假制度.docx",
  "公司福利制度.pdf"
]
```

## 🐛 常见问题

### 1. 密码字段长度不够

**错误：** `Data too long for column 'password'`

**解决：** 修改字段长度为255
```python
password: Mapped[str] = mapped_column(String(255), nullable=False)
```

### 2. Emoji 无法存储

**错误：** `Incorrect string value: '\xF0\x9F\x98\x8A'`

**解决：** 使用 utf8mb4 字符集
```sql
ALTER DATABASE rag_agent CHARACTER SET utf8mb4;
```

### 3. 知识库检索无结果

**可能原因：**
- 文档未上传
- 提问与制度内容不相关
- 向量数据库未初始化

**解决：**
```bash
# 检查知识库文件
ls knowledge_data/

# 重新上传
python upload_knowledge.py
```

### 4. API Key 无效

**错误：** `Authentication failed`

**解决：** 检查 `.env` 文件中的 API Key 是否正确

## 🚀 扩展开发

### 添加新的文档格式

1. **在 `utils/document_service.py` 中添加解析函数**

```python
def excel_service(file_path: str, filename: str):
    """解析Excel文件"""
    import pandas as pd
    df = pd.read_excel(file_path)
    text = df.to_string()
    return kb_service.upload_by_str(text, filename)
```

2. **在 `upload_knowledge.py` 中注册**

```python
elif filename.endswith('.xlsx'):
    result = excel_service(file_path, filename)
```

### 调整检索参数

在 `utils/config.py` 中修改：

```python
TOP_K = 5              # 返回更多结果
CHUNK_SIZE = 800       # 更大的文本块
```

## 📄 许可证

MIT License

## 👤 作者

**pppyyz1233**

- GitHub: [@pppyyz1233](https://github.com/pppyyz1233)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Web框架
- [DeepSeek](https://deepseek.com/) - 大语言模型
- [LangChain](https://www.langchain.com/) - LLM应用开发框架
- [Chroma](https://www.trychroma.com/) - 向量数据库

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**

**📚 完整教程：[零基础从零搭建企业制度智能问答系统](./TUTORIAL.md)**
```

