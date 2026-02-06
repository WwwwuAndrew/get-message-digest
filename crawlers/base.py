"""
消息爬取基础类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MessageCrawler(ABC):
    """消息爬取的基础类"""
    
    def __init__(self, name: str = "MessageCrawler"):
        """
        初始化爬取器
        
        Args:
            name: 爬取器的名称
        """
        self.name = name
        self.messages: List[Dict[str, Any]] = []
    
    @abstractmethod
    def crawl(self) -> List[Dict[str, Any]]:
        """
        爬取消息的抽象方法
        
        Returns:
            消息列表，每条消息为一个字典
        """
        pass
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """获取已爬取的消息"""
        return self.messages
    
    def clear_messages(self):
        """清空消息列表"""
        self.messages = []
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
