#!/usr/bin/env python3
"""
GitHub Trending Digest - 主程序

功能流程：
1. 爬取 GitHub Trending 页面当天前10个仓库的 README
2. 使用智谱 AI 对 README 进行总结
3. 将总结后的内容发送到指定的邮箱
"""

import sys
import os
from datetime import datetime
from utils.config import Config
from crawlers.github_trending import GitHubTrendingCrawler
from processors.ai_processor import AIProcessor
from processors.email_processor import EmailProcessor


def main():
    """主函数"""
    
    print("=" * 60)
    print("GitHub Trending Digest")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载配置
    config = Config('config.json')
    
    # 验证必要的配置
    if not _validate_config(config):
        print("\n❌ Configuration validation failed!")
        print("Please create config.json based on config.json.example")
        sys.exit(1)
    
    # 第一步：爬取消息
    print("\n[Step 1] Crawling GitHub Trending...")
    try:
        crawler = GitHubTrendingCrawler(
            language=config.get('github.language', ''),
            since=config.get('github.since', 'daily')
        )
        messages = crawler.crawl()
        
        if not messages:
            print("❌ Failed to crawl repositories")
            sys.exit(1)
        
        print(f"✅ Successfully crawled {len(messages)} repositories")
    
    except Exception as e:
        print(f"❌ Error during crawling: {e}")
        sys.exit(1)
    
    # 第二步：AI 总结
    print("\n[Step 2] Processing with AI...")
    try:
        ai_processor = AIProcessor(
            api_key=config.get('ai.api_key'),
            model=config.get('ai.model', 'glm-4-flash')
        )
        messages = ai_processor.process(messages)
        print(f"✅ Successfully processed {len(messages)} messages")
    
    except Exception as e:
        print(f"❌ Error during AI processing: {e}")
        print("⚠️  Continuing without AI summaries...")
    
    # 第三步：发送邮件
    print("\n[Step 3] Sending emails...")
    try:
        email_processor = EmailProcessor(
            smtp_server=config.get('email.smtp_server'),
            smtp_port=config.get('email.smtp_port', 587),
            sender_email=config.get('email.sender_email'),
            sender_password=config.get('email.sender_password'),
            recipient_email=config.get('email.recipient_email')
        )
        results = email_processor.process(messages)
        print(f"✅ Successfully sent email")
    
    except Exception as e:
        print(f"❌ Error during email sending: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tasks completed successfully!")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def _validate_config(config: Config) -> bool:
    """
    验证配置文件中的必要字段
    
    Args:
        config: 配置对象
        
    Returns:
        配置是否有效
    """
    required_fields = [
        'ai.api_key',
        'email.smtp_server',
        'email.sender_email',
        'email.sender_password',
        'email.recipient_email'
    ]
    
    missing_fields = []
    for field in required_fields:
        value = config.get(field)
        if not value or value == f'YOUR_{field.upper().replace(".", "_")}_HERE':
            missing_fields.append(field)
    
    if missing_fields:
        print(f"\n❌ Missing or invalid configuration fields:")
        for field in missing_fields:
            print(f"  - {field}")
        return False
    
    return True


if __name__ == '__main__':
    main()
