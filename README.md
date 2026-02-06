# GitHub Trending Digest

获取 GitHub Trending 当日排名前10的仓库，通过 AI 进行内容总结，最后发送到指定的邮箱地址。

## 功能特性

✨ **核心功能**
- 🔍 自动爬取 GitHub Trending 排名前10的仓库
- 📄 获取每个仓库的 README 文件内容
- 🤖 使用智谱 AI (GLM) 进行自动总结
- 📧 生成格式化的 HTML 邮件并发送

🚀 **架构特性**
- 模块化设计：清晰的爬取器、处理器架构
- 易于扩展：支持轻松添加新的爬取源和处理器
- 配置管理：JSON 配置文件，无需修改代码
- 错误处理：完善的异常处理和日志输出

## 项目结构

```
get-message-digest/
├── crawlers/                     # 消息爬取模块
│   ├── base.py                   # MessageCrawler 基础类
│   └── github_trending.py        # GitHub Trending 爬取器
├── processors/                   # 消息处理模块
│   ├── base.py                   # MessageProcessor 基础类
│   ├── ai_processor.py           # AI 总结处理器
│   └── email_processor.py        # 邮件发送处理器
├── utils/                        # 工具模块
│   └── config.py                 # 配置管理
├── main.py                       # 主程序入口
├── config.json.example           # 配置文件模板
├── requirements.txt              # Python 依赖
├── design.md                     # 设计文档
├── README.md                     # 本文件
└── LICENSE                       # MIT 许可证
```

## 快速开始

### 前置要求
- Python 3.8+
- 智谱 AI API Key
- 可用的 SMTP 邮箱（推荐 Gmail）

### 安装步骤

1. **克隆或下载项目**
```bash
cd get-message-digest
```

2. **创建配置文件**
```bash
cp config.json.example config.json
```

3. **编辑配置文件** - 修改 `config.json` 中的以下信息：

```json
{
  "ai": {
    "api_key": "your-zhipu-api-key"
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "target@example.com"
  }
}
```

4. **安装依赖**
```bash
pip install -r requirements.txt
```

5. **运行程序**
```bash
python main.py
```

## 配置说明

### 智谱 AI 配置

1. 访问 [智谱 AI 官网](https://open.bigmodel.cn)
2. 注册并登录账号
3. 进入"我的 API"页面，创建新的 API 密钥
4. 复制 API Key 到 `config.json` 中的 `ai.api_key`

### Gmail 邮箱配置

1. 启用"两步验证"
2. 生成"应用专用密码" (App Password)
   - 访问 [Google 账户安全设置](https://myaccount.google.com/security)
   - 选择"应用专用密码"
   - 选择"邮件"和"Windows 电脑"
   - 生成密码并复制
3. 将应用专用密码填入 `config.json` 中的 `email.sender_password`

## 使用工作流

程序执行流程分为三个步骤：

```
Step 1: 消息提取 → GitHubTrendingCrawler → 爬取前10个仓库 README
                  ↓
Step 2: AI 总结 → AIProcessor → 用智谱 AI 总结内容
                  ↓
Step 3: 发送邮件 → EmailProcessor → 生成 HTML 邮件并发送
```

## 许可证

本项目采用 MIT 许可证。

---

**最后更新**：2026-02-05
