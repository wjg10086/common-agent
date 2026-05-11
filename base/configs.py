import os
from dotenv import load_dotenv # 导入load_dotnev(可有可无)
load_dotenv()  # 默认加载启动时当前目录下的 .env 文件 (可有可无)

ROOT_PATH_AGENT = '/agent_files'

BASE_LLM = os.getenv("BASE_LLM") # 从环境变量中获取模型
BASE_URL = os.getenv("MODEL_API_BASE_URL") # 从环境变量中获取base_url

LOG_DIR = os.path.dirname(__file__) # 当前脚本所在目录
NEED_CONSOLE_LOG = True # 日志是否打印到控制台