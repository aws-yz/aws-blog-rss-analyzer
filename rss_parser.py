#!/usr/bin/env python3
"""
AWS Blog RSS Parser
基于 n8n RSS node 优化实现，支持智能内容选择
"""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import json
import sys
from typing import List, Dict, Optional

class AWSBlogRSSParser:
    def __init__(self):
        # 基于 n8n RSS node 的优化 HTTP headers（已验证有效）
        self.headers = {
            'User-Agent': 'rss-parser',
            'Accept': 'application/rss+xml, application/rdf+xml;q=0.8, application/atom+xml;q=0.6, application/xml;q=0.4, text/xml;q=0.4'
        }
        
        # AWS Blog RSS feeds (扩展支持更多类型)
        self.feeds = {
            'aws': 'https://aws.amazon.com/blogs/aws/feed/',
            'machine-learning': 'https://aws.amazon.com/blogs/machine-learning/feed/',
            'database': 'https://aws.amazon.com/blogs/database/feed/',
            'security': 'https://aws.amazon.com/blogs/security/feed/',
            'compute': 'https://aws.amazon.com/blogs/compute/feed/',
            'storage': 'https://aws.amazon.com/blogs/storage/feed/',
            'networking': 'https://aws.amazon.com/blogs/networking-and-content-delivery/feed/',
            'devops': 'https://aws.amazon.com/blogs/devops/feed/',
            'containers': 'https://aws.amazon.com/blogs/containers/feed/',
            'serverless': 'https://aws.amazon.com/blogs/compute/feed/',
            'big-data': 'https://aws.amazon.com/blogs/big-data/feed/',
            'analytics': 'https://aws.amazon.com/blogs/big-data/feed/',
            'mobile': 'https://aws.amazon.com/blogs/mobile/feed/',
            'iot': 'https://aws.amazon.com/blogs/iot/feed/',
            'gametech': 'https://aws.amazon.com/blogs/gametech/feed/',
            'media': 'https://aws.amazon.com/blogs/media/feed/',
            'architecture': 'https://aws.amazon.com/blogs/architecture/feed/',
            'startup': 'https://aws.amazon.com/blogs/startups/feed/',
            'publicsector': 'https://aws.amazon.com/blogs/publicsector/feed/',
            'enterprise': 'https://aws.amazon.com/blogs/enterprise-strategy/feed/',
            'whats-new': 'https://aws.amazon.com/about-aws/whats-new/recent/feed/',
            'news': 'https://aws.amazon.com/about-aws/whats-new/recent/feed/'
        }
    
    def fetch_rss(self, feed_url: str) -> Optional[str]:
        """使用验证过的优化 headers 获取 RSS 内容"""
        try:
            req = urllib.request.Request(feed_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching RSS: {e}", file=sys.stderr)
            return None
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """解析 RSS pubDate 格式（支持多种格式）"""
        try:
            # 尝试多种日期格式
            formats = [
                "%a, %d %b %Y %H:%M:%S %z",      # "Fri, 22 Aug 2025 17:54:38 +0000"
                "%a, %d %b %Y %H:%M:%S GMT",     # "Fri, 22 Aug 2025 16:00:00 GMT"
                "%a, %d %b %Y %H:%M:%S %Z"       # 其他时区格式
            ]
            
            for fmt in formats:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    # 如果是 GMT，转换为 UTC
                    if 'GMT' in date_str:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    return parsed.replace(tzinfo=None)  # 转换为 naive datetime
                except ValueError:
                    continue
            
            return None
        except Exception:
            return None
    
    def parse_rss_items(self, rss_content: str, start_date: str, end_date: str) -> List[Dict]:
        """解析 RSS 并按日期过滤（基于验证的逻辑）"""
        try:
            root = ET.fromstring(rss_content)
            items = []
            
            # 解析日期范围
            start_dt = datetime.fromisoformat(start_date.replace('Z', ''))
            end_dt = datetime.fromisoformat(end_date.replace('Z', ''))
            
            # 提取所有 item 元素
            for item in root.findall('.//item'):
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                description_elem = item.find('description')
                creator_elem = item.find('.//{http://purl.org/dc/elements/1.1/}creator')
                # 提取 content:encoded 内容
                content_encoded_elem = item.find('.//{http://purl.org/rss/1.0/modules/content/}encoded')
                
                if title_elem is None or link_elem is None or pub_date_elem is None:
                    continue
                
                # 解析发布日期
                pub_date = self.parse_date(pub_date_elem.text)
                if not pub_date:
                    continue
                
                # 日期过滤
                if start_dt <= pub_date <= end_dt:
                    # 修复可能的 URL 格式问题
                    link = link_elem.text.strip()
                    if "amazon.comabout-aws" in link:
                        link = link.replace("amazon.comabout-aws", "amazon.com/about-aws")
                    
                    # 提取内容，优先使用 content:encoded
                    content_encoded = ""
                    if content_encoded_elem is not None and content_encoded_elem.text:
                        content_encoded = content_encoded_elem.text.strip()
                    
                    items.append({
                        'title': title_elem.text.strip(),
                        'link': link,
                        'pub_date': pub_date.isoformat(),
                        'pub_date_raw': pub_date_elem.text,
                        'description': description_elem.text.strip() if description_elem is not None else '',
                        'content_encoded': content_encoded,
                        'author': creator_elem.text.strip() if creator_elem is not None else 'AWS Team'
                    })
            
            return sorted(items, key=lambda x: x['pub_date'], reverse=True)
            
        except Exception as e:
            print(f"Error parsing RSS: {e}", file=sys.stderr)
            return []
    
    def get_blog_articles(self, blog_type: str, start_date: str, end_date: str) -> List[Dict]:
        """获取指定类型和日期范围的博客文章"""
        if blog_type not in self.feeds:
            print(f"Unknown blog type: {blog_type}. Available: {list(self.feeds.keys())}", file=sys.stderr)
            return []
        
        feed_url = self.feeds[blog_type]
        rss_content = self.fetch_rss(feed_url)
        
        if not rss_content:
            return []
        
        return self.parse_rss_items(rss_content, start_date, end_date)

def main():
    if len(sys.argv) != 4:
        print("Usage: python rss_parser.py <blog_type> <start_date> <end_date>")
        print("Blog types: aws, machine-learning, database, security, compute, storage, networking")
        print("Date format: 2024-08-17T00:00:00Z")
        sys.exit(1)
    
    blog_type = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    parser = AWSBlogRSSParser()
    articles = parser.get_blog_articles(blog_type, start_date, end_date)
    
    print(json.dumps(articles, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
