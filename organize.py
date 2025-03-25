import json
import re
import datetime

# 讀取 JSON 檔案
with open('all_posts.json', encoding='utf-8') as f:
    all_posts = json.load(f)

def extract_date(post):
    """
    根據文章連結中 /YYYY/MM/DD/ 格式提取日期
    """
    link = post.get("連結", "")
    m = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', link)
    if m:
        year, month, day = m.groups()
        try:
            return datetime.date(int(year), int(month), int(day))
        except Exception:
            return None
    return None

# 為每篇文章提取日期，若無法提取則為 None
for post in all_posts:
    post['date'] = extract_date(post)

# 根據日期排序，存入變數 sorted_posts
sorted_posts = sorted(all_posts, key=lambda x: x['date'] if x['date'] is not None else datetime.date(1,1,1), reverse=False)

# 轉換 date 物件為字串（ISO 格式）
for post in sorted_posts:
    if post.get('date'):
        post['date'] = post['date'].isoformat()
    else:
        post['date'] = None

# 將排序結果寫入 JSON 檔案 sorted_posts.json
with open('sorted_posts.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_posts, f, ensure_ascii=False, indent=4)

# 同時產生 HTML 內容供閱讀
html_content = """<html>
<head>
    <meta charset="utf-8">
    <title>文章主目錄</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .post { margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #ccc; }
        .title { font-size: 20px; font-weight: bold; margin-bottom: 5px; }
        .date { color: #888; margin-bottom: 5px; }
        .source { font-size: 12px; color: #555; margin-bottom: 5px; }
        .excerpt { font-size: 14px; }
    </style>
</head>
<body>
<h1>文章主目錄</h1>
"""

for post in sorted_posts:
    date_str = post['date'] if post['date'] else "未知日期"
    title = post.get("標題", "無標題")
    link = post.get("連結", "#")
    source = post.get("來源", "")
    excerpt = post.get("摘要", "")
    html_content += f"""
    <div class="post">
        <div class="title"><a href="{link}" target="_blank">{title}</a></div>
        <div class="date">日期：{date_str}</div>
        <div class="source">來源：{source}</div>
        <div class="excerpt">{excerpt}</div>
    </div>
    """

html_content += """
</body>
</html>
"""

# 將 HTML 寫入檔案 posts_directory.html
with open('posts_directory.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("sorted_posts 已存入 sorted_posts.json，並生成 posts_directory.html 成功！")
