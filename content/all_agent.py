from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend # 导入FilesystemBackend
from base import configs as gc
from conn.llm import get_llm
from content.middles import file_manager_middle
from content.others import mybackend
from utils.langchain_utils import common_utils as cu, stream_util
from utils.loggers import logger
from content.mytools import globle_tools as gt


class AllAgent:

    def __init__(self):
        prompt = f'''
        你是一个通用智能体，
        回答用户用中文。
        '''
        self.agent = create_deep_agent(
            model=get_llm(), # 传一个llm
            tools=self._get_tools(), # 工具函数列表
            middleware=self._get_middlewares(),  # 中间件列表
            # backend=FilesystemBackend(root_dir=gc.ROOT_PATH_AGENT,virtual_mode=True),
            backend=mybackend.create_session_backend,  # 设置后端
            system_prompt=prompt,
        )
        logger.info("common-agent init success.")

    def _get_tools(self):
        tools = gt.get_tools()
        return tools

    def _get_middlewares(self):  # 中间件
        return [
            file_manager_middle.FileMiddleware()
        ]



# if __name__ == '__main__':
#     agent = AllAgent()
#     cu.save_graph_img(agent, 'agent.png')
#
#     stream_util.stream_log(agent, '你好')
#
#     stream_util.stream_print_tokens(agent, '你好')
#
#     stream_util.stream_both(agent, '你好')