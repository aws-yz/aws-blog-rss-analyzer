#!/bin/bash
# 简化 Demo 脚本

clear
echo "🚀 AWS Blog RSS Analyzer Demo"
echo "============================="
sleep 1

echo ""
echo "📋 项目概览:"
echo "• 智能 RSS 解析器"
echo "• 双重 AI 备用机制" 
echo "• 支持 20+ AWS RSS feeds"
sleep 2

echo ""
echo "📁 核心文件:"
ls -1 *.py | head -4
sleep 2

echo ""
echo "🔧 安装 Agent:"
echo "$ ./install_agent.sh"
sleep 1
./install_agent.sh | head -10
sleep 2

echo ""
echo "🧪 验证配置:"
echo "$ python3 validate_config.py"
sleep 1
python3 validate_config.py | grep "✅"
sleep 2

echo ""
echo "📊 RSS 解析演示:"
echo "$ python3 rss_parser.py whats-new 2025-08-24T00:00:00Z 2025-08-24T23:59:59Z"
sleep 1
python3 rss_parser.py whats-new 2025-08-24T00:00:00Z 2025-08-24T23:59:59Z | head -15
sleep 2

echo ""
echo "🤖 查看帮助:"
echo "$ python3 blog_analyzer.py --help"
sleep 1
python3 blog_analyzer.py --help | head -10
sleep 2

echo ""
echo "✅ Demo 完成!"
echo "🔗 GitHub: https://github.com/aws-yz/aws-blog-rss-analyzer"
sleep 1
