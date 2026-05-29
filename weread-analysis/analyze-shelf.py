#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import requests
from datetime import datetime

class WereadAnalyzer:
    def __init__(self, api_key, output_dir=None):
        self.api_key = api_key
        self.base_url = "https://i.weread.qq.com/api/agent/gateway"
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_shelf(self):
        """获取书架数据"""
        print("📚 获取书架数据...")
        body = {"api_name": "/shelf/sync", "skill_version": "1.0.3"}
        try:
            response = requests.post(self.base_url, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            shelf_file = os.path.join(self.output_dir, "shelf.json")
            with open(shelf_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 书架数据已保存到 {shelf_file}")
            return data
        except Exception as e:
            print(f"❌ 获取书架失败: {e}")
            return None
    
    def get_book_info(self, book_id):
        """获取单本书的详细信息"""
        body = {"api_name": "/book/info", "bookId": book_id, "skill_version": "1.0.3"}
        try:
            response = requests.post(self.base_url, headers=self.headers, json=body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ 获取书籍 {book_id} 信息失败: {e}")
            return None
    
    def get_all_books_details(self, shelf):
        """批量获取所有书籍详情"""
        books = shelf.get("books", [])
        total = len(books)
        print(f"\n🔄 开始获取 {total} 本书的详细信息...")
        
        all_details = []
        batch_size = 50
        batches = (total // batch_size) + 1
        
        for batch in range(batches):
            start = batch * batch_size
            end = min((batch + 1) * batch_size, total)
            print(f"  处理批次 {batch + 1}/{batches} (第 {start + 1}-{end} 本书)")
            
            for book in books[start:end]:
                details = self.get_book_info(book["bookId"])
                if details:
                    details["readUpdateTime"] = book.get("readUpdateTime", 0)
                    details["finishReading"] = book.get("finishReading", 0)
                    details["isTop"] = book.get("isTop", 0)
                    all_details.append(details)
                time.sleep(0.03)
            
            # 每批保存进度
            progress_file = os.path.join(self.output_dir, "books-details-progress.json")
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(all_details, f, ensure_ascii=False)
        
        # 最终保存
        details_file = os.path.join(self.output_dir, "all-books-details.json")
        with open(details_file, "w", encoding="utf-8") as f:
            json.dump(all_details, f, ensure_ascii=False, indent=2)
        print(f"✅ 全部书籍详情已保存到 {details_file}")
        return all_details
    
    def analyze_books(self, books):
        """分析书籍价值"""
        print("\n📊 开始分析书籍价值...")
        
        stats = {
            "total": len(books),
            "never_read": 0,
            "read_before": 0,
            "finished": 0,
            "high_score": 0,
            "low_score": 0,
            "recent_books": 0,
            "ai_books": 0,
        }
        
        category_stats = {}
        delete_candidates = []
        keep_candidates = []
        consider_candidates = []
        
        for book in books:
            rating = book.get("newRating", 0)
            rating_count = book.get("newRatingCount", 0)
            publish_time = book.get("publishTime", "")
            title = book.get("title", "")
            read_update = book.get("readUpdateTime", 0)
            finished = book.get("finishReading", 0)
            
            # 统计阅读状态
            if read_update == 0:
                stats["never_read"] += 1
            else:
                stats["read_before"] += 1
            if finished == 1:
                stats["finished"] += 1
            
            # 统计评分
            if rating >= 80:
                stats["high_score"] += 1
            if rating < 50:
                stats["low_score"] += 1
            
            # 统计出版时间
            if publish_time.startswith(("2024", "2025", "2026")):
                stats["recent_books"] += 1
            
            # 统计AI书籍
            if any(keyword in title for keyword in ["ChatGPT", "GPT", "AI", "AIGC", "Midjourney", "Sora", "DeepSeek"]):
                stats["ai_books"] += 1
            
            # 统计分类
            cat = book.get("categoryName", "未分类")
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            # 价值评分
            score = 0
            if rating >= 80:
                score += 3
            elif rating >= 60:
                score += 1
            else:
                score -= 2
            
            if rating_count >= 100:
                score += 2
            elif rating_count >= 10:
                score += 1
            
            if publish_time.startswith(("2024", "2025", "2026")):
                score += 2
            elif publish_time.startswith(("2020", "2021", "2022", "2023")):
                score += 1
            
            if any(keyword in title for keyword in ["入门", "实战", "图解", "轻松上手", "一本通"]):
                score -= 1
            
            if score >= 4:
                keep_candidates.append(book)
            elif score <= 0:
                delete_candidates.append(book)
            else:
                consider_candidates.append(book)
        
        stats["delete_candidates"] = len(delete_candidates)
        stats["keep_candidates"] = len(keep_candidates)
        stats["consider_candidates"] = len(consider_candidates)
        
        # 保存分析结果
        result = {
            "stats": stats,
            "category_stats": sorted(category_stats.items(), key=lambda x: x[1], reverse=True),
            "delete_candidates": delete_candidates,
            "keep_candidates": keep_candidates,
            "consider_candidates": consider_candidates,
        }
        
        result_file = os.path.join(self.output_dir, "analysis-result.json")
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 分析结果已保存到 {result_file}")
        
        return result
    
    def generate_html_report(self, analysis_result):
        """生成HTML报告"""
        print("\n🎨 生成HTML报告...")
        
        stats = analysis_result["stats"]
        category_stats = analysis_result["category_stats"]
        delete_candidates = analysis_result["delete_candidates"]
        keep_candidates = analysis_result["keep_candidates"]
        consider_candidates = analysis_result["consider_candidates"]
        
        def escape_html(text):
            return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        
        def group_books_by_category(books):
            groups = {}
            for book in books:
                cat = book.get("categoryName", "未分类")
                if cat not in groups:
                    groups[cat] = []
                groups[cat].append(book)
            return dict(sorted(groups.items(), key=lambda x: len(x[1]), reverse=True))
        
        def generate_book_section(books, title, status):
            grouped = group_books_by_category(books)
            section_html = f"""
        <div class="section" id="{status}">
            <h2>{title} (共 {len(books)} 本)</h2>
            <p style="color:#666; margin-bottom:15px;">点击书名可跳转到微信读书</p>
"""
            for cat, cat_books in grouped.items():
                section_html += f"""
            <div class="category-group">
                <h3>📁 {escape_html(cat)} ({len(cat_books)}本)</h3>
                <div class="book-list">
"""
                for book in cat_books:
                    book_id = book.get("bookId", "")
                    book_url = f"https://weread.qq.com/web/bookDetail/{book_id}"
                    section_html += f"""
<div class="book-card {status}">
    <div class="book-title"><a href="{book_url}" target="_blank" rel="noopener noreferrer">{escape_html(book.get("title", ""))}</a></div>
    <div class="book-info">作者: {escape_html(book.get("author", ""))}</div>
    <div class="book-meta">
        <span>评分: {book.get("newRating", 0)}</span>
        <span>评论: {book.get("newRatingCount", 0)}</span>
        <span>出版: {escape_html(book.get("publishTime", ""))}</span>
        <span><a href="{book_url}" target="_blank" class="read-btn">📖 去阅读</a></span>
    </div>
</div>
"""
                section_html += """
                </div>
            </div>
"""
            section_html += """
        </div>
"""
            return section_html
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信读书书架分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .nav-bar {{ background: #f8f9fa; padding: 15px 30px; border-bottom: 1px solid #eee; }}
        .nav-bar a {{ margin-right: 20px; text-decoration: none; color: #667eea; font-weight: 500; }}
        .nav-bar a:hover {{ color: #764ba2; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }}
        .stat-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; padding: 20px; text-align: center; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .stat-card .label {{ margin-top: 5px; color: #666; }}
        .section {{ padding: 30px; border-top: 1px solid #eee; }}
        .section h2 {{ color: #333; margin-bottom: 15px; font-size: 22px; }}
        .section p {{ color: #666; margin-bottom: 15px; }}
        .category-group {{ margin-bottom: 25px; }}
        .category-group h3 {{ color: #444; margin-bottom: 12px; font-size: 16px; padding-left: 10px; border-left: 3px solid #667eea; }}
        .book-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
        .book-card {{ background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; transition: transform 0.2s; }}
        .book-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .book-card.delete {{ border-left-color: #dc3545; }}
        .book-card.consider {{ border-left-color: #ffc107; }}
        .book-card.keep {{ border-left-color: #28a745; }}
        .book-title {{ font-weight: bold; color: #333; margin-bottom: 5px; font-size: 15px; }}
        .book-title a {{ color: #333; text-decoration: none; }}
        .book-title a:hover {{ color: #667eea; text-decoration: underline; }}
        .book-info {{ color: #666; font-size: 13px; }}
        .book-meta {{ display: flex; gap: 10px; margin-top: 8px; font-size: 12px; flex-wrap: wrap; }}
        .book-meta span {{ color: #888; }}
        .read-btn {{ display: inline-block; padding: 3px 8px; background: #667eea; color: white; border-radius: 4px; text-decoration: none; font-size: 11px; }}
        .read-btn:hover {{ background: #764ba2; }}
        .category-list {{ max-height: 400px; overflow-y: auto; }}
        .category-item {{ display: flex; justify-content: space-between; padding: 8px 15px; border-bottom: 1px solid #eee; }}
        .category-item:nth-child(odd) {{ background: #f8f9fa; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 微信读书书架分析报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 共分析 {stats['total']} 本书</p>
        </div>
        <div class="nav-bar">
            <a href="#stats">📊 统计概览</a>
            <a href="#keep">✅ 建议保留</a>
            <a href="#consider">⚠️ 建议考虑</a>
            <a href="#delete">❌ 建议删除</a>
            <a href="#suggestions">💡 整理建议</a>
        </div>
        <div class="section" id="stats">
            <h2>📊 统计概览</h2>
            <div class="stats-grid">
                <div class="stat-card"><div class="number">{stats['total']}</div><div class="label">总书籍</div></div>
                <div class="stat-card"><div class="number">{stats['never_read']}</div><div class="label">从未阅读</div></div>
                <div class="stat-card"><div class="number">{stats['finished']}</div><div class="label">已读完</div></div>
                <div class="stat-card"><div class="number">{stats['high_score']}</div><div class="label">高分书(≥80)</div></div>
                <div class="stat-card"><div class="number">{stats['recent_books']}</div><div class="label">2024+新书</div></div>
                <div class="stat-card"><div class="number">{stats['ai_books']}</div><div class="label">AI主题书</div></div>
            </div>
            <h3 style="margin-top:20px;">分类分布 (前 20)</h3>
            <div class="category-list">
"""
        
        for cat, count in category_stats[:20]:
            html += f'<div class="category-item"><span>{escape_html(cat)}</span><span style="color: #667eea; font-weight: bold;">{count} 本</span></div>\n'
        
        html += """
            </div>
        </div>
"""
        
        html += generate_book_section(keep_candidates, "✅ 建议保留", "keep")
        html += generate_book_section(consider_candidates, "⚠️ 建议考虑", "consider")
        html += generate_book_section(delete_candidates, "❌ 建议删除", "delete")
        
        html += f"""
        <div class="section" id="suggestions">
            <h2>💡 整理建议</h2>
            <ul style="padding-left: 20px; line-height: 2;">
                <li><strong>清理优先</strong>: 删除 {stats['delete_candidates']} 本低分/低价值书籍</li>
                <li><strong>阅读优先</strong>: 从 {stats['keep_candidates']} 本高分书中选择阅读</li>
                <li><strong>AI书籍去重</strong>: 书架中有 {stats['ai_books']} 本AI主题书，建议保留经典</li>
                <li><strong>公众号管理</strong>: 建议单独管理公众号内容</li>
            </ul>
        </div>
        <div class="footer">
            <p>微信读书书架分析报告 · <a href="https://weread.qq.com" target="_blank">前往微信读书</a></p>
        </div>
    </div>
</body>
</html>
"""
        
        html_file = os.path.join(self.output_dir, "index.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ HTML报告已保存到 {html_file}")
        return html_file
    
    def run(self):
        """执行完整分析流程"""
        print("🚀 开始微信读书书架分析...")
        
        # 获取书架
        shelf = self.get_shelf()
        if not shelf:
            print("❌ 获取书架失败，退出")
            return
        
        # 获取书籍详情
        books_details = self.get_all_books_details(shelf)
        
        # 分析书籍
        analysis_result = self.analyze_books(books_details)
        
        # 生成报告
        self.generate_html_report(analysis_result)
        
        # 输出摘要
        stats = analysis_result["stats"]
        print("\n" + "="*50)
        print("📊 分析报告摘要")
        print("="*50)
        print(f"总书籍: {stats['total']}")
        print(f"从未读: {stats['never_read']}")
        print(f"已读完: {stats['finished']}")
        print(f"高分书: {stats['high_score']}")
        print(f"2024+新书: {stats['recent_books']}")
        print(f"AI主题书: {stats['ai_books']}")
        print(f"建议删除: {stats['delete_candidates']}")
        print(f"建议考虑: {stats['consider_candidates']}")
        print(f"建议保留: {stats['keep_candidates']}")
        print("="*50)
        print(f"\n📁 输出目录: {self.output_dir}")
        print("🎉 分析完成！")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="微信读书书架分析工具")
    parser.add_argument("--api-key", required=True, help="WEREAD_API_KEY")
    parser.add_argument("--output-dir", help="输出目录，默认在脚本同级目录的output文件夹")
    
    args = parser.parse_args()
    
    analyzer = WereadAnalyzer(args.api_key, args.output_dir)
    analyzer.run()
