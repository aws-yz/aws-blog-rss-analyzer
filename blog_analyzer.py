#!/usr/bin/env python3
"""
AWS Blog RSS 分析器
使用 Claude 3.7 Sonnet 和 Nova Lite 双重备用机制生成高质量中文摘要
支持智能内容选择和差异化处理
"""

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
import re
import time

def invoke_bedrock_model(content, title, blog_type=""):
    """调用 Bedrock Claude 3.7 Sonnet 生成中文摘要或翻译"""
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            # 根据博客类型选择不同的处理方式
            if blog_type in ['whats-new', 'news']:
                # What's New 类型使用翻译
                prompt = f"""请将以下AWS What's New更新内容翻译成中文。要求：
1. 准确翻译技术术语和服务名称
2. 保持原文的信息完整性
3. 使用专业的技术语言
4. 保持简洁明了

标题：{title}

内容：
{content[:1500]}

请提供中文翻译："""
            else:
                # 其他类型使用摘要
                prompt = f"""请为以下AWS技术博客生成一个150-200字的中文摘要。要求：
1. 突出主要技术特性和功能
2. 说明实际应用价值和场景
3. 使用专业的技术语言
4. 不要包含英文原文

博客标题：{title}

博客内容：
{content[:2000]}

请生成中文摘要："""

            # 构建 Claude 3.7 Sonnet 的请求体格式
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            # 调用 AWS CLI 调用 Bedrock
            cmd = [
                'aws', 'bedrock-runtime', 'invoke-model',
                '--model-id', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0',
                '--body', json.dumps(request_body),
                '--cli-binary-format', 'raw-in-base64-out',
                '/tmp/bedrock_response.json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                if "ThrottlingException" in result.stderr and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # 指数退避
                    print(f"请求被限流，等待 {delay} 秒后重试...", file=sys.stderr)
                    time.sleep(delay)
                    continue
                else:
                    print(f"Bedrock API 调用失败: {result.stderr}", file=sys.stderr)
                    return None
            
            # 读取响应
            with open('/tmp/bedrock_response.json', 'r', encoding='utf-8') as f:
                response = json.load(f)
            
            # 提取生成的摘要
            if 'content' in response and len(response['content']) > 0:
                summary = response['content'][0].get('text', '').strip()
                return summary
            
            return None
            
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"生成摘要时出错: {e}，等待 {delay} 秒后重试...", file=sys.stderr)
                time.sleep(delay)
                continue
            else:
                print(f"生成摘要时出错: {e}", file=sys.stderr)
                return None
    
    return None

