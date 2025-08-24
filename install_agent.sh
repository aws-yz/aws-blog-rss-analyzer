#!/bin/bash
# AWS Blog RSS Analyzer Agent 安装脚本

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_TEMPLATE="$SCRIPT_DIR/aws-blog-rss-analyzer.json.template"
CONFIG_FILE="$SCRIPT_DIR/aws-blog-rss-analyzer.json"

echo "正在安装 AWS Blog RSS Analyzer Agent..."

# 检查模板文件是否存在
if [ ! -f "$CONFIG_TEMPLATE" ]; then
    echo "❌ 错误: 找不到配置模板文件 $CONFIG_TEMPLATE"
    exit 1
fi

# 检查必需的脚本文件是否存在
required_files=("rss_parser.py" "blog_analyzer.py" "README.md")
for file in "${required_files[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        echo "❌ 错误: 找不到必需文件 $file"
        exit 1
    fi
done

# 生成配置文件，替换路径占位符
echo "📝 生成配置文件..."
sed "s|{{SCRIPT_DIR}}|$SCRIPT_DIR|g" "$CONFIG_TEMPLATE" > "$CONFIG_FILE"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 错误: 配置文件生成失败"
    exit 1
fi

# 确保目标目录存在
mkdir -p ~/.aws/amazonq/cli-agents/

# 复制配置文件
cp "$CONFIG_FILE" ~/.aws/amazonq/cli-agents/

echo "✅ Agent 安装完成！"
echo ""
echo "📍 安装路径: $SCRIPT_DIR"
echo "📄 配置文件: ~/.aws/amazonq/cli-agents/aws-blog-rss-analyzer.json"
echo ""
echo "使用方法:"
echo "  q chat --agent aws-blog-rss-analyzer"
echo ""
echo "示例对话:"
echo '  "生成上周的AWS What'\''s New更新摘要"'
echo '  "分析最近的机器学习博客文章"'
echo ""
echo "主要功能:"
echo "  • 智能内容处理 (content:encoded vs description)"
echo "  • 差异化AI分析 (翻译 vs 摘要)"
echo "  • 双重AI备用 (Claude 3.7 + Nova Lite)"
echo "  • 支持20+种AWS RSS feeds"
