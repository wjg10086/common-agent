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