def generate_chinese_summary(title, content, blog_type=""):
    """基于内容使用 Bedrock 生成中文摘要或翻译"""
    if not content or len(content) < 50:
        return "暂无足够内容生成摘要。"
    
    # 清理内容（移除 HTML 标签）
    clean_content = re.sub(r'<[^>]+>', ' ', content)
    clean_content = re.sub(r'[{}"\[\]]', '', clean_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    
    # 调用 Bedrock 生成摘要或翻译
    bedrock_result = invoke_bedrock_model(clean_content, title, blog_type)
    
    if bedrock_result:
        return bedrock_result
    
    # 如果 Claude 3.7 调用失败，使用 Nova Lite 备用
    print("Claude 3.7 调用失败，使用 Nova Lite 备用生成", file=sys.stderr)
    
    nova_lite_result = invoke_nova_lite_fallback(clean_content, title, blog_type)
    if nova_lite_result:
        return nova_lite_result
    
    # 最后的简化备用逻辑
    print("Nova Lite 也失败，使用最简备用逻辑", file=sys.stderr)
    if blog_type in ['whats-new', 'news']:
        return f"AWS 发布了关于 {title} 的更新。"
    else:
        return f"本文介绍了 {title} 相关的 AWS 服务更新和技术特性。"

def generate_markdown_report(blog_type, articles, start_date, end_date):
    """生成 Markdown 报告"""
    blog_names = {
        'aws': 'AWS 主博客',
        'machine-learning': '机器学习',
        'database': '数据库',
        'security': '安全',
        'compute': '计算服务',
        'storage': '存储服务',
        'networking': '网络和内容分发'
    }
    
    # 格式化日期
    start_dt = datetime.fromisoformat(start_date.replace('Z', ''))
    end_dt = datetime.fromisoformat(end_date.replace('Z', ''))
    
    report = f"""# AWS {blog_names.get(blog_type, blog_type)} 博客分析报告

**分析时间范围**: {start_dt.strftime('%Y年%m月%d日')} 至 {end_dt.strftime('%Y年%m月%d日')}
**文章总数**: {len(articles)}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 博客文章列表

"""
    
    for i, article in enumerate(articles, 1):
        # 格式化日期
        pub_date = datetime.fromisoformat(article['pub_date'])
        formatted_date = pub_date.strftime('%Y年%m月%d日')
        
        # 生成中文摘要
        summary = generate_chinese_summary(
            article['title'], 
            article['description'], 
            article.get('content', '')
        )
        
        # 清理摘要中的标题标记，避免与报告结构冲突
        if summary:
            # 移除开头的 # 标题标记
            summary = re.sub(r'^#+\s*', '', summary.strip())
            # 移除中间的 # 标题标记，替换为粗体
            summary = re.sub(r'\n#+\s*([^\n]+)', r'\n**\1**', summary)
        
        report += f"""### {i}. {article['title']}
- **作者**: {article['author']}
- **发布时间**: {formatted_date}
- **链接**: {article['link']}

**中文摘要**:
{summary}

---

"""
    
    return report

def print_help():
    """打印帮助信息"""
    print("""
AWS Blog RSS Analyzer v2.0 - 智能内容处理和差异化AI分析

用法:
    python blog_analyzer.py <blog_type> <start_date> <end_date>
    python blog_analyzer.py -h|--help
    python blog_analyzer.py -v|--version

参数:
    blog_type    博客类型 (whats-new, machine-learning, database, etc.)
    start_date   开始日期 (ISO格式: 2025-08-17T00:00:00Z)
    end_date     结束日期 (ISO格式: 2025-08-23T23:59:59Z)

支持的博客类型:
    whats-new, news          - AWS更新和新闻 (使用翻译)
    machine-learning         - 机器学习博客 (使用摘要)
    database, security       - 数据库、安全博客 (使用摘要)
    compute, storage         - 计算、存储博客 (使用摘要)
    networking, containers   - 网络、容器博客 (使用摘要)
    
技术特性:
    • 智能内容选择 (content:encoded vs description)
    • 差异化处理 (翻译 vs 摘要)
    • 双重AI备用 (Claude 3.7 + Nova Lite)
    • 智能限流处理

示例:
    python blog_analyzer.py whats-new 2025-08-17T00:00:00Z 2025-08-23T23:59:59Z
    python blog_analyzer.py machine-learning 2025-08-20T00:00:00Z 2025-08-24T23:59:59Z
""")

def main():
    if len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        print_help()
        sys.exit(0)
    
    if len(sys.argv) == 2 and sys.argv[1] in ['-v', '--version']:
        print("AWS Blog RSS Analyzer v2.0")
        print("支持智能内容处理和差异化AI分析")
        sys.exit(0)
    
    if len(sys.argv) != 4:
        print("Usage: python blog_analyzer.py <blog_type> <start_date> <end_date>")
        print("Use -h or --help for more information")
        sys.exit(1)
    
    blog_type = sys.argv[1]
    start_date = sys.argv[2] 
    end_date = sys.argv[3]
    
    # 1. 获取 RSS 文章列表
    print("正在使用RSS解析器获取文章列表...", file=sys.stderr)
    
    # 使用相对路径，更灵活
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rss_parser_path = os.path.join(script_dir, 'rss_parser.py')
    
    result = subprocess.run([
        'python3', rss_parser_path,
        blog_type, start_date, end_date
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"RSS 解析失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    try:
        articles = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("JSON 解析失败", file=sys.stderr)
        sys.exit(1)
    
    if not articles:
        print("未找到指定日期范围内的文章", file=sys.stderr)
        sys.exit(1)
    
    print(f"找到 {len(articles)} 篇文章，直接使用 RSS 内容生成摘要...", file=sys.stderr)
    
    # 2. 直接使用 RSS description 生成摘要 - 考虑限流，分批处理
    print(f"正在使用 Claude 3.7 Sonnet 生成摘要 (配额: 250次/分钟)...", file=sys.stderr)
    
    # 如果文章数量较多，分批处理避免限流
    batch_size = 10  # 每批处理10篇文章
    processed = 0
    
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i+batch_size]
        
        for article in batch:
            # 根据博客类型和可用内容选择最佳源
            if blog_type in ['whats-new', 'news']:
                # What's New 和 News 只有 description，直接使用
                content_source = article['description']
            else:
                # 其他博客优先使用 content_encoded，回退到 description
                content_source = article.get('content_encoded', '') or article['description']
            
            summary = generate_chinese_summary(
                article['title'], 
                content_source, 
                blog_type
            )
            article['summary'] = summary
            processed += 1
            
            # 每处理一篇文章后短暂延迟，避免超过限流
            # 注释掉延迟以加快演示速度
            # if processed < len(articles):
            #     time.sleep(0.3)  # 300ms延迟，确保不超过250次/分钟
        
        # 批次间延迟
        if i + batch_size < len(articles):
            print(f"已处理 {min(i + batch_size, len(articles))}/{len(articles)} 篇文章，短暂休息避免限流...", file=sys.stderr)
            time.sleep(2)  # 批次间2秒延迟
    
    # 4. 生成报告
    report = generate_markdown_report(blog_type, articles, start_date, end_date)
    print(report)

def invoke_nova_lite_fallback(content, title, blog_type=""):
    """使用 Nova Lite 作为备用模型生成摘要"""
    try:
        # 根据博客类型选择处理方式
        if blog_type in ['whats-new', 'news']:
            prompt = f"""请将以下AWS更新内容翻译成中文：

标题：{title}
内容：{content[:1000]}

请提供简洁的中文翻译："""
        else:
            prompt = f"""请为以下AWS博客生成中文摘要：

标题：{title}
内容：{content[:1000]}

请生成150字左右的中文摘要："""

        # Nova Lite 请求格式
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 200,
                "temperature": 0.3
            }
        }

        cmd = [
            'aws', 'bedrock-runtime', 'invoke-model',
            '--model-id', 'us.amazon.nova-lite-v1:0',
            '--body', json.dumps(request_body),
            '--cli-binary-format', 'raw-in-base64-out',
            '/tmp/nova_lite_response.json'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        
        if result.returncode == 0:
            with open('/tmp/nova_lite_response.json', 'r', encoding='utf-8') as f:
                response = json.load(f)
            
            if 'output' in response and 'message' in response['output']:
                content_list = response['output']['message'].get('content', [])
                if content_list and len(content_list) > 0:
                    return content_list[0].get('text', '').strip()
        
        return None
        
    except Exception as e:
        print(f"Nova Lite 备用生成失败: {e}", file=sys.stderr)
        return None
if __name__ == "__main__":
    main()
