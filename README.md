# 在本地创建 README.md
echo "# 企业制度智能问答系统

基于RAG技术的企业制度智能问答系统

## 功能
- 用户注册/登录
- 文档上传（PDF/Word）
- 智能问答
- 多轮对话

## 技术栈
- FastAPI + MySQL + ChromaDB
- DeepSeek API

## 快速开始
\`\`\`bash
pip install -r requirements.txt
python main.py
\`\`\`
" > README.md

git add README.md
git commit -m "Add README"
git push
