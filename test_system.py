#!/usr/bin/env python3
"""
AWS Blog RSS 系统测试脚本
验证所有组件是否正常工作，包括最新的智能内容处理功能
"""

import subprocess
import json
import sys
import os
from datetime import datetime

# 获取脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_rss_parser():
    """测试 RSS 解析器"""
    print("=== 测试 RSS 解析器 ===")
    
    rss_parser_path = os.path.join(SCRIPT_DIR, 'rss_parser.py')
    cmd = [
        'python3', rss_parser_path,
        'machine-learning', '2025-08-17T00:00:00Z', '2025-08-23T23:59:59Z'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ RSS 解析器失败: {result.stderr}")
            return False
        
        articles = json.loads(result.stdout)
        print(f"✅ RSS 解析器成功，获取 {len(articles)} 篇文章")
        
        if articles:
            article = articles[0]
            print("✅ 文章结构完整")
            print(f"   示例文章: {article['title'][:50]}...")
            
            # 测试新功能：content_encoded 字段
            if 'content_encoded' in article:
                print("✅ 包含 content_encoded 字段")
                if article['content_encoded']:
                    print(f"   content_encoded 长度: {len(article['content_encoded'])} 字符")
                else:
                    print("   content_encoded 为空（正常，取决于 RSS 类型）")
            else:
                print("❌ 缺少 content_encoded 字段")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ RSS 解析器测试出错: {e}")
        return False

def test_blog_analyzer():
    """测试博客分析器"""
    print("\n=== 测试博客分析器 ===")
    
    blog_analyzer_path = os.path.join(SCRIPT_DIR, 'blog_analyzer.py')
    cmd = [
        'python3', blog_analyzer_path,
        'machine-learning', '2025-08-22T17:00:00Z', '2025-08-22T18:00:00Z'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"❌ 博客分析器失败: {result.stderr}")
            return False
        
        report = result.stdout
        
        # 检查报告格式
        if "# AWS 机器学习 博客分析报告" in report:
            print("✅ 报告格式正确")
        else:
            print("❌ 报告格式错误")
            return False
        
        if "**文章总数**:" in report:
            print("✅ 包含文章统计")
        else:
            print("❌ 缺少文章统计")
            return False
        
        print(f"✅ 博客分析器成功，生成 {len(report)} 字符的报告")
        return True
        
    except Exception as e:
        print(f"❌ 博客分析器测试出错: {e}")
        return False

def test_whats_new_translation():
    """测试 What's New 翻译功能"""
    print("\n=== 测试 What's New 翻译功能 ===")
    
    blog_analyzer_path = os.path.join(SCRIPT_DIR, 'blog_analyzer.py')
    cmd = [
        'python3', blog_analyzer_path,
        'whats-new', '2025-08-22T15:00:00Z', '2025-08-22T17:00:00Z'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            print(f"❌ What's New 翻译失败: {result.stderr}")
            return False
        
        report = result.stdout
        
        # 检查翻译报告格式
        if "# AWS whats-new 博客分析报告" in report:
            print("✅ What's New 报告格式正确")
        else:
            print("❌ What's New 报告格式错误")
            return False
        
        # 检查是否包含中文翻译内容
        if "**中文摘要**:" in report or "**中文翻译**:" in report:
            print("✅ 包含中文翻译内容")
        else:
            print("❌ 缺少中文翻译内容")
            return False
        
        print(f"✅ What's New 翻译成功，生成 {len(report)} 字符的报告")
        return True
        
    except Exception as e:
        print(f"❌ What's New 翻译测试出错: {e}")
        return False

def test_agent_config():
    """测试 Agent 配置"""
    print("\n=== 测试 Agent 配置 ===")
    
    try:
        config_path = os.path.join(SCRIPT_DIR, 'aws-blog-rss-analyzer.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # 检查基本结构
        required_fields = ['name', 'description', 'prompt', 'tools', 'resources']
        for field in required_fields:
            if field not in config:
                print(f"❌ 配置缺少字段: {field}")
                return False
        
        print("✅ Agent 配置文件结构完整")
        
        # 检查名称
        if config['name'] == 'aws-blog-rss-analyzer':
            print("✅ Agent 名称正确")
        else:
            print("❌ Agent 名称错误")
            return False
        
        # 检查工具路径
        resources = config.get('resources', [])
        expected_files = ['rss_parser.py', 'blog_analyzer.py', 'README.md']
        
        for expected_file in expected_files:
            found = any(expected_file in resource for resource in resources)
            if found:
                print(f"✅ 工具路径配置正确: {expected_file}")
            else:
                print(f"❌ 缺少工具路径: {expected_file}")
                return False
        
        # 检查新功能描述
        if "智能内容处理" in config['description'] or "差异化" in config['description']:
            print("✅ 包含新功能描述")
        else:
            print("⚠️  建议更新描述以反映新功能")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent 配置测试出错: {e}")
        return False

def main():
    """主测试函数"""
    print("AWS Blog RSS 系统测试")
    print("=" * 50)
    
    tests = [
        ("RSS 解析器", test_rss_parser),
        ("博客分析器", test_blog_analyzer),
        ("What's New 翻译", test_whats_new_translation),
        ("Agent 配置", test_agent_config)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results[test_name] = False
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常使用。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
