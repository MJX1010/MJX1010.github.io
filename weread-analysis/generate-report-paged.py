#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

def classify_book(title, author, original_category, book_id):
    if original_category and original_category != "未分类":
        return original_category
    
    if book_id.startswith('MP_WXS_'):
        return "公众号"
    
    title_lower = title.lower()
    author_lower = author.lower()
    
    categories = {
        "计算机/编程": ["编程", "代码", "程序", "python", "java", "javascript", "js", "前端", "后端", "算法", "数据结构", "数据库", "网络", "架构", "设计模式", "开发", "工程师", "git", "linux", "shell", "docker", "kubernetes", "云原生", "api", "react", "vue", "angular", "node", "spring", "django", "flask", "typescript", "rust", "go语言", "golang", "c++", "c#", "swift", "kotlin", "算法导论", "数据挖掘"],
        "AI/人工智能": ["人工智能", "机器学习", "深度学习", "神经网络", "chatgpt", "gpt", "ai", "aigc", "大模型", "prompt", "midjourney", "sora", "deepseek", "tensorflow", "pytorch", "数据挖掘", "自然语言", "图像识别", "推荐系统", "强化学习", "计算机视觉", "nlp", "transformer"],
        "经济/金融": ["经济", "金融", "投资", "股票", "基金", "理财", "货币", "银行", "证券", "保险", "比特币", "区块链", "量化", "估值", "财报", "财务", "会计", "宏观", "微观", "经济学", "央行"],
        "管理/商业": ["管理", "商业", "创业", "营销", "销售", "产品", "运营", "领导力", "团队", "战略", "品牌", "市场", "客户", "商业模式", "企业", "组织", "创新", "竞争"],
        "科技/互联网": ["科技", "互联网", "数码", "电子", "芯片", "半导体", "通信", "5g", "物联网", "大数据", "云计算", "安全", "隐私", "数字", "软件", "硬件", "手机", "智能", "互联网+"],
        "文学小说": ["小说", "文学", "故事", "爱情", "悬疑", "推理", "科幻", "奇幻", "穿越", "言情", "武侠", "都市", "青春", "校园", "历史小说", "长篇", "短篇", "经典文学"],
        "历史/传记": ["历史", "传记", "自传", "人物", "文明", "朝代", "战争", "古代", "近现代", "世界史", "中国史", "名人", "回忆录", "史记", "三国志"],
        "心理学": ["心理", "情绪", "认知", "行为", "人格", "社交", "沟通", "情商", "压力", "焦虑", "抑郁", "正念", "潜意识", "精神", "心理治疗", "积极心理学"],
        "健康/养生": ["健康", "养生", "饮食", "营养", "运动", "健身", "跑步", "瑜伽", "睡眠", "冥想", "中医", "食疗", "抗炎", "免疫", "减肥", "减脂", "增肌", "康复"],
        "教育/学习": ["学习", "教育", "考试", "考研", "高考", "英语", "语言", "阅读", "写作", "记忆", "思维", "方法论", "时间管理", "效率", "学习方法", "脑科学"],
        "生活/家居": ["生活", "家居", "旅行", "美食", "烹饪", "手工", "收纳", "整理", "宠物", "育儿", "亲子", "婚姻", "家庭", "情感", "人际关系"],
        "投资理财": ["理财", "投资", "基金", "股票", "债券", "黄金", "房产", "资产", "配置", "风险", "收益", "复利", "定投", "价值投资", "指数基金"],
        "政治/社会": ["政治", "社会", "法律", "哲学", "伦理", "文化", "社会学", "国际关系", "公共政策", "政府", "制度", "民主", "自由"],
        "艺术/设计": ["艺术", "设计", "绘画", "音乐", "摄影", "建筑", "电影", "创意", "美学", "插画", "平面设计", "UI设计", "交互设计"],
        "科普/百科": ["科学", "科普", "自然", "宇宙", "物理", "化学", "生物", "天文", "地理", "科普读物", "百科", "探索", "发现"],
        "童书/绘本": ["儿童", "绘本", "童话", "故事书", "启蒙", "早教", "亲子阅读", "图画书", "寓言"],
        "工具书": ["词典", "手册", "指南", "教程", "全集", "大全", "百科全书", "手册", "年鉴"],
        "军事/战争": ["军事", "战争", "战略", "武器", "军队", "国防", "二战", "抗战"],
        "法律/法规": ["法律", "法规", "律师", "司法", "诉讼", "宪法", "民法", "刑法"],
        "哲学/宗教": ["哲学", "宗教", "佛学", "禅", "道", "儒家", "西方哲学", "存在主义"],
        "旅游/地理": ["旅游", "旅行", "地理", "游记", "探险", "环球", "城市"],
        "美食/烹饪": ["美食", "烹饪", "菜谱", "烘焙", "料理", "饮食文化"],
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title_lower or keyword.lower() in author_lower:
                return category
    
    return "其他"

def get_publish_time_category(publish_time):
    if not publish_time:
        return "未知年份"
    
    try:
        if publish_time.startswith(("2024", "2025", "2026")):
            return "📅 2024年后"
        elif publish_time.startswith(("2020", "2021", "2022", "2023")):
            return "📅 2020-2023"
        elif publish_time.startswith(("2015", "2016", "2017", "2018", "2019")):
            return "📅 2015-2019"
        elif publish_time.startswith(("2010", "2011", "2012", "2013", "2014")):
            return "📅 2010-2014"
        elif publish_time.startswith(("2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009")):
            return "📅 2000-2009"
        elif int(publish_time[:4]) < 2000:
            return "📅 2000年前"
    except:
        pass
    
    return "未知年份"

def main():
    input_dir = os.path.dirname(__file__)
    
    print("📊 加载书籍数据...")
    with open(os.path.join(input_dir, "all-books-details.json"), "r", encoding="utf-8-sig") as f:
        all_books = json.load(f)
    
    stats = {
        "total": len(all_books),
        "never_read": sum(1 for b in all_books if b.get("readUpdateTime", 0) == 0),
        "finished": sum(1 for b in all_books if b.get("finishReading", 0) == 1),
        "high_score": sum(1 for b in all_books if b.get("newRating", 0) >= 80),
        "recent_books": sum(1 for b in all_books if b.get("publishTime", "").startswith(("2024", "2025", "2026"))),
        "ai_books": sum(1 for b in all_books if any(k in b.get("title", "") for k in ["ChatGPT", "GPT", "AI", "AIGC", "Midjourney", "Sora", "DeepSeek"])),
    }
    
    category_stats = {}
    for book in all_books:
        original_cat = book.get("categoryName", "未分类")
        book_id = book.get("bookId", "")
        cat = classify_book(book.get("title", ""), book.get("author", ""), original_cat, book_id)
        category_stats[cat] = category_stats.get(cat, 0) + 1
    category_stats = sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
    
    publish_time_stats = {}
    for book in all_books:
        publish_time = book.get("publishTime", "")
        time_cat = get_publish_time_category(publish_time)
        publish_time_stats[time_cat] = publish_time_stats.get(time_cat, 0) + 1
    
    print("🎨 生成HTML报告...")
    
    books_json_lines = []
    for book in all_books:
        rating = book.get("newRating", 0)
        rating_count = book.get("newRatingCount", 0)
        publish_time = book.get("publishTime", "")
        title = book.get("title", "")
        book_id = book.get("bookId", "")
        
        score = 0
        if rating >= 80: score += 3
        elif rating >= 60: score += 1
        else: score -= 2
        
        if rating_count >= 100: score += 2
        elif rating_count >= 10: score += 1
        
        if publish_time.startswith(("2024", "2025", "2026")): score += 2
        elif publish_time.startswith(("2020", "2021", "2022", "2023")): score += 1
        
        if any(k in title for k in ["入门", "实战", "图解", "轻松上手", "一本通"]): score -= 1
        
        status = "keep" if score >= 4 else ("delete" if score <= 0 else "consider")
        
        original_cat = book.get("categoryName", "未分类")
        category = classify_book(title, book.get("author", ""), original_cat, book_id)
        time_category = get_publish_time_category(publish_time)
        
        title_escaped = book.get("title", "").replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
        author_escaped = book.get("author", "").replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
        
        books_json_lines.append(f'            {{"id":"{book_id}","title":"{title_escaped}","author":"{author_escaped}","category":"{category}","timeCategory":"{time_category}","status":"{status}","rating":{rating},"ratingCount":{rating_count},"publishTime":"{publish_time}"}}')
    
    html_parts = []
    
    html_parts.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信读书书架分析报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .search-bar { background: #fff; padding: 15px 30px; border-bottom: 1px solid #eee; }
        .search-box { width: 100%; max-width: 600px; padding: 12px 20px; border: 2px solid #e0e0e0; border-radius: 30px; font-size: 16px; }
        .search-box:focus { outline: none; border-color: #667eea; }
        .nav-bar { background: #f8f9fa; padding: 15px 30px; border-bottom: 1px solid #eee; }
        .nav-bar a { margin-right: 20px; text-decoration: none; color: #667eea; font-weight: 500; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }
        .stat-card { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; padding: 20px; text-align: center; }
        .stat-card .number { font-size: 36px; font-weight: bold; color: #667eea; }
        .stat-card .label { margin-top: 5px; color: #666; }
        .section { padding: 30px; border-top: 1px solid #eee; }
        .section h2 { color: #333; margin-bottom: 15px; font-size: 22px; }
        .filter-tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .filter-tab { padding: 8px 16px; border: 2px solid #eee; border-radius: 20px; background: white; cursor: pointer; }
        .filter-tab.active { border-color: #667eea; background: #667eea; color: white; }
        .category-filter { display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap; align-items: center; }
        .category-filter select { padding: 8px 12px; border: 2px solid #eee; border-radius: 8px; font-size: 14px; width: 180px; }
        .book-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }
        .book-card { background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; }
        .book-card.delete { border-left-color: #dc3545; }
        .book-card.consider { border-left-color: #ffc107; }
        .book-card.keep { border-left-color: #28a745; }
        .book-title { font-weight: bold; color: #333; margin-bottom: 5px; font-size: 15px; }
        .book-title a { color: #333; text-decoration: none; }
        .book-title a:hover { color: #667eea; }
        .book-info { color: #666; font-size: 13px; }
        .book-meta { display: flex; gap: 10px; margin-top: 8px; font-size: 12px; flex-wrap: wrap; color: #888; }
        .read-btn { display: inline-block; padding: 3px 8px; background: #667eea; color: white; border-radius: 4px; text-decoration: none; font-size: 11px; }
        .pagination { display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 30px; padding: 20px; border-top: 1px solid #eee; }
        .pagination button { padding: 8px 16px; border: 2px solid #eee; border-radius: 8px; background: white; cursor: pointer; }
        .pagination button:hover:not(:disabled) { border-color: #667eea; }
        .pagination button:disabled { opacity: 0.5; }
        .pagination span { color: #666; }
        .category-list { max-height: 400px; overflow-y: auto; }
        .category-item { display: flex; justify-content: space-between; padding: 8px 15px; border-bottom: 1px solid #eee; }
        .category-item:nth-child(odd) { background: #f8f9fa; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }
        .footer a { color: #667eea; }
        .no-results { text-align: center; color: #999; padding: 40px; }
        .category-group { margin-bottom: 25px; }
        .category-header { background: #f5f7fa; padding: 12px 15px; border-radius: 8px; margin-bottom: 12px; }
        .category-header h3 { margin: 0; color: #333; font-size: 16px; }
        .time-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 12px; border-radius: 6px; margin-bottom: 10px; font-size: 14px; }
        .sort-info { font-size: 12px; color: #999; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 微信读书书架分析报告</h1>
            <p>生成时间: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ''' | 共分析 ''' + str(stats["total"]) + ''' 本书</p>
        </div>
        <div class="search-bar">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 搜索书名或作者..." onkeyup="searchBooks()">
        </div>
        <div class="nav-bar">
            <a href="#stats">📊 统计概览</a>
            <a href="#books">📖 我的书架</a>
            <a href="#suggestions">💡 整理建议</a>
        </div>
        <div class="section" id="stats">
            <h2>📊 统计概览</h2>
            <div class="stats-grid">
                <div class="stat-card"><div class="number">''' + str(stats["total"]) + '''</div><div class="label">总书籍</div></div>
                <div class="stat-card"><div class="number">''' + str(stats["never_read"]) + '''</div><div class="label">从未阅读</div></div>
                <div class="stat-card"><div class="number">''' + str(stats["finished"]) + '''</div><div class="label">已读完</div></div>
                <div class="stat-card"><div class="number">''' + str(stats["high_score"]) + '''</div><div class="label">高分书(≥80)</div></div>
                <div class="stat-card"><div class="number">''' + str(stats["recent_books"]) + '''</div><div class="label">2024+新书</div></div>
                <div class="stat-card"><div class="number">''' + str(stats["ai_books"]) + '''</div><div class="label">AI主题书</div></div>
            </div>
            <h3 style="margin-top:20px;">分类分布 (共 ''' + str(len(category_stats)) + ''' 个分类)</h3>
            <div class="category-list">''')
    
    for cat, count in category_stats:
        html_parts.append(f'                <div class="category-item"><span>{cat}</span><span style="color: #667eea; font-weight: bold;">{count} 本</span></div>')
    
    html_parts.append('''            </div>
            <h3 style="margin-top:20px;">出版年份分布</h3>
            <div class="category-list">''')
    
    for time_cat in ["📅 2024年后", "📅 2020-2023", "📅 2015-2019", "📅 2010-2014", "📅 2000-2009", "📅 2000年前", "未知年份"]:
        count = publish_time_stats.get(time_cat, 0)
        html_parts.append(f'                <div class="category-item"><span>{time_cat}</span><span style="color: #667eea; font-weight: bold;">{count} 本</span></div>')
    
    html_parts.append('''            </div>
        </div>
        <div class="section" id="books">
            <h2>📖 我的书架</h2>
            <div class="filter-tabs">
                <div class="filter-tab active" onclick="filterBooks('all')">📚 全部</div>
                <div class="filter-tab" onclick="filterBooks('keep')">✅ 建议保留</div>
                <div class="filter-tab" onclick="filterBooks('consider')">⚠️ 建议考虑</div>
                <div class="filter-tab" onclick="filterBooks('delete')">❌ 建议删除</div>
            </div>
            <div class="category-filter">
                <select id="categoryFilter" onchange="filterByCategory()">
                    <option value="">全部内容分类</option>''')
    
    for cat, _ in category_stats:
        html_parts.append(f'                    <option value="{cat}">{cat}</option>')
    
    html_parts.append('''                </select>
                <select id="timeFilter" onchange="filterByTime()">
                    <option value="">全部出版时间</option>
                    <option value="📅 2024年后">📅 2024年后</option>
                    <option value="📅 2020-2023">📅 2020-2023</option>
                    <option value="📅 2015-2019">📅 2015-2019</option>
                    <option value="📅 2010-2014">📅 2010-2014</option>
                    <option value="📅 2000-2009">📅 2000-2009</option>
                    <option value="📅 2000年前">📅 2000年前</option>
                </select>
            </div>
            <div class="sort-info">🔄 书籍按出版时间从新到旧排序</div>
            <div id="bookContainer" class="book-list"></div>
            <div id="pagination" class="pagination">
                <button id="prevBtn" disabled onclick="prevPage()">上一页</button>
                <span id="pageInfo">第 1 页 / 共 ? 页</span>
                <button id="nextBtn" onclick="nextPage()">下一页</button>
            </div>
        </div>
        <div class="section" id="suggestions">
            <h2>💡 整理建议</h2>
            <ul style="padding-left: 20px; line-height: 2;">
                <li><strong>清理优先</strong>: 删除低分/低价值书籍</li>
                <li><strong>阅读优先</strong>: 从高分书中选择阅读</li>
                <li><strong>AI书籍去重</strong>: 书架中有 ''' + str(stats["ai_books"]) + ''' 本AI主题书，建议保留经典</li>
                <li><strong>公众号管理</strong>: 建议单独管理公众号内容</li>
            </ul>
        </div>
        <div class="footer">
            <p>微信读书书架分析报告 · <a href="https://weread.qq.com" target="_blank">前往微信读书</a></p>
        </div>
    </div>
    <script>
        var allBooks = [
''')
    
    html_parts.append(",\n".join(books_json_lines))
    
    html_parts.append('''
        ];
        
        var currentPage = 1;
        var pageSize = 50;
        var currentFilter = 'all';
        var currentCategory = '';
        var currentTimeFilter = '';
        
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
        
        function groupBooksByCategoryAndTime(books) {
            var groups = {};
            books.forEach(function(book) {
                var cat = book.category || '其他';
                if (!groups[cat]) {
                    groups[cat] = {};
                }
                var timeCat = book.timeCategory || '未知年份';
                if (!groups[cat][timeCat]) {
                    groups[cat][timeCat] = [];
                }
                groups[cat][timeCat].push(book);
            });
            
            var sortedGroups = [];
            Object.keys(groups).sort().forEach(function(cat) {
                var timeGroups = [];
                var timeOrder = ['📅 2024年后', '📅 2020-2023', '📅 2015-2019', '📅 2010-2014', '📅 2000-2009', '📅 2000年前', '未知年份'];
                timeOrder.forEach(function(timeCat) {
                    if (groups[cat][timeCat]) {
                        groups[cat][timeCat].sort(function(a, b) {
                            return (b.publishTime || '').localeCompare(a.publishTime || '');
                        });
                        timeGroups.push({ timeCategory: timeCat, books: groups[cat][timeCat] });
                    }
                });
                Object.keys(groups[cat]).forEach(function(timeCat) {
                    if (timeOrder.indexOf(timeCat) === -1) {
                        groups[cat][timeCat].sort(function(a, b) {
                            return (b.publishTime || '').localeCompare(a.publishTime || '');
                        });
                        timeGroups.push({ timeCategory: timeCat, books: groups[cat][timeCat] });
                    }
                });
                sortedGroups.push({ category: cat, timeGroups: timeGroups });
            });
            return sortedGroups;
        }
        
        function renderBooks() {
            var filtered = allBooks;
            
            if (currentFilter !== 'all') {
                filtered = filtered.filter(function(b) { return b.status === currentFilter; });
            }
            
            if (currentCategory) {
                filtered = filtered.filter(function(b) { return b.category === currentCategory; });
            }
            
            if (currentTimeFilter) {
                filtered = filtered.filter(function(b) { return b.timeCategory === currentTimeFilter; });
            }
            
            var totalPages = Math.ceil(filtered.length / pageSize);
            var start = (currentPage - 1) * pageSize;
            var end = start + pageSize;
            var pageBooks = filtered.slice(start, end);
            
            var container = document.getElementById('bookContainer');
            var pageInfo = document.getElementById('pageInfo');
            var prevBtn = document.getElementById('prevBtn');
            var nextBtn = document.getElementById('nextBtn');
            
            if (pageBooks.length === 0) {
                container.innerHTML = '<div class="no-results">😕 没有找到匹配的书籍</div>';
                document.getElementById('pagination').style.display = 'none';
                return;
            }
            
            document.getElementById('pagination').style.display = 'flex';
            pageInfo.textContent = '第 ' + currentPage + ' 页 / 共 ' + totalPages + ' 页';
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage >= totalPages;
            
            var groupedBooks = groupBooksByCategoryAndTime(pageBooks);
            
            var html = '';
            groupedBooks.forEach(function(group) {
                html += '<div class="category-group">';
                var totalBooks = group.timeGroups.reduce(function(sum, tg) { return sum + tg.books.length; }, 0);
                html += '<div class="category-header"><h3>📁 ' + group.category + ' (' + totalBooks + '本)</h3></div>';
                group.timeGroups.forEach(function(timeGroup) {
                    html += '<div class="time-header">' + timeGroup.timeCategory + ' (' + timeGroup.books.length + '本)</div>';
                    html += '<div class="book-list">';
                    timeGroup.books.forEach(function(book) {
                        var url = getBookUrl(book.id, book.title, book.author);
                        var isMp = book.id.startsWith('MP_WXS_');
                        html += '<div class="book-card ' + book.status + '">';
                        html += '<div class="book-title"><a href="' + url + '" target="_blank">' + book.title + '</a></div>';
                        html += '<div class="book-info">作者: ' + book.author + (isMp ? ' 🔖' : '') + '</div>';
                        html += '<div class="book-meta">';
                        html += '<span>评分: ' + book.rating + '</span>';
                        html += '<span>评论: ' + book.ratingCount + '</span>';
                        html += '<span>出版: ' + (book.publishTime || '未知') + '</span>';
                        html += '<span><a href="' + url + '" target="_blank" class="read-btn">' + (isMp ? '📱' : '📖') + ' 去阅读</a></span>';
                        html += '</div></div>';
                    });
                    html += '</div>';
                });
                html += '</div>';
            });
            
            container.innerHTML = html;
        }
        
        function filterBooks(filter) {
            currentFilter = filter;
            currentPage = 1;
            document.querySelectorAll('.filter-tab').forEach(function(t) { t.classList.remove('active'); });
            event.target.classList.add('active');
            renderBooks();
        }
        
        function filterByCategory() {
            currentCategory = document.getElementById('categoryFilter').value;
            currentPage = 1;
            renderBooks();
        }
        
        function filterByTime() {
            currentTimeFilter = document.getElementById('timeFilter').value;
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
                filtered = filtered.filter(function(b) { return b.category === currentCategory; });
            }
            if (currentTimeFilter) {
                filtered = filtered.filter(function(b) { return b.timeCategory === currentTimeFilter; });
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
                currentTimeFilter = '';
                currentPage = 1;
                document.querySelectorAll('.filter-tab').forEach(function(t) { t.classList.remove('active'); });
                document.querySelectorAll('.filter-tab')[0].classList.add('active');
                document.getElementById('categoryFilter').value = '';
                document.getElementById('timeFilter').value = '';
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
            
            var groupedBooks = groupBooksByCategoryAndTime(pageBooks);
            
            var html = '<div style="margin-bottom:10px;color:#667eea;">搜索到 ' + matches.length + ' 本匹配的书籍</div>';
            groupedBooks.forEach(function(group) {
                html += '<div class="category-group">';
                var totalBooks = group.timeGroups.reduce(function(sum, tg) { return sum + tg.books.length; }, 0);
                html += '<div class="category-header"><h3>📁 ' + group.category + ' (' + totalBooks + '本)</h3></div>';
                group.timeGroups.forEach(function(timeGroup) {
                    html += '<div class="time-header">' + timeGroup.timeCategory + ' (' + timeGroup.books.length + '本)</div>';
                    html += '<div class="book-list">';
                    timeGroup.books.forEach(function(book) {
                        var url = getBookUrl(book.id, book.title, book.author);
                        var isMp = book.id.startsWith('MP_WXS_');
                        html += '<div class="book-card ' + book.status + '">';
                        html += '<div class="book-title"><a href="' + url + '" target="_blank">' + book.title + '</a></div>';
                        html += '<div class="book-info">作者: ' + book.author + (isMp ? ' 🔖' : '') + '</div>';
                        html += '<div class="book-meta">';
                        html += '<span>评分: ' + book.rating + '</span>';
                        html += '<span><a href="' + url + '" target="_blank" class="read-btn">' + (isMp ? '📱' : '📖') + ' 去阅读</a></span>';
                        html += '</div></div>';
                    });
                    html += '</div>';
                });
                html += '</div>';
            });
            
            container.innerHTML = html;
        }
        
        renderBooks();
    </script>
</body>
</html>''')
    
    html_content = "\n".join(html_parts)
    
    with open(os.path.join(input_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ HTML报告已保存")

if __name__ == "__main__":
    main()
