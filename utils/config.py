import os
from dotenv import load_dotenv

#从.env里加载变量
load_dotenv(override=True)

#项目的根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#deepseek大模型
DEEPSEEK_API_KEY  = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

#阿里云百炼
DASHSCOPE_API_KEY= os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_MODEL = "text-embedding-v4"

#chroma数据库
dashscope_model ="text-embedding-v4"
collection_name="knowledge-chroma"
persist_directory="db/chroma_db"

text_path = os.path.join(BASE_DIR, "knowledge_data")

#文本切割配置
chunk_size = 500
chunk_overlap = 100
separators= ["\n\n", "\n", "。", "；", "，", " ", ""]
max_splter_char_number = 1000


#md5存放路径
md5_path=os.path.join(BASE_DIR, "data", "md5_records.txt")

#回答问题数量
top_k = 3

