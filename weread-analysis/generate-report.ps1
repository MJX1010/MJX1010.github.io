$outputDir = "d:\Notes\MJX1010.github.io\weread-analysis"
$allBookDetails = Get-Content "$outputDir/all-books-details.json" -Raw | ConvertFrom-Json

Write-Host "分析 $($allBookDetails.Count) 本书..."

$neverRead = $allBookDetails | Where-Object { $_.readUpdateTime -eq 0 }
$readBefore = $allBookDetails | Where-Object { $_.readUpdateTime -ne 0 }
$finished = $allBookDetails | Where-Object { $_.finishReading -eq 1 }
$highScore = $allBookDetails | Where-Object { $_.newRating -ge 80 }
$lowScore = $allBookDetails | Where-Object { $_.newRating -lt 50 }
$recentBooks = $allBookDetails | Where-Object { $_.publishTime -match "202[4-6]" }

$categoryStats = $allBookDetails | Group-Object -Property categoryName | Sort-Object -Property Count -Descending
$aiBooks = $allBookDetails | Where-Object { $_.title -match "ChatGPT|GPT|AI|AIGC|Midjourney|Sora|DeepSeek" }

$deleteCandidates = @()
$keepCandidates = @()
$considerCandidates = @()

foreach ($book in $allBookDetails) {
    $score = 0
    if ($book.newRating -ge 80) { $score += 3 }
    elseif ($book.newRating -ge 60) { $score += 1 }
    else { $score -= 2 }
    
    if ($book.newRatingCount -ge 100) { $score += 2 }
    elseif ($book.newRatingCount -ge 10) { $score += 1 }
    
    if ($book.publishTime -match "202[4-6]") { $score += 2 }
    elseif ($book.publishTime -match "202[0-3]") { $score += 1 }
    
    if ($book.title -match "入门|实战.*例|图解|轻松上手|一本通") { $score -= 1 }
    
    if ($score -ge 4) {
        $keepCandidates += $book
    } elseif ($score -le 0) {
        $deleteCandidates += $book
    } else {
        $considerCandidates += $book
    }
}

