import asyncio
import time
from langchain.agents.middleware import AgentState, AgentMiddleware
from utils.doc_utils import os_util as ou
from utils.general_utils.globle_util import get_uuid
from content.utils import runtime_util as rt
from langchain.messages import ToolMessage, AIMessage
from utils.doc_utils.zip_files import compress_dir
from conn.minio_conn import MinioConn
from base.configs import USER_UPLOAD_PATH
from content.utils import base64_util as bu
import os

class CustomState(AgentState):
    """
    自定义Agent状态类，扩展LangChain的AgentState
    """
    start_work_time: float  # Agent工作开始的时间戳
    file_update_time: float  # 文件最后更新时间戳，用于检测文件变化
    upload_files: list  # 用户上传的文件列表


class FileMiddleware(AgentMiddleware[CustomState]):

    state_schema = CustomState  # 指定使用的状态类

    def __init__(self):
        super().__init__()
        self.mc = MinioConn()  # MinIO对象存储连接实例

    async def _check_if_new_file(self, folder_path, work_start_time):
        """
        检查文件夹中是否有比指定时间更新的文件

        参数:
        folder_path: str - 要检查的文件夹路径
        work_start_time: float - 参考时间戳

        返回:
        bool: 如果存在比work_start_time更新的文件返回True，否则False
        """
        # 异步执行文件时间检查，避免阻塞事件循环
        max_time = await asyncio.to_thread(ou.get_folder_file_update_time_max, folder_path)
        return max_time > work_start_time  # 比较最新文件时间与参考时间

    async def abefore_model(self, state, runtime):
        """
        Agent调用模型前的钩子函数

        功能: 检查工作目录是否有新文件，如果有则生成目录结构信息
        触发条件: 文件更新时间晚于状态中记录的时间
        """
        DIR_PATH = rt.get_root_thread_dir()  # 获取当前线程的工作目录
        # 检查是否有新文件加入工作目录
        if await self._check_if_new_file(DIR_PATH, state['file_update_time']):
            # 生成美观的目录树结构描述
            content = f'当前目录结构:\n{ou.get_directory_tree(DIR_PATH)}'

            # 返回ToolMessage给模型，包含目录结构信息
            return {
                "messages": [ToolMessage(
                    content=content,
                    tool_call_id=get_uuid(),  # 生成唯一工具调用ID
                    name="summary_file_paths"  # 工具名称
                )],
                "file_update_time": time.time()  # 更新文件检测时间
            }

    async def abefore_agent(self, state, runtime):
        """
        Agent执行前的钩子函数

        功能: 处理用户上传的文件，保存到本地工作目录
        主要任务:
        1. 创建用户上传目录
        2. 将base64编码的文件保存为本地文件
        3. 初始化Agent工作状态
        """
        # 获取当前时间戳，用于状态管理
        file_update_time = time.time()

        # 转换用户上传路径为当前线程的绝对路径
        dir_path = os.path.join(rt.get_root_thread_dir(), USER_UPLOAD_PATH)

        # 异步创建目录（如果不存在）
        await asyncio.to_thread(os.makedirs, dir_path, exist_ok=True)

        # 获取用户上传的文件列表
        files = state.get('upload_files')

        if files:  # 如果有上传的文件
            content = f'用户上传了如下文件,已下载,文件路径如下:'

            # 遍历所有上传的文件
            for file in files:
                # 异步保存base64编码的文件到本地
                r = await asyncio.to_thread(
                    bu.save_base64_file_from_content_block,
                    file,
                    dir_path
                )
                # 将绝对路径转换为相对路径，便于显示
                content += f"\n{rt.get_out_path(r['file_path'])}"

            # 返回处理结果并更新状态
            return {
                "messages": [ToolMessage(
                    content=content,
                    tool_call_id=get_uuid(),
                    name="file_upload"  # 文件上传工具
                )],
                "upload_files": None,  # 清空上传文件列表
                "start_work_time": time.time(),  # 记录工作开始时间
                "file_update_time": file_update_time  # 更新文件时间
            }
        else:
            # 没有上传文件时，只更新时间状态
            return {
                "start_work_time": file_update_time,
                "file_update_time": file_update_time
            }

    async def awrap_tool_call(self, request, handler):
        # 执行实际工具调用
        tool_result = await handler(request)

        # 在工具调用后：将绝对路径转换回相对路径
        if isinstance(tool_result, ToolMessage):
            # 只转换内容中的路径，其他信息保持不变
            tool_result.content = rt.get_out_path(tool_result.content)

        return tool_result

    async def aafter_agent(self, state, runtime):
        """
        Agent执行后的钩子函数

        功能: 检查工作期间是否有新文件产生，如果有则打包上传
        主要任务:
        1. 检查文件变化
        2. 压缩工作目录
        3. 上传到MinIO对象存储
        4. 生成下载链接
        """
        DIR_PATH = rt.get_root_thread_dir()  # 获取工作目录

        # 检查工作期间是否有新文件产生
        if await self._check_if_new_file(DIR_PATH, state['start_work_time']):
            # 1. 异步压缩工作目录
            local_p = await asyncio.to_thread(compress_dir, DIR_PATH)

            # 2. 上传到MinIO对象存储
            obj_path = os.path.basename(local_p)  # 获取压缩文件名
            # 异步上传
            await asyncio.to_thread(self.mc.upload_obj, obj_path, local_p)

            # 3. 生成预签名下载URL（带有效期）
            url = self.mc.gen_presigned_url(obj_path)

            # 返回下载链接给用户
            return {
                "messages": [
                    AIMessage(content='可通过如下地址下载:'),
                    AIMessage(content=url)
                ]
            }
        else:
            # 没有新文件，不执行任何操作
            return None