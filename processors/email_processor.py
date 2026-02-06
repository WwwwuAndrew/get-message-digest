"""邮件发送处理器"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict, List
from datetime import datetime
import markdown
from processors.base import MessageProcessor


class EmailProcessor(MessageProcessor):
    """发送邮件的处理器"""
    
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, 
                 sender_password: str, recipient_email: str):
        """
        初始化邮件处理器
        
        Args:
            smtp_server: SMTP 服务器地址
            smtp_port: SMTP 服务器端口
            sender_email: 发送者邮箱
            sender_password: 发送者密码/授权码
            recipient_email: 接收者邮箱
        """
        super().__init__(name="EmailProcessor")
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
    
    def process(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将处理后的消息发送到邮箱
        
        Args:
            messages: 待发送的消息列表（应包含 summary 字段）
            
        Returns:
            处理结果列表
        """
        self.results = []
        
        try:
            email_content = self._generate_email_content(messages)
            self._send_email(email_content)
            
            for message in messages:
                self.results.append({
                    **message,
                    "email_sent": True,
                    "sent_at": datetime.now().isoformat()
                })
            
            print(f"Successfully sent email with {len(messages)} repositories")
        
        except Exception as e:
            print(f"Error sending email: {e}")
            for message in messages:
                self.results.append({
                    **message,
                    "email_sent": False,
                    "error": str(e)
                })
        
        return self.results
    
    def _generate_email_content(self, messages: List[Dict[str, Any]]) -> str:
        """
        生成邮件内容（HTML 格式）
        
        Args:
            messages: 消息列表
            
        Returns:
            HTML 格式的邮件内容
        """
        html_content = """
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                .repo-item { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
                .repo-name { font-size: 18px; font-weight: bold; color: #0366d6; margin-bottom: 5px; }
                .repo-description { color: #666; margin-bottom: 10px; }
                .repo-meta { font-size: 12px; color: #999; margin-bottom: 10px; }
                .summary { background-color: #f8f9fa; padding: 10px; border-left: 4px solid #0366d6; margin-top: 10px; }
                .footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>GitHub Trending 日报</h1>
                    <p>生成时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                </div>
        """
        
        for i, message in enumerate(messages, 1):
            summary = message.get('summary', '[No summary available]')
            summary_html = markdown.markdown(summary)
            
            html_content += f"""
                <div class="repo-item">
                    <div class="repo-name">{i}. <a href="{message.get('repo_url', '#')}" target="_blank">{message.get('repo_name', 'Unknown')}</a></div>
                    <div class="repo-description">{message.get('description', 'No description')}</div>
                    <div class="repo-meta">
                        🌍 Language: {message.get('language', 'Unknown')} | 
                        ⭐ Stars: {message.get('stars', 'N/A')} | 
                        👤 Owner: {message.get('owner', 'Unknown')}
                    </div>
                    <div class="summary">
                        <strong>📝 AI 总结：</strong><br>
                        {summary_html}
                    </div>
                </div>
            """
        
        html_content += """
                <div class="footer">
                    <p>由 GitHub Trending Digest 自动生成</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _send_email(self, html_content: str):
        """
        发送邮件
        
        Args:
            html_content: HTML 格式的邮件内容
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart('alternative')
            message['Subject'] = f'GitHub Trending 日报 - {datetime.now().strftime("%Y-%m-%d")}'
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            
            # 添加 HTML 内容
            part = MIMEText(html_content, 'html', _charset='utf-8')
            message.attach(part)
            
            # 发送邮件
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"Email sent successfully to {self.recipient_email}")
        
        except Exception as e:
            print(f"Error sending email: {e}")
            raise
