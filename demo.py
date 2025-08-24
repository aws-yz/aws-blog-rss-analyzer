#!/usr/bin/env python3
"""
AWS Blog RSS Analyzer 功能演示脚本
展示系统的主要功能和差异化处理能力
"""

import subprocess
import json
import sys
import os
from datetime import datetime, timedelta

def run_demo():
    """运行功能演示"""
    print("🚀 AWS Blog RSS Analyzer 功能演示")
    print("=" * 50)
    
    # 获取脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 计算日期范围（最近3天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    
    start_str = start_date.strftime("%Y-%m-%dT00:00:00Z")
    end_str = end_date.strftime("%Y-%m-%dT23:59:59Z")
    
    print(f"📅 分析时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
    print()
    
    # 演示1: What's New 翻译
    print("📰 演示1: What's New 翻译功能")
    print("-" * 30)
    
    cmd = [
        'python3', os.path.join(script_dir, 'blog_analyzer.py'),
        'whats-new', start_str, end_str
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            # 显示前20行
            for line in lines[:20]:
                print(line)
            if len(lines) > 20:
                print(f"... (还有 {len(lines) - 20} 行)")
        else:
            print(f"❌ 执行失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 执行出错: {e}")
    
    print("\n" + "=" * 50)
    
    # 演示2: 技术博客摘要
    print("🔬 演示2: 机器学习博客摘要功能")
    print("-" * 30)
    
    cmd = [
        'python3', os.path.join(script_dir, 'blog_analyzer.py'),
        'machine-learning', start_str, end_str
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            # 显示前20行
            for line in lines[:20]:
                print(line)
            if len(lines) > 20:
                print(f"... (还有 {len(lines) - 20} 行)")
        else:
            print(f"❌ 执行失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 执行出错: {e}")
    
    print("\n" + "=" * 50)
    
    # 演示3: RSS 解析器功能
    print("⚙️  演示3: RSS 解析器 - 内容源对比")
    print("-" * 30)
    
    cmd = [
        'python3', os.path.join(script_dir, 'rss_parser.py'),
        'machine-learning', start_str, end_str
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            articles = json.loads(result.stdout)
            if articles:
                article = articles[0]
                print(f"📄 文章标题: {article['title'][:60]}...")
                print(f"📝 Description 长度: {len(article['description'])} 字符")
                print(f"📖 Content_encoded 长度: {len(article.get('content_encoded', ''))} 字符")
                print(f"🔗 链接: {article['link']}")
                
                if article.get('content_encoded'):
                    print("✅ 该博客包含完整的 content:encoded 内容")
                else:
                    print("ℹ️  该博客仅包含 description 内容")
            else:
                print("ℹ️  当前时间范围内没有找到文章")
        else:
            print(f"❌ 执行失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 执行出错: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print("\n💡 主要特性:")
    print("   • What's New: 使用翻译保持信息完整性")
    print("   • 技术博客: 使用摘要提取关键要点")
    print("   • 智能内容选择: content:encoded vs description")
    print("   • 双重 AI 备用: Claude 3.7 + Nova Lite")
    print("   • 性能优化: 直接使用 RSS 内容，提升 3-5倍 速度")

if __name__ == "__main__":
    run_demo()
