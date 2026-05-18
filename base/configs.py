import os
from dotenv import load_dotenv # 导入load_dotnev(可有可无)

from utils.general_utils.globle_util import get_platform

load_dotenv()  # 默认加载启动时当前目录下的 .env 文件 (可有可无)

ROOT_PATH_AGENT = '/agent_files'

BASE_LLM = os.getenv("BASE_LLM") # 从环境变量中获取模型
BASE_URL = os.getenv("MODEL_API_BASE_URL") # 从环境变量中获取base_url

LOG_DIR = os.path.dirname(__file__) # 当前脚本所在目录
NEED_CONSOLE_LOG = True # 日志是否打印到控制台


# gent工作的根目录样式如果是Windows系统则加上 C 盘的前置，否则保持原样
ROOT_PATH_SYSTEM = f'C:/{ROOT_PATH_AGENT}' if get_platform()==0 else ROOT_PATH_AGENT  # 系统工作根目录

HOST_IP = os.getenv("HOST_IP")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_ENDPOINT = f"{HOST_IP}:{MINIO_PORT}"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

USER_UPLOAD_PATH = 'user_uploads'    # 用户上传文件保存目录

ROOT_SYSTEM = 'fD:/' if get_platform()==0 else '/'  # 系统根目录

WAIT_RATE_LIMIT_SEC = 90 # 等待wait_rate_limit的间隔
WAIT_RATE_LIMIT_RETRY = 3 # 重试次数

BASE_VLM = os.getenv("BASE_VLM")  # VLM 模型
IMAGE_MODEL = os.getenv("IMAGE_MODEL") # 基础生图模型
EDIT_IMAGE_MODEL = os.getenv("EDIT_IMAGE_MODEL") # 修改图像模型
SILICON_API_KEY = os.getenv("OPENAI_API_KEY") # 引入一下硅基流动的API_KEY因为调用生图模型无法利用langchain本身框架。
GENERATE_IMAGE_PATH = 'generate_images'  # 生成图片保存目录