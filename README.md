# AWS Blog RSS Analyzer - Amazon Q CLI Custom Agent

AWS 全方位 RSS 分析专家，支持多种 AWS 官方 RSS feeds 的智能分析助手。

## 🚀 功能特点

### 核心能力
- **多源 RSS 解析**: 支持 20+ 种 AWS RSS feeds，包括博客、What's New 等
- **智能内容处理**: 根据内容类型自动选择最佳处理方式
- **AI 驱动分析**: 使用 Claude 3.7 Sonnet + Nova Lite 双重备用机制
- **差异化处理**: What's New 使用翻译，技术博客使用摘要
- **结构化报告**: 输出标准化的 Markdown 格式报告

### 技术优势
- **智能内容选择**: 自动使用 `content:encoded` 或 `description`
- **双重 AI 备用**: Claude 3.7 Sonnet (250次/分钟) + Nova Lite (40次/分钟)
- **批量处理优化**: 智能分批处理，避免限流
- **精确日期过滤**: 支持多种 RSS 日期格式（GMT、UTC等）
- **完善错误恢复**: 三层备用机制确保稳定性

## 📋 支持的 AWS RSS Feeds

### 主要博客类型
- `aws`: AWS 主博客
- `machine-learning`: 机器学习博客
- `database`: 数据库博客
- `security`: 安全博客
- `compute`: 计算服务博客
- `storage`: 存储服务博客
- `networking`: 网络和内容分发博客

### 专业领域博客
- `devops`: DevOps 博客
- `containers`: 容器技术博客
- `serverless`: 无服务器计算博客
- `big-data`: 大数据博客
- `analytics`: 数据分析博客
- `mobile`: 移动开发博客
- `iot`: 物联网博客
- `gametech`: 游戏技术博客
- `media`: 媒体服务博客
- `architecture`: 架构博客

### 行业和企业博客
- `startup`: 初创企业博客
- `publicsector`: 公共部门博客
- `enterprise`: 企业战略博客

### 新闻和更新
- `whats-new`: AWS What's New 更新
- `news`: AWS 新闻动态

## 📁 项目结构

```
rss-parser/
├── rss_parser.py                           # 核心 RSS 解析器
├── blog_analyzer.py                        # 智能博客分析器
├── aws-blog-rss-analyzer.json.template     # Agent 配置模板
├── install_agent.sh                        # 安装脚本
├── validate_config.py                      # 配置验证脚本
├── test_system.py                          # 系统测试脚本
├── demo.py                                 # 功能演示脚本
├── README.md                               # 使用说明
└── .gitignore                              # Git 忽略文件
```

## 🔧 安装方法

### 前置要求

- Python 3.7+
- Amazon Q CLI 已正确配置
- AWS 凭证已配置（用于 Bedrock 访问）

### 快速安装

```bash
# 1. Clone 项目
git clone <repository-url>
cd rss-parser

# 2. 运行安装脚本
./install_agent.sh

# 3. 开始使用
q chat --agent aws-blog-rss-analyzer
```

### 完整安装（包含验证）

```bash
# 1. Clone 项目
git clone <repository-url>
cd rss-parser

# 2. 运行安装脚本
./install_agent.sh

# 3. 验证安装
python3 validate_config.py
python3 test_system.py

# 4. 开始使用
q chat --agent aws-blog-rss-analyzer
```

## 💡 使用方法

### 方式1: Amazon Q CLI Agent（推荐）

```bash
q chat --agent aws-blog-rss-analyzer
```

**示例对话**:
- "生成上周的AWS What's New更新摘要"
- "分析最近的机器学习博客文章"
- "对比容器技术和无服务器计算的最新趋势"

### 方式2: 直接使用脚本

```bash
# RSS 解析器（获取原始数据）
python3 rss_parser.py <blog_type> <start_date> <end_date>

# 博客分析器（生成AI摘要）
python3 blog_analyzer.py <blog_type> <start_date> <end_date>

# 查看帮助
python3 blog_analyzer.py --help
```

**示例**:
```bash
# What's New 翻译
python3 blog_analyzer.py whats-new 2025-08-17T00:00:00Z 2025-08-23T23:59:59Z

# 机器学习博客摘要
python3 blog_analyzer.py machine-learning 2025-08-17T00:00:00Z 2025-08-23T23:59:59Z
```

