import json
import os
from datetime import datetime

output_dir = r"d:\Notes\MJX1010.github.io\weread-analysis"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "all-books-details.json"), "r", encoding="utf-8-sig") as f:
    all_books = json.load(f)

print(f"分析 {len(all_books)} 本书...")

never_read = [b for b in all_books if b.get("readUpdateTime", 0) == 0]
read_before = [b for b in all_books if b.get("readUpdateTime", 0) != 0]
finished = [b for b in all_books if b.get("finishReading", 0) == 1]
high_score = [b for b in all_books if b.get("newRating", 0) >= 80]
low_score = [b for b in all_books if b.get("newRating", 0) < 50]
recent_books = [b for b in all_books if "publishTime" in b and b["publishTime"].startswith(("2024", "2025", "2026"))]

category_stats = {}
for book in all_books:
    cat = book.get("categoryName", "未分类")
    category_stats[cat] = category_stats.get(cat, 0) + 1
category_stats = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)

ai_books = [b for b in all_books if any(keyword in b.get("title", "") for keyword in ["ChatGPT", "GPT", "AI", "AIGC", "Midjourney", "Sora", "DeepSeek"])]

delete_candidates = []
keep_candidates = []
consider_candidates = []

for book in all_books:
    score = 0
    rating = book.get("newRating", 0)
    rating_count = book.get("newRatingCount", 0)
    publish_time = book.get("publishTime", "")
    title = book.get("title", "")
    
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

def escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

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
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }}
        .stat-card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; padding: 20px; text-align: center; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .stat-card .label {{ margin-top: 5px; color: #666; }}
        .section {{ padding: 30px; border-top: 1px solid #eee; }}
        .section h2 {{ color: #333; margin-bottom: 20px; font-size: 22px; }}
        .book-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
        .book-card {{ background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; }}
        .book-card.delete {{ border-left-color: #dc3545; }}
        .book-card.consider {{ border-left-color: #ffc107; }}
        .book-card.keep {{ border-left-color: #28a745; }}
        .book-title {{ font-weight: bold; color: #333; margin-bottom: 5px; }}
        .book-info {{ color: #666; font-size: 14px; }}
        .book-meta {{ display: flex; gap: 15px; margin-top: 8px; font-size: 12px; }}
        .category-list {{ max-height: 400px; overflow-y: auto; }}
        .category-item {{ display: flex; justify-content: space-between; padding: 8px 15px; border-bottom: 1px solid #eee; }}
        .category-item:nth-child(odd) {{ background: #f8f9fa; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 微信读书书架分析报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 共分析 {len(all_books)} 本书</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="number">{len(all_books)}</div><div class="label">总书籍</div></div>
            <div class="stat-card"><div class="number">{len(never_read)}</div><div class="label">从未阅读</div></div>
            <div class="stat-card"><div class="number">{len(finished)}</div><div class="label">已读完</div></div>
            <div class="stat-card"><div class="number">{len(high_score)}</div><div class="label">高分书(≥80)</div></div>
            <div class="stat-card"><div class="number">{len(recent_books)}</div><div class="label">2024+新书</div></div>
            <div class="stat-card"><div class="number">{len(ai_books)}</div><div class="label">AI主题书</div></div>
        </div>
        <div class="section">
            <h2>📊 分类分布 (前 20)</h2>
            <div class="category-list">
"""

for cat, count in category_stats[:20]:
    html += f'<div class="category-item"><span>{escape_html(cat)}</span><span style="color: #667eea; font-weight: bold;">{count} 本</span></div>\n'

html += """
            </div>
        </div>
        <div class="section">
            <h2>❌ 建议删除 ({} 本)</h2>
            <p style="color:#666; margin-bottom:15px;">显示前 200 本（共 {} 本）</p>
            <div class="book-list">
""".format(len(delete_candidates), len(delete_candidates))

for book in delete_candidates[:200]:
    html += f"""
<div class="book-card delete"><div class="book-title">{escape_html(book.get("title", ""))}</div><div class="book-info">作者: {escape_html(book.get("author", ""))}</div><div class="book-meta"><span>评分: {book.get("newRating", 0)}</span><span>评论: {book.get("newRatingCount", 0)}</span><span>出版: {escape_html(book.get("publishTime", ""))}</span></div></div>
"""

html += """
            </div>
        </div>
        <div class="section">
            <h2>⚠️ 建议考虑 ({} 本)</h2>
            <p style="color:#666; margin-bottom:15px;">显示前 100 本（共 {} 本）</p>
            <div class="book-list">
""".format(len(consider_candidates), len(consider_candidates))

for book in consider_candidates[:100]:
    html += f"""
<div class="book-card consider"><div class="book-title">{escape_html(book.get("title", ""))}</div><div class="book-info">作者: {escape_html(book.get("author", ""))}</div><div class="book-meta"><span>评分: {book.get("newRating", 0)}</span><span>评论: {book.get("newRatingCount", 0)}</span><span>出版: {escape_html(book.get("publishTime", ""))}</span></div></div>
"""

html += """
            </div>
        </div>
        <div class="section">
            <h2>✅ 建议保留 ({} 本)</h2>
            <p style="color:#666; margin-bottom:15px;">显示前 200 本（共 {} 本）</p>
            <div class="book-list">
""".format(len(keep_candidates), len(keep_candidates))

for book in keep_candidates[:200]:
    html += f"""
<div class="book-card keep"><div class="book-title">{escape_html(book.get("title", ""))}</div><div class="book-info">作者: {escape_html(book.get("author", ""))}</div><div class="book-meta"><span>评分: {book.get("newRating", 0)}</span><span>评论: {book.get("newRatingCount", 0)}</span><span>出版: {escape_html(book.get("publishTime", ""))}</span></div></div>
"""

html += f"""
            </div>
        </div>
        <div class="section">
            <h2>💡 整理建议</h2>
            <ul style="padding-left: 20px; line-height: 2;">
                <li><strong>清理优先</strong>: 删除 {len(delete_candidates)} 本低分/低价值书籍</li>
                <li><strong>阅读优先</strong>: 从 {len(keep_candidates)} 本高分书中选择阅读</li>
                <li><strong>AI书籍去重</strong>: 书架中有 {len(ai_books)} 本AI主题书，建议保留经典</li>
                <li><strong>公众号管理</strong>: 建议单独管理公众号内容</li>
            </ul>
        </div>
        <div class="footer">
            <p>微信读书书架分析报告 · 由 weread-skills 生成</p>
        </div>
    </div>
</body>
</html>
"""

with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML 报告已保存到 {os.path.join(output_dir, 'index.html')}")
print(f"--- 报告摘要 ---")
print(f"总书籍: {len(all_books)}")
print(f"从未读: {len(never_read)}")
print(f"已读完: {len(finished)}")
print(f"建议删除: {len(delete_candidates)}")
print(f"建议保留: {len(keep_candidates)}")
