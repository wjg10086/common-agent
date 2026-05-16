from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend # 导入FilesystemBackend
from base import configs as gc
from conn.llm import get_llm
from content.middles import file_manager_middle
from content.others import mybackend
from utils.langchain_utils import common_utils as cu, stream_util
from utils.loggers import logger
from content.mytools import globle_tools as gt
from content.mytools import (
                             globle_tools as gt,
                             read_doc_tools, # 阅读文件工具
                             write_doc_tools # 写入文件工具
                            )


class AllAgent:

    def __init__(self):
        prompt = f'''
                  你是一个通用智能体，
                  读取ppt,doc,xls,pdf等文件时优先使用get_file_content,
                  注意调用write_file与edit_file时，需要有file_path和content参数，content是文件内容，也就是说你需要先写内容，然后调用write_file保存文件，或者用edit_file修改文件；
                  直到完成任务前，都不要停止。
                  回答用户用中文。
                  '''

        self.agent = create_deep_agent(
            model=get_llm(),
            tools=self._get_tools(),
            middleware=self._get_middlewares(),
            backend=mybackend.create_session_backend,
            system_prompt=prompt,

        )
        logger.info("common-agent init success.")

    def _get_tools(self):
        tools = [  # 配置读写文件工具
            read_doc_tools.get_file_content,
            write_doc_tools.convert_file,
        ]
        tools.extend(gt.get_tools())
        return tools

    def _get_middlewares(self):
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