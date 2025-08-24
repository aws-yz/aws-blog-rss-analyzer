#!/bin/bash
# 推送到 GitHub 仓库的脚本

echo "🚀 推送 AWS Blog RSS Analyzer 到 GitHub..."

# 检查是否提供了 GitHub 用户名
if [ -z "$1" ]; then
    echo "❌ 请提供 GitHub 用户名"
    echo "用法: ./push_to_github.sh <github-username>"
    echo "示例: ./push_to_github.sh your-username"
    exit 1
fi

GITHUB_USER="$1"
REPO_URL="https://github.com/${GITHUB_USER}/aws-blog-rss-analyzer.git"

# 检查远程仓库是否已添加
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ 远程仓库已配置"
else
    echo "📝 添加远程仓库: $REPO_URL"
    git remote add origin "$REPO_URL"
fi

# 推送到 GitHub
echo "📤 推送代码到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功！"
    echo "🔗 仓库地址: https://github.com/${GITHUB_USER}/aws-blog-rss-analyzer"
    echo ""
    echo "📋 仓库包含:"
    echo "   • 智能 RSS 解析器"
    echo "   • 双重 AI 备用机制"
    echo "   • 动态路径解析"
    echo "   • 完整测试套件"
    echo "   • 详细文档"
else
    echo "❌ 推送失败，请检查："
    echo "   1. GitHub 仓库是否已创建"
    echo "   2. 网络连接是否正常"
    echo "   3. Git 凭证是否正确"
fi
