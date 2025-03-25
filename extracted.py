import json

# 讀取 sorted_posts.json
with open('sorted_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# 只提取標題、連結和 date 欄位
extracted_posts = []
for post in posts:
    extracted_posts.append({
        "標題": post.get("標題"),
        "連結": post.get("連結"),
        "date": post.get("date")
    })

# 將提取結果寫入新的 JSON 檔案
with open('extracted_sorted_posts.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_posts, f, ensure_ascii=False, indent=4)

print("提取完成，結果存入 extracted_sorted_posts.json")
