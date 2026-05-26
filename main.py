import io
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import user, conversation, chat, upload_document

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
app = FastAPI(
    title="企业制度智能问答Agent",
    description="基于RAG的企业内部制度助手",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有域名访问（开发环境）
    allow_credentials=True,        # 允许携带认证信息
    allow_methods=["*"],           # 允许所有HTTP方法
    allow_headers=["*"],           # 允许所有请求头
)

app.include_router(user.router)
app.include_router(conversation.router)
app.include_router(chat.router)
app.include_router(upload_document.router)