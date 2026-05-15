import os
from base import configs as gc

from langchain_core.runnables.config import var_child_runnable_config

def get_thread_id(runtime=None):
    # 从 runtime config 中获取 thread_id
    config = getattr(runtime, 'config', None)
    if config is None:
        configurable = getattr(runtime, 'context', None)
    else:
        configurable = config.get('configurable', None)

    # 从 var_child_runnable_config
    if configurable is None and var_child_runnable_config.get() is not None:
        configurable = var_child_runnable_config.get().get("configurable", {})
    if configurable is None:
        return 'default'
    thread_id = configurable.get('thread_id', 'default')
    return thread_id


def get_root_thread_dir():
    """
    获取当前线程的专属根目录路径

    功能描述：
    1. 将系统根路径与当前线程ID组合，生成线程专用的目录路径
    2. 对路径进行规范化处理，确保路径格式统一

    返回:
    str: 当前线程的专属目录路径（标准化格式）

    示例:
    如果 ROOT_PATH_SYSTEM = "C:\\temp"
    get_thread_id() 返回 "thread_123"
    则返回 "C:\\temp\\thread_123"
    """
    # 将系统根目录路径与当前线程ID拼接，生成完整路径
    # os.path.join: 智能拼接路径，自动处理不同操作系统的路径分隔符
    # get_thread_id(): 原有方法，获取当前线程的唯一标识符
    raw_path = os.path.join(gc.ROOT_PATH_SYSTEM, get_thread_id())

    # 规范化路径，处理路径中的冗余部分（如 '..', '.', 多余的斜杠等）
    # 例如: "C:\\temp\\thread_123\\..\\thread_123" → "C:\\temp\\thread_123"
    normalized_path = os.path.normpath(raw_path)

    return normalized_path


def get_out_path(file_path):
    """
    从完整的文件路径中提取相对于线程目录的相对路径

    功能描述：
    1. 获取线程根目录路径并添加路径分隔符
    2. 从完整文件路径中移除线程根目录部分，得到相对路径
    3. 用于将绝对路径转换为相对于线程目录的相对路径

    参数:
    file_path (str): 文件路径

    返回:
    str: 相对于线程根目录的文件路径（移除了线程目录前缀）, 如果线程根目录不存在，则返回原始路径

    示例:
    假设线程目录为 "C:\\temp\\thread_123"
    输入: "C:\\temp\\thread_123\\data\\file.txt"
    返回: "data\\file.txt"
    输入: "dir\\data\\file.txt"
    返回: "dir\\data\\file.txt"
    """
    # 如果输入不是字符串，则返回原始路径
    if type(file_path) != str:
        return file_path

    # 获取线程根目录并添加路径分隔符
    # 注意：这里使用 '\\' 作为分隔符，在跨平台场景中建议使用 os.path.sep
    thread_dir = get_root_thread_dir() + '\\'

    # 规范化输入的文件路径，确保格式一致
    # 这有助于后续的字符串替换操作更可靠
    file_path = os.path.normpath(file_path)

    # 从完整路径中移除线程根目录前缀，得到相对路径
    # 例如: "C:\\temp\\thread_123\\data\\file.txt" → "data\\file.txt"
    # 如果线程根目录不存在，则返回原始路径
    # 例如: "data\\file.txt" → "data\\file.txt"
    relative_path = file_path.replace(thread_dir, '')

    return relative_path