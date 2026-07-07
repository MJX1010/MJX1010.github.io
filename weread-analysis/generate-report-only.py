#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime
from urllib.parse import quote

def escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def normalize_search_keywords(title):
    keywords = str(title or "")
    keywords = re.sub(r"[（(][^）)]*[）)]", " ", keywords)
    keywords = re.sub(r"[“”\"'‘’：:？?!！，,、/\\|]+", " ", keywords)
    keywords = re.sub(r"\s+", " ", keywords).strip()
    return keywords or str(title or "").strip()


def get_book_search_url(title):
    keywords = normalize_search_keywords(title)
    return "https://weread.qq.com/web/search/books?keyword=" + quote(keywords, safe="")


def get_book_url(book):
    book_id = str(book.get("bookId", "") or "")
    title = book.get("title", "")
    if book_id.startswith("MP_WXS_"):
        return f"https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650743514&idx=1&sn={book_id.replace('MP_WXS_', '')}"
    if not book_id or book_id.isdigit() or book_id.startswith("YueWen_"):
        return get_book_search_url(title)
    return f"https://weread.qq.com/web/bookDetail/{quote(book_id, safe='')}"

def generate_book_card(book, status):
    book_id = book.get("bookId", "")
    book_url = get_book_url(book)
    is_mp = book_id.startswith("MP_WXS_")
    return f"""
<div class="book-card {status}">
    <div class="book-title"><a href="{book_url}" target="_blank" rel="noopener noreferrer">{escape_html(book.get("title", ""))}</a></div>
    <div class="book-info">作者: {escape_html(book.get("author", ""))}{' 🔖' if is_mp else ''}</div>
    <div class="book-meta">
        <span>评分: {book.get("newRating", 0)}</span>
        <span>评论: {book.get("newRatingCount", 0)}</span>
        <span>出版: {escape_html(book.get("publishTime", ""))}</span>
        <span><a href="{book_url}" target="_blank" class="read-btn">{'📱' if is_mp else '📖'} 去阅读</a></span>
    </div>
</div>
"""

