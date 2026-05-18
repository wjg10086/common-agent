import base64
import os


def save_base64_file_from_content_block(content_block,save_dir):
    """
    从 content_block 中提取 base64 数据并保存为文件
    Args:
        content_block: 包含 base64 数据的字典，从Agent Chat UI前端传来的数据
        save_dir: 保存目录

    Returns:
        Dict: 包含文件信息的字典
    """
    return save_base64_file(
        base64_data=content_block["data"],
        filename=content_block["metadata"]["filename"],
        save_dir=save_dir
    )

def save_base64_file(
        base64_data: str,
        filename: str,
        save_dir: str
):
    """
    将 base64 数据保存为文件

    Args:
        base64_data: base64 编码的字符串
        filename: 原始文件名
        save_dir: 保存目录

    Returns:
        Dict: 包含文件信息的字典
    """

    file_path = os.path.join(save_dir, filename)
    # 解码 base64 数据
    file_data = base64.b64decode(base64_data)

    # 保存文件
    with open(file_path, 'wb') as f:
        f.write(file_data)

    return {
        "success": True,
        "file_path": str(file_path),
        "filename": filename,
    }

import base64
import mimetypes

def image_to_data_url(file_path):
    """生成完整的data URL（包含MIME类型）"""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'image/jpeg'  # 默认类型
    with open(file_path, 'rb') as image_file:
        base64_data = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"