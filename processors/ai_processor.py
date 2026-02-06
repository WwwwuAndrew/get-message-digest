"""
AI 总结处理器 - 使用智谱 AI 进行消息总结
"""
from time import sleep
import requests
from typing import Any, Dict, List
from processors.base import MessageProcessor


class AIProcessor(MessageProcessor):
    """使用智谱 AI 进行消息总结的处理器"""
    
    def __init__(self, api_key: str, model: str = "glm-4-flash"):
        """
        初始化 AI 处理器
        
        Args:
            api_key: 智谱 AI API 密钥
            model: 使用的模型名称（默认为 glm-4-flash）
        """
        super().__init__(name="ZhipuAIProcessor")
        self.api_key = api_key
        self.model = model
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def process(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        使用 AI 处理消息（总结 README 内容）
        
        Args:
            messages: 待处理的消息列表（包含 README 内容）
            
        Returns:
            处理后的消息列表（包含 AI 总结）
        """
        self.results = []
        
        for i, message in enumerate(messages):
            print(f"Processing message {i+1}/{len(messages)}: {message.get('repo_name', 'Unknown')}")
            
            readme = message.get('readme', '')
            if not readme or readme.startswith('['):
                # README 为空或获取失败
                summary = "[Unable to summarize: No README content available]"
            else:
                summary = self._summarize_readme(readme, message.get('repo_name', 'Unknown'))
            
            processed_message = {
                **message,
                "summary": summary
            }
            
            self.results.append(processed_message)
            sleep(3)  # 避免过快请求 API
        
        print(f"Successfully processed {len(self.results)} messages")
        return self.results
    
    def _summarize_readme(self, readme_content: str, repo_name: str) -> str:
        """
        使用智谱 AI 总结 README 内容
        
        Args:
            readme_content: README 文件内容
            repo_name: 仓库名称
            
        Returns:
            总结后的内容
        """
        try:
            prompt = f"""请简洁地总结这个 GitHub 仓库 '{repo_name}' 的 README 内容。
总结应该包括：
1. 项目的主要功能和目的
2. 主要特性
3. 使用场景

请用中文回答，控制在 500 字以内。

README 内容：
{readme_content}
"""
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "thinking": {               
                    "type": "disabled"                                                         
                },
                "temperature": 1.0,
                "max_tokens": 65536
            }
            for i in range(3):
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                print(f"AI API response : {response.content.decode('utf-8')}")
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        summary = data['choices'][0]['message']['content']
                        return summary.strip()
                    elif 'error' in data and 'code' in data['error'] and data['error']['code'] == 1302:
                        sleep(30)
                        continue
                    else:
                        raise Exception(f"Unexpected API response: {data}")
                else:
                    return f"[Error: API returned status {response.status_code}]"
            raise Exception("API rate limit exceeded after 3 attempts")
        except Exception as e:
            print(f"Error summarizing README for {repo_name}: {e}")
            return f"[Error: {str(e)}]"