def main():
    input_dir = os.path.dirname(__file__)
    
    print("📊 加载书籍数据...")
    with open(os.path.join(input_dir, "all-books-details.json"), "r", encoding="utf-8-sig") as f:
        all_books = json.load(f)
    
    print(f"分析 {len(all_books)} 本书...")
    
    stats = {
        "total": len(all_books),
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
    
    for book in all_books:
        rating = book.get("newRating", 0)
        rating_count = book.get("newRatingCount", 0)
        publish_time = book.get("publishTime", "")
        title = book.get("title", "")
        read_update = book.get("readUpdateTime", 0)
        finished = book.get("finishReading", 0)
        
        if read_update == 0:
            stats["never_read"] += 1
        else:
            stats["read_before"] += 1
        if finished == 1:
            stats["finished"] += 1
        
        if rating >= 80:
            stats["high_score"] += 1
        if rating < 50:
            stats["low_score"] += 1
        
        if publish_time.startswith(("2024", "2025", "2026")):
            stats["recent_books"] += 1
        
        if any(keyword in title for keyword in ["ChatGPT", "GPT", "AI", "AIGC", "Midjourney", "Sora", "DeepSeek"]):
            stats["ai_books"] += 1
        
        cat = book.get("categoryName", "未分类")
        category_stats[cat] = category_stats.get(cat, 0) + 1
        
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
    category_stats = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    
    print("🎨 生成HTML报告...")
    
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
        .search-bar {{ background: #fff; padding: 15px 30px; border-bottom: 1px solid #eee; }}
        .search-box {{ width: 100%; max-width: 600px; padding: 12px 20px; border: 2px solid #e0e0e0; border-radius: 30px; font-size: 16px; transition: border-color 0.3s; }}
        .search-box:focus {{ outline: none; border-color: #667eea; }}
        .search-box::placeholder {{ color: #999; }}
        .search-results {{ padding: 15px 30px; background: #fff3e0; border-bottom: 1px solid #ffe0b2; display: none; }}
        .search-results.show {{ display: block; }}
        .search-results h4 {{ color: #e65100; margin-bottom: 10px; }}
        .search-results .result-item {{ display: block; padding: 8px 15px; background: white; border-radius: 8px; margin-bottom: 5px; text-decoration: none; color: #333; }}
        .search-results .result-item:hover {{ background: #f5f5f5; }}
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
        .filter-tabs {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .filter-tab {{ padding: 8px 16px; border: 2px solid #eee; border-radius: 20px; background: white; cursor: pointer; transition: all 0.3s; }}
        .filter-tab.active {{ border-color: #667eea; background: #667eea; color: white; }}
        .category-filter {{ margin-bottom: 15px; }}
        .category-filter select {{ padding: 8px 12px; border: 2px solid #eee; border-radius: 8px; font-size: 14px; }}
        .book-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
        .book-card {{ background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; transition: transform 0.2s; }}
        .book-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .book-card.delete {{ border-left-color: #dc3545; }}
        .book-card.consider {{ border-left-color: #ffc107; }}
        .book-card.keep {{ border-left-color: #28a745; }}
        .book-card.highlight {{ background: #fff3e0; border-left-color: #ff9800; }}
        .book-title {{ font-weight: bold; color: #333; margin-bottom: 5px; font-size: 15px; }}
        .book-title a {{ color: #333; text-decoration: none; }}
        .book-title a:hover {{ color: #667eea; text-decoration: underline; }}
        .book-info {{ color: #666; font-size: 13px; }}
        .book-meta {{ display: flex; gap: 10px; margin-top: 8px; font-size: 12px; flex-wrap: wrap; }}
        .book-meta span {{ color: #888; }}
        .read-btn {{ display: inline-block; padding: 3px 8px; background: #667eea; color: white; border-radius: 4px; text-decoration: none; font-size: 11px; }}
        .read-btn:hover {{ background: #764ba2; }}
        .pagination {{ display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 30px; padding: 20px; border-top: 1px solid #eee; }}
        .pagination button {{ padding: 8px 16px; border: 2px solid #eee; border-radius: 8px; background: white; cursor: pointer; transition: all 0.3s; }}
        .pagination button:hover:not(:disabled) {{ border-color: #667eea; }}
        .pagination button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .pagination button.active {{ background: #667eea; color: white; border-color: #667eea; }}
        .pagination span {{ color: #666; }}
        .category-list {{ max-height: 400px; overflow-y: auto; }}
        .category-item {{ display: flex; justify-content: space-between; padding: 8px 15px; border-bottom: 1px solid #eee; }}
        .category-item:nth-child(odd) {{ background: #f8f9fa; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
        .footer a {{ color: #667eea; text-decoration: none; }}
        .hidden {{ display: none; }}
        .no-results {{ text-align: center; color: #999; padding: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 微信读书书架分析报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 共分析 {stats['total']} 本书</p>
        </div>
        <div class="search-bar">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 搜索书名或作者..." onkeyup="searchBooks()">
        </div>
        <div id="searchResults" class="search-results"></div>
        <div class="nav-bar">
            <a href="#stats">📊 统计概览</a>
            <a href="#books">📖 我的书架</a>
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
        <div class="section" id="books">
            <h2>📖 我的书架</h2>
            <div class="filter-tabs">
                <div class="filter-tab active" onclick="filterBooks('all')">📚 全部 ({stats['total']})</div>
                <div class="filter-tab" onclick="filterBooks('keep')">✅ 建议保留 ({stats['keep_candidates']})</div>
                <div class="filter-tab" onclick="filterBooks('consider')">⚠️ 建议考虑 ({stats['consider_candidates']})</div>
                <div class="filter-tab" onclick="filterBooks('delete')">❌ 建议删除 ({stats['delete_candidates']})</div>
            </div>
            <div class="category-filter">
                <select id="categoryFilter" onchange="filterByCategory()">
                    <option value="">全部分类</option>
"""
    
    for cat, _ in category_stats[:30]:
        html += f'<option value="{escape_html(cat)}">{escape_html(cat)}</option>\n'
    
    html += """
                <option value="公众号">🔖 公众号</option>
            </select>
        </div>
        <div id="bookContainer" class="book-list">
"""
    
    html += "\n".join([generate_book_card(book, "keep" if book in keep_candidates else ("delete" if book in delete_candidates else "consider")) for book in all_books[:50]])
    
    html += """
        </div>
        <div id="pagination" class="pagination">
            <button id="prevBtn" disabled onclick="prevPage()">上一页</button>
            <span id="pageInfo">第 1 页 / 共 ? 页</span>
            <button id="nextBtn" onclick="nextPage()">下一页</button>
        </div>
        </div>
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
    <script>
        var allBooks = ["""
    
    books_data = []
    for book in all_books:
        status = "keep" if book in keep_candidates else ("delete" if book in delete_candidates else "consider")
        books_data.append(f'{{"id":"{book.get("bookId", "")}","title":"{escape_html(book.get("title", ""))}","author":"{escape_html(book.get("author", ""))}","category":"{escape_html(book.get("categoryName", ""))}","status":"{status}"}}')
    
    html += ",".join(books_data)
    
    html += """];
    
        var currentPage = 1;
        var pageSize = 50;
        var currentFilter = 'all';
        var currentCategory = '';
        
        function normalizeSearchKeywords(title) {
            var keywords = String(title || '');
            keywords = keywords.replace(/[（(][^）)]*[）)]/g, ' ');
            keywords = keywords.replace(/[“”"'‘’：:？?!！，,、/\\|]+/g, ' ');
            keywords = keywords.replace(/\\s+/g, ' ').trim();
            return keywords || String(title || '').trim();
        }
        
        function getBookSearchUrl(title) {
            var keywords = normalizeSearchKeywords(title);
            return 'https://weread.qq.com/web/search/books?keyword=' + encodeURIComponent(keywords);
        }
        
        function shouldUseSearchUrl(bookId) {
            return !bookId || /^\\d+$/.test(bookId) || bookId.startsWith('YueWen_');
        }
        
        function getBookUrl(bookId, title, author) {
            if (bookId && bookId.startsWith('MP_WXS_')) {
                return 'https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650743514&idx=1&sn=' + bookId.replace('MP_WXS_', '');
            }
            if (shouldUseSearchUrl(bookId)) {
                return getBookSearchUrl(title);
            }
            return 'https://weread.qq.com/web/bookDetail/' + encodeURIComponent(bookId);
        }
        
        function renderBooks() {
            var filtered = allBooks;
            
            if (currentFilter !== 'all') {
                filtered = filtered.filter(function(b) { return b.status === currentFilter; });
            }
            
            if (currentCategory) {
                if (currentCategory === '公众号') {
                    filtered = filtered.filter(function(b) { return b.id.startsWith('MP_WXS_'); });
                } else {
                    filtered = filtered.filter(function(b) { return b.category === currentCategory; });
                }
            }
            
            var totalPages = Math.ceil(filtered.length / pageSize);
            var start = (currentPage - 1) * pageSize;
            var end = start + pageSize;
            var pageBooks = filtered.slice(start, end);
            
            var container = document.getElementById('bookContainer');
            var pagination = document.getElementById('pagination');
            var pageInfo = document.getElementById('pageInfo');
            var prevBtn = document.getElementById('prevBtn');
            var nextBtn = document.getElementById('nextBtn');
            
            if (pageBooks.length === 0) {
                container.innerHTML = '<div class="no-results">😕 没有找到匹配的书籍</div>';
                pagination.style.display = 'none';
                return;
            }
            
            pagination.style.display = 'flex';
            pageInfo.textContent = '第 ' + currentPage + ' 页 / 共 ' + totalPages + ' 页';
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage >= totalPages;
            
            var html = '';
            pageBooks.forEach(function(book) {
                var url = getBookUrl(book.id, book.title, book.author);
                var isMp = book.id.startsWith('MP_WXS_');
                html += '<div class="book-card ' + book.status + '">';
                html += '<div class="book-title"><a href="' + url + '" target="_blank">' + book.title + '</a></div>';
                html += '<div class="book-info">作者: ' + book.author + (isMp ? ' 🔖' : '') + '</div>';
                html += '<div class="book-meta">';
                html += '<span>分类: ' + book.category + '</span>';
                html += '<span><a href="' + url + '" target="_blank" class="read-btn">' + (isMp ? '📱' : '📖') + ' 去阅读</a></span>';
                html += '</div></div>';
            });
            
            container.innerHTML = html;
        }
        
        function filterBooks(filter) {
            currentFilter = filter;
            currentPage = 1;
            document.querySelectorAll('.filter-tab').forEach(function(t) { t.classList.remove('active'); });
            if (event && event.target) {
                event.target.classList.add('active');
            }
            renderBooks();
        }
        
        function filterByCategory() {
            currentCategory = document.getElementById('categoryFilter').value;
            currentPage = 1;
            renderBooks();
        }
        
        function prevPage() {
            if (currentPage > 1) {
                currentPage--;
                renderBooks();
            }
        }
        
        function nextPage() {
            var filtered = allBooks;
            if (currentFilter !== 'all') {
                filtered = filtered.filter(function(b) { return b.status === currentFilter; });
            }
            if (currentCategory) {
                if (currentCategory === '公众号') {
                    filtered = filtered.filter(function(b) { return b.id.startsWith('MP_WXS_'); });
                } else {
                    filtered = filtered.filter(function(b) { return b.category === currentCategory; });
                }
            }
            var totalPages = Math.ceil(filtered.length / pageSize);
            if (currentPage < totalPages) {
                currentPage++;
                renderBooks();
            }
        }
        
        function searchBooks() {
            var input = document.getElementById('searchInput').value.toLowerCase().trim();
            if (!input) {
                currentFilter = 'all';
                currentCategory = '';
                currentPage = 1;
                document.querySelectorAll('.filter-tab').forEach(function(t) { t.classList.remove('active'); });
                document.querySelectorAll('.filter-tab')[0].classList.add('active');
                document.getElementById('categoryFilter').value = '';
                renderBooks();
                return;
            }
            
            var matches = allBooks.filter(function(b) {
                return b.title.toLowerCase().includes(input) || b.author.toLowerCase().includes(input);
            });
            
            var pageBooks = matches.slice(0, pageSize);
            var container = document.getElementById('bookContainer');
            
            if (pageBooks.length === 0) {
                container.innerHTML = '<div class="no-results">😕 没有找到匹配的书籍</div>';
                document.getElementById('pagination').style.display = 'none';
                return;
            }
            
            document.getElementById('pagination').style.display = 'none';
            
            var html = '<div style="margin-bottom:10px;color:#667eea;">搜索到 ' + matches.length + ' 本匹配的书籍</div>';
            pageBooks.forEach(function(book) {
                var url = getBookUrl(book.id, book.title, book.author);
                var isMp = book.id.startsWith('MP_WXS_');
                html += '<div class="book-card ' + book.status + '">';
                html += '<div class="book-title"><a href="' + url + '" target="_blank">' + book.title + '</a></div>';
                html += '<div class="book-info">作者: ' + book.author + (isMp ? ' 🔖' : '') + '</div>';
                html += '<div class="book-meta">';
                html += '<span>分类: ' + book.category + '</span>';
                html += '<span><a href="' + url + '" target="_blank" class="read-btn">' + (isMp ? '📱' : '📖') + ' 去阅读</a></span>';
                html += '</div></div>';
            });
            
            container.innerHTML = html;
        }
        
        renderBooks();
    </script>
</body>
</html>"""
    
    with open(os.path.join(input_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ HTML报告已保存")

if __name__ == "__main__":
    main()
