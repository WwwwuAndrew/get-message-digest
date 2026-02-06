"""
GitHub Trending 爬取器
"""
import requests
from typing import Any, Dict, List
from datetime import datetime
from bs4 import BeautifulSoup
from crawlers.base import MessageCrawler


class GitHubTrendingCrawler(MessageCrawler):
    """爬取 GitHub Trending 页面的爬取器"""
    
    def __init__(self, language: str = "", since: str = "daily"):
        """
        初始化 GitHub Trending 爬取器
        
        Args:
            language: 编程语言过滤（默认为空，表示全部）
            since: 时间范围，可选 'daily', 'weekly', 'monthly'（默认为 'daily'）
        """
        super().__init__(name="GitHubTrendingCrawler")
        self.language = language
        self.since = since
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = "https://github.com/trending"
    
    def crawl(self) -> List[Dict[str, Any]]:
        """
        爬取 GitHub Trending 前10个仓库的信息
        
        Returns:
            包含仓库信息和 README 的消息列表
        """
        self.messages = []
        
        try:
            # 获取 trending 页面
            repos = self._get_trending_repos()
            
            # 获取前10个仓库的 README
            for i, repo in enumerate(repos[:10]):
                print(f"Processing repo {i+1}/10: {repo['name']}")
                
                readme_content = self._get_readme(repo['owner'], repo['name'])
                
                message = {
                    "repo_name": repo['name'],
                    "repo_url": repo['url'],
                    "owner": repo['owner'],
                    "description": repo['description'],
                    "language": repo['language'],
                    "stars": repo['stars'],
                    "readme": readme_content,
                    "crawled_at": datetime.now().isoformat()
                }
                
                self.messages.append(message)
            
            print(f"Successfully crawled {len(self.messages)} repositories")
            
        except Exception as e:
            print(f"Error during crawling: {e}")
        
        return self.messages
    
    def _get_trending_repos(self) -> List[Dict[str, Any]]:
        """
        获取 GitHub Trending 页面的仓库列表
        
        Returns:
            仓库信息列表
        """
        repos = []
        
        try:
            url = self.base_url
            if self.language:
                url += f"/{self.language}"
            url += f"?since={self.since}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找所有仓库的 article 标签
            articles = soup.find_all('article', class_='Box-row')
            
            for article in articles:
                try:
                    # 提取仓库信息
                    repo_link = article.find('h2', class_='h3').find('a')
                    repo_path = repo_link.get('href', '').strip('/')
                    
                    if '/' in repo_path:
                        owner, name = repo_path.split('/', 1)
                    else:
                        continue
                    
                    description = article.find('p', class_='col-9')
                    description = description.text.strip() if description else ""
                    
                    language_tag = article.find('span', itemprop='programmingLanguage')
                    language = language_tag.text.strip() if language_tag else "Unknown"
                    
                    stars = "0"
                    star_span = article.find('span', class_='d-inline-block float-sm-right')
                    if star_span:
                        stars = star_span.text.strip().split()[0]
                    
                    repos.append({
                        'owner': owner,
                        'name': name,
                        'url': f"https://github.com/{repo_path}",
                        'description': description,
                        'language': language,
                        'stars': stars
                    })
                    
                except Exception as e:
                    print(f"Error parsing repo: {e}")
                    continue
            
        except Exception as e:
            print(f"Error fetching trending page: {e}")
        
        return repos
    
    def _get_readme(self, owner: str, repo: str) -> str:
        """
        获取仓库的 README 文件内容
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            
        Returns:
            README 内容，如果失败返回空字符串
        """
        try:
            # 尝试获取 README.md
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # 如果 main 分支不存在，尝试 master 分支
            if response.status_code == 404:
                url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
                response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                return "[README not found]"
        
        except Exception as e:
            print(f"Error fetching README for {owner}/{repo}: {e}")
            return f"[Error fetching README: {str(e)}]"
