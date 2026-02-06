"""
消息处理基础类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MessageProcessor(ABC):
    """消息处理的基础类"""
    
    def __init__(self, name: str = "MessageProcessor"):
        """
        初始化处理器
        
        Args:
            name: 处理器的名称
        """
        self.name = name
        self.results: List[Dict[str, Any]] = []
    
    @abstractmethod
    def process(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        处理消息的抽象方法
        
        Args:
            messages: 待处理的消息列表
            
        Returns:
            处理后的消息列表
        """
        pass
    
    def get_results(self) -> List[Dict[str, Any]]:
        """获取处理结果"""
        return self.results
    
    def clear_results(self):
        """清空处理结果"""
        self.results = []
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
