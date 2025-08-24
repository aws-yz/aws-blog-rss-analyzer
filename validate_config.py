#!/usr/bin/env python3
"""
AWS Blog RSS Analyzer 配置验证脚本
验证 agent 配置文件的正确性
"""

import json
import os
import sys

def validate_config():
    """验证配置文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'aws-blog-rss-analyzer.json')
    template_path = os.path.join(script_dir, 'aws-blog-rss-analyzer.json.template')
    
    # 检查模板文件
    if not os.path.exists(template_path):
        print(f"❌ 配置模板文件不存在: {template_path}")
        return False
    else:
        print(f"✅ 配置模板文件存在: {template_path}")
    
    # 检查生成的配置文件
    if not os.path.exists(config_path):
        print(f"⚠️  生成的配置文件不存在: {config_path}")
        print("💡 请运行 ./install_agent.sh 生成配置文件")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False
    
    # 验证必需字段
    required_fields = ['name', 'description', 'prompt', 'tools', 'resources']
    for field in required_fields:
        if field not in config:
            print(f"❌ 缺少必需字段: {field}")
            return False
    
    # 验证名称
    if config['name'] != 'aws-blog-rss-analyzer':
        print(f"❌ Agent 名称错误: {config['name']}")
        return False
    
    # 验证资源文件路径
    resources = config.get('resources', [])
    expected_files = ['rss_parser.py', 'blog_analyzer.py', 'README.md']
    
    for expected_file in expected_files:
        found = any(expected_file in resource for resource in resources)
        if not found:
            print(f"❌ 缺少资源文件: {expected_file}")
            return False
        
        # 检查文件是否实际存在
        file_path = os.path.join(script_dir, expected_file)
        if not os.path.exists(file_path):
            print(f"❌ 资源文件不存在: {file_path}")
            return False
    
    # 检查是否还有硬编码路径
    for resource in resources:
        if '/Users/' in resource and '{{SCRIPT_DIR}}' not in resource:
            print(f"⚠️  发现硬编码路径: {resource}")
            print("💡 这可能导致其他用户无法使用")
    
    # 检查 prompt 中的硬编码路径
    prompt = config.get('prompt', '')
    if '/Users/' in prompt and '{{SCRIPT_DIR}}' not in prompt:
        print("⚠️  Prompt 中发现硬编码路径")
        print("💡 这可能导致其他用户无法使用")
    
    # 验证工具配置
    required_tools = ['fs_read', 'execute_bash']
    allowed_tools = config.get('allowedTools', [])
    
    for tool in required_tools:
        if tool not in allowed_tools:
            print(f"⚠️  建议添加工具: {tool}")
    
    print("✅ 配置文件验证通过")
    print(f"   Agent 名称: {config['name']}")
    print(f"   描述: {config['description'][:50]}...")
    print(f"   工具数量: {len(config.get('tools', []))}")
    print(f"   资源数量: {len(resources)}")
    
    return True

if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)
