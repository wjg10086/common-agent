from utils.doc_utils import markitdown_util
from langchain.tools import tool

@tool
def get_file_content(filepath):
    """
    阅读文件的工具，支持ppt,doc,xls,pdf
    :param filepath: 文件地址
    :return: str 文件内容
    """
    result = markitdown_util.get_file_content(filepath)
    return result