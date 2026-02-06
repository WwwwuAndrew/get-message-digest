"""爬取模块初始化文件"""
from crawlers.base import MessageCrawler
from crawlers.github_trending import GitHubTrendingCrawler

__all__ = [
    'MessageCrawler',
    'GitHubTrendingCrawler'
]