$htmlTemplate = @"
<!DOCTYPE html>
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
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }
        .stat-card { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px; padding: 20px; text-align: center; }
        .stat-card .number { font-size: 36px; font-weight: bold; color: #667eea; }
        .stat-card .label { margin-top: 5px; color: #666; }
        .section { padding: 30px; border-top: 1px solid #eee; }
        .section h2 { color: #333; margin-bottom: 20px; font-size: 22px; }
        .book-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .book-card { background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; }
        .book-card.delete { border-left-color: #dc3545; }
        .book-card.consider { border-left-color: #ffc107; }
        .book-card.keep { border-left-color: #28a745; }
        .book-title { font-weight: bold; color: #333; margin-bottom: 5px; }
        .book-info { color: #666; font-size: 14px; }
        .book-meta { display: flex; gap: 15px; margin-top: 8px; font-size: 12px; }
        .category-list { max-height: 400px; overflow-y: auto; }
        .category-item { display: flex; justify-content: space-between; padding: 8px 15px; border-bottom: 1px solid #eee; }
        .category-item:nth-child(odd) { background: #f8f9fa; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 微信读书书架分析报告</h1>
            <p>生成时间: GENERATE_TIME | 共分析 TOTAL_COUNT 本书</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div class="number">TOTAL_COUNT</div><div class="label">总书籍</div></div>
            <div class="stat-card"><div class="number">NEVER_READ</div><div class="label">从未阅读</div></div>
            <div class="stat-card"><div class="number">FINISHED</div><div class="label">已读完</div></div>
            <div class="stat-card"><div class="number">HIGH_SCORE</div><div class="label">高分书(≥80)</div></div>
            <div class="stat-card"><div class="number">RECENT_BOOKS</div><div class="label">2024+新书</div></div>
            <div class="stat-card"><div class="number">AI_BOOKS</div><div class="label">AI主题书</div></div>
        </div>
        <div class="section">
            <h2>📊 分类分布 (前 20)</h2>
            <div class="category-list">CATEGORY_LIST</div>
        </div>
        <div class="section">
            <h2>❌ 建议删除 (DELETE_COUNT 本)</h2>
            <div class="book-list">DELETE_LIST</div>
        </div>
        <div class="section">
            <h2>⚠️ 建议考虑 (CONSIDER_COUNT 本)</h2>
            <div class="book-list">CONSIDER_LIST</div>
        </div>
        <div class="section">
            <h2>✅ 建议保留 (KEEP_COUNT 本)</h2>
            <div class="book-list">KEEP_LIST</div>
        </div>
        <div class="section">
            <h2>💡 整理建议</h2>
            <ul style="padding-left: 20px; line-height: 2;">
                <li><strong>清理优先</strong>: 删除 DELETE_COUNT 本低分/低价值书籍</li>
                <li><strong>阅读优先</strong>: 从 KEEP_COUNT 本高分书中选择阅读</li>
                <li><strong>AI书籍去重</strong>: 书架中有 AI_BOOKS 本AI主题书，建议保留经典</li>
                <li><strong>公众号管理</strong>: 建议单独管理公众号内容</li>
            </ul>
        </div>
        <div class="footer">
            <p>微信读书书架分析报告 · 由 weread-skills 生成</p>
        </div>
    </div>
</body>
</html>
"@

$categoryHtml = ""
$categoryStats | Select-Object -First 20 | ForEach-Object {
    $categoryHtml += "<div class='category-item'><span>$($_.Name)</span><span style='color: #667eea; font-weight: bold;'>$($_.Count) 本</span></div>"
}

$deleteHtml = ""
$deleteCandidates | Select-Object -First 50 | ForEach-Object {
    $deleteHtml += "<div class='book-card delete'><div class='book-title'>$($_.title)</div><div class='book-info'>作者: $($_.author)</div><div class='book-meta'><span>评分: $($_.newRating)</span><span>评论: $($_.newRatingCount)</span><span>出版: $($_.publishTime)</span></div></div>"
}

$considerHtml = ""
$considerCandidates | Select-Object -First 30 | ForEach-Object {
    $considerHtml += "<div class='book-card consider'><div class='book-title'>$($_.title)</div><div class='book-info'>作者: $($_.author)</div><div class='book-meta'><span>评分: $($_.newRating)</span><span>评论: $($_.newRatingCount)</span><span>出版: $($_.publishTime)</span></div></div>"
}

$keepHtml = ""
$keepCandidates | Select-Object -First 30 | ForEach-Object {
    $keepHtml += "<div class='book-card keep'><div class='book-title'>$($_.title)</div><div class='book-info'>作者: $($_.author)</div><div class='book-meta'><span>评分: $($_.newRating)</span><span>评论: $($_.newRatingCount)</span><span>出版: $($_.publishTime)</span></div></div>"
}

$html = $htmlTemplate `
    -replace "GENERATE_TIME", (Get-Date -Format "yyyy-MM-dd HH:mm:ss") `
    -replace "TOTAL_COUNT", $allBookDetails.Count `
    -replace "NEVER_READ", $neverRead.Count `
    -replace "FINISHED", $finished.Count `
    -replace "HIGH_SCORE", $highScore.Count `
    -replace "RECENT_BOOKS", $recentBooks.Count `
    -replace "AI_BOOKS", $aiBooks.Count `
    -replace "CATEGORY_LIST", $categoryHtml `
    -replace "DELETE_COUNT", $deleteCandidates.Count `
    -replace "DELETE_LIST", $deleteHtml `
    -replace "CONSIDER_COUNT", $considerCandidates.Count `
    -replace "CONSIDER_LIST", $considerHtml `
    -replace "KEEP_COUNT", $keepCandidates.Count `
    -replace "KEEP_LIST", $keepHtml

$html | Out-File "$outputDir/index.html" -Encoding utf8
Write-Host "HTML 报告已保存到 $outputDir/index.html"
