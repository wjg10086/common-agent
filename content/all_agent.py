from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend # 导入FilesystemBackend
from base import configs as gc
from conn.llm import get_llm
from content.others import mybackend


class AllAgent:

    def __init__(self):
        prompt = f'''
        你是一个通用智能体，
        回答用户用中文。
        '''
        self.agent = create_deep_agent(
            model=get_llm(), # 传一个llm
            tools=[], # 工具函数列表
            # backend=FilesystemBackend(root_dir=gc.ROOT_PATH_AGENT,virtual_mode=True),
            backend=mybackend.create_session_backend,  # 设置后端
            system_prompt=prompt,
        )