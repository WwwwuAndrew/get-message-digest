"""
配置管理模块
"""
import json
import os
from typing import Any, Dict


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """从配置文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config file: {e}")
                self.config = {}
        else:
            print(f"Warning: Config file '{self.config_file}' not found")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 点号分隔的键名（支持嵌套），如 "email.smtp_server"
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def __repr__(self) -> str:
        return f"Config(file='{self.config_file}')"
