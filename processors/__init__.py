"""处理模块初始化文件"""
from processors.base import MessageProcessor
from processors.ai_processor import AIProcessor
from processors.email_processor import EmailProcessor

__all__ = [
    'MessageProcessor',
    'AIProcessor',
    'EmailProcessor'
]