## 🧠 智能处理机制

### 内容源选择
- **What's New/News**: 使用 `description`（约1300字符，适合翻译）
- **技术博客**: 优先使用 `content:encoded`（完整文章），回退到 `description`

### 处理方式差异
- **What's New**: 中文翻译（保持信息完整性）
- **技术博客**: 中文摘要（提取关键要点）

### AI 模型备用机制
1. **Claude 3.7 Sonnet**: 主要模型（250次/分钟）
2. **Nova Lite**: 备用模型（40次/分钟）
3. **简化模板**: 最终备用

## ⚡ 性能优化

### 限流处理
- **批量处理**: 每批处理 10 篇文章
- **智能延迟**: 每篇文章间 300ms 延迟
- **批次间隔**: 批次间 2 秒休息
- **配额管理**: 自动切换到备用模型

### 技术优化
- **智能内容源**: 根据 RSS 类型自动选择最佳内容
- **无额外抓取**: 直接使用 RSS 内容，提升 3-5倍 速度
- **错误恢复**: 完善的三层备用机制
- **URL 自动修复**: 智能修复 RSS 中的格式错误

## 📊 输出格式

### What's New 翻译报告
```markdown
# AWS whats-new 博客分析报告

**分析时间范围**: 2025年08月17日 至 2025年08月23日
**文章总数**: 15
**生成时间**: 2025-08-24 16:00:00
**处理方式**: 中文翻译

## 博客文章列表

### 1. [更新标题]
- **作者**: AWS Team
- **发布时间**: 2025年08月22日
- **链接**: [更新链接]

**中文翻译**:
[准确的中文翻译，保持原文信息完整性]
```

### 技术博客摘要报告
```markdown
# AWS 机器学习 博客分析报告

**分析时间范围**: 2025年08月17日 至 2025年08月23日
**文章总数**: 8
**生成时间**: 2025-08-24 16:00:00
**处理方式**: 中文摘要

## 博客文章列表

### 1. [文章标题]
- **作者**: [作者名]
- **发布时间**: 2025年08月22日
- **链接**: [博客链接]

**中文摘要**:
[专业的中文摘要，包含技术特性、应用场景和关键要点]
```

## 🧪 测试和验证

```bash
# 验证配置文件
python3 validate_config.py

# 运行系统测试
python3 test_system.py

# 查看功能演示
python3 demo.py
```

## 🔍 故障排除

### 常见问题

**1. 安装失败**
```bash
# 检查 Python 版本
python3 --version

# 检查必需文件
ls -la *.py *.sh *.template
```

**2. Agent 无法找到**
```bash
# 检查配置文件
ls -la ~/.aws/amazonq/cli-agents/aws-blog-rss-analyzer.json

# 重新安装
./install_agent.sh
```

**3. API 调用失败**
```bash
# 检查 AWS 凭证
aws sts get-caller-identity

# 检查 Bedrock 权限
aws bedrock list-foundation-models --region us-east-1
```

## 🎯 技术创新

1. **RSS 内容智能解析**: 自动识别并使用 `content:encoded` 完整内容
2. **差异化 AI 处理**: What's New 翻译 vs 技术博客摘要
3. **多层备用机制**: Claude 3.7 → Nova Lite → 简化模板
4. **日期格式兼容**: 支持 GMT、UTC 等多种时区格式
5. **动态路径解析**: 支持任意目录结构，无硬编码路径

## 📈 验证结果

- ✅ 支持 20+ 种 AWS RSS feeds
- ✅ 智能内容选择（content:encoded vs description）
- ✅ 差异化处理（翻译 vs 摘要）
- ✅ 双重 AI 备用机制
- ✅ 智能限流处理
- ✅ 完整的错误处理和恢复机制
- ✅ 结构化的专业报告输出
- ✅ 跨平台兼容性

## 🎪 应用场景

这个 agent 提供了全面的 AWS 内容分析能力，适用于：

- **技术研究**: 跟踪 AWS 最新技术发展
- **趋势分析**: 分析不同服务领域的发展趋势
- **内容监控**: 定期获取 AWS 官方更新
- **学习资源**: 获取高质量的技术内容摘要
- **决策支持**: 为技术选型提供参考信息

---

**版本**: v2.0  
**最后更新**: 2025-08-24  
**维护状态**: 活跃开发中
