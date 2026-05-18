from langchain_openai import ChatOpenAI
from base import configs as gc

def get_llm():
    llm = ChatOpenAI(
            model=gc.BASE_LLM,
            base_url=gc.BASE_URL,
            temperature=0.1,
        )
    return llm

def get_small_llm():
    llm = ChatOpenAI(
            model='Qwen/Qwen3-30B-A3B-Instruct-2507',
            base_url=gc.BASE_URL,
            temperature=0.1,
        )
    return llm

def get_vlm():
    vlm = ChatOpenAI(
            model=gc.BASE_VLM,
            base_url=gc.BASE_URL,
    )
    return vlm