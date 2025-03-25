import os
import json
import requests
from bs4 import BeautifulSoup
import html2text
import time
import re

def sanitize_filename(name):
    # 將標題中的特殊字元去除或替換
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip()
    return name

def get_article_markdown(link):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # 嘗試多個選擇器提取文章內容
        selectors = [
            "article",
            "div.entry-content",
            "div.post-content",
            "div.single-post",
            "div.content"
        ]
        content = None
        for sel in selectors:
            content = soup.select_one(sel)
            if content and content.get_text(strip=True):
                break

        if content:
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.body_width = 0
            markdown = h.handle(str(content))
        else:
            markdown = "無法提取文章內容。請檢查頁面 HTML 結構。"
    except Exception as e:
        markdown = f"錯誤：{e}"
    return markdown

# 讀取之前提取的文章資料，假設檔名為 extracted_posts.json
with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# 建立存放 Markdown 檔案的資料夾
md_folder = "markdown"
if not os.path.exists(md_folder):
    os.makedirs(md_folder)

summary_list = []

for idx, post in enumerate(posts, start=1):
    title = post.get("標題", f"文章_{idx}")
    link = post.get("連結")
    date = post.get("date", "未知日期")
    print(f"處理文章：{title} - {link}")
    markdown = get_article_markdown(link)
    
    # 產生檔名，使用標題並加上索引以避免重複
    file_name = f"{idx:02d}_{sanitize_filename(title)}.md"
    file_path = os.path.join(md_folder, file_name)
    
    # 儲存 Markdown 檔案
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    summary_list.append({
        "標題": title,
        "連結": link,
        "date": date,
        "markdown_file": file_path
    })
    
    time.sleep(1)  # 延遲以避免訪問過快

# 將摘要結果寫入 summary.json
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_list, f, ensure_ascii=False, indent=4)

print("完成生成 summary.json，Markdown 檔案已存放於 'markdown' 資料夾中！")
