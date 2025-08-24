# 🎬 AWS Blog RSS Analyzer Demo

## 快速演示

### 1. 项目概览
```
AWS Blog RSS Analyzer - 智能内容处理和差异化 AI 分析
• 智能 RSS 解析器
• 双重 AI 备用机制 
• 支持 20+ AWS RSS feeds
```

### 2. 核心文件
```
📁 项目结构:
├── rss_parser.py          # RSS 解析器
├── blog_analyzer.py       # AI 分析器
├── install_agent.sh       # 安装脚本
├── test_system.py         # 测试脚本
└── README.md             # 完整文档
```

### 3. 安装演示
```bash
$ ./install_agent.sh
正在安装 AWS Blog RSS Analyzer Agent...
📝 生成配置文件...
✅ Agent 安装完成！

📍 安装路径: /path/to/rss-parser
📄 配置文件: ~/.aws/amazonq/cli-agents/aws-blog-rss-analyzer.json

使用方法:
  q chat --agent aws-blog-rss-analyzer
```

### 4. 验证配置
```bash
$ python3 validate_config.py
✅ 配置模板文件存在
✅ 配置文件验证通过
   Agent 名称: aws-blog-rss-analyzer
   工具数量: 9
   资源数量: 3
```

### 5. RSS 解析演示
```bash
$ python3 rss_parser.py machine-learning 2025-08-17T00:00:00Z 2025-08-23T23:59:59Z
[
  {
    "title": "Enhance Geospatial Analysis and GIS Workflows with...",
    "link": "https://aws.amazon.com/blogs/machine-learning/...",
    "pub_date": "2025-08-22T15:30:00Z",
    "author": "AWS Team",
    "description": "Today, we are excited to announce...",
    "content_encoded": "Complete article content..."
  }
]
```

### 6. AI 分析器功能
```bash
$ python3 blog_analyzer.py --help

AWS Blog RSS Analyzer v2.0 - 智能内容处理和差异化AI分析

用法:
    python blog_analyzer.py <blog_type> <start_date> <end_date>
    python blog_analyzer.py -h|--help
    python blog_analyzer.py -v|--version

支持的博客类型:
    whats-new, machine-learning, database, security, compute...

技术特性:
    • 智能内容选择 (content:encoded vs description)
    • 差异化处理 (翻译 vs 摘要)
    • 双重AI备用 (Claude 3.7 + Nova Lite)
```

### 7. 系统测试
```bash
$ python3 test_system.py
AWS Blog RSS 系统测试
==================================================
=== 测试 RSS 解析器 ===
✅ RSS 解析器成功，获取 17 篇文章
✅ 文章结构完整
✅ 包含 content_encoded 字段

=== 测试博客分析器 ===
✅ 报告格式正确
✅ 博客分析器成功

总计: 4/4 项测试通过
🎉 所有测试通过！系统可以正常使用。
```

## 🚀 Amazon Q CLI Agent 使用

### 启动 Agent
```bash
q chat --agent aws-blog-rss-analyzer
```

### 示例对话
```
用户: "生成上周的AWS What's New更新摘要"
Agent: 正在分析 AWS What's New 更新...
       [生成中文翻译报告]

用户: "分析最近的机器学习博客文章"  
Agent: 正在分析机器学习博客...
       [生成中文摘要报告]
```

## 🎯 核心特性展示

### 智能内容处理
- **What's New**: 使用 `description` (适合翻译)
- **技术博客**: 使用 `content:encoded` (完整内容)

### 差异化 AI 分析
- **What's New**: 中文翻译 (保持信息完整性)
- **技术博客**: 中文摘要 (提取关键要点)

### 双重 AI 备用
- **Claude 3.7 Sonnet**: 主要模型 (250次/分钟)
- **Nova Lite**: 备用模型 (40次/分钟)

---

🔗 **GitHub**: https://github.com/aws-yz/aws-blog-rss-analyzer  
📖 **完整文档**: README.md
