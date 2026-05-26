import hashlib
import os
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from crud import user
from utils import config
from utils.config import dashscope_model, DASHSCOPE_API_KEY, top_k


#md5计算
def transform_string_md5(input_str:str,encoding='utf-8'):
    input_bytes = input_str.encode(encoding=encoding)#将输入的转为utf-8
    md5_obj = hashlib.md5()#创建md5对象
    md5_obj.update(input_bytes)#添加数据给计算机计算

    return md5_obj.hexdigest()#md5值

#检查pdf是否已经上传过-看md5的值是不是一样的
def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w', encoding="utf-8").close()
        return False

    with open(config.md5_path,'r', encoding="utf-8") as f:
        for i in f:
            if i.strip() == md5_str:# strip()去除换行符和空格
                return True# 找到了，说明已经上传过

    return False# 没找到，是新文件

#保存新的md5
def save_md5(md5_str:str):
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + '\n')  #每行一个MD5



#知识库服务类
class KnowledgeBaseService:

    def __init__(self):

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model=dashscope_model),
            persist_directory = config.persist_directory#数据库文件存储位置
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,# 每块最大字符数
            chunk_overlap=config.chunk_overlap,# 块之间的重叠字符数（防止上下文断裂）
            separators=config.separators,# 优先按这些符号切割（保持句子完整）
            length_function=len,# 计算文本长度的函数
        )

#将文本内容存入知识库
    def upload_by_str(self, content: str, filename: str, operator: str = "admin"):
        """
            content: 要存储的文本内容
            filename: 来源文件名
        """
        md5 = transform_string_md5(content)#计算content(pdf里所有的文本信息)的md5值
        if check_md5(md5):
            return "文件已存在，跳过上传"

        #决定是否需要切块
        if len(content) <= config.max_splter_char_number:
            chunks = [content]  #直接为一块
        else:
            chunks = self.splitter.split_text(content)

        #准备元数据
        metadata = {
            "source": filename,  # 来自哪个文件
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 上传时间
            "operator":operator   # 上传者
        }

        if chunks:
            self.chroma.add_texts(
                chunks,
                metadatas=[metadata for _ in chunks]  # 每块都有相同的元数据
            )

            save_md5(md5)

            return "文档上传成功"

    def search(self, query: str):
        docs = self.chroma.similarity_search(query, k=top_k)

        return [(doc.page_content, doc.metadata) for doc in docs]


kb_service = KnowledgeBaseService()


#返回检索到的文本片段列表
def retrieve_context(query: str):
    results = kb_service.search(query)
    return [content for content, _ in results]
