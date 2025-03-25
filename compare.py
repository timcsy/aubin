import json

# 讀取 JSON 檔案
with open('all_posts0.json', encoding='utf-8') as f:
    posts1 = json.load(f)

with open('all_posts1.json', encoding='utf-8') as f:
    posts2 = json.load(f)

# 將兩個檔案的文章依標題建立字典（假設每個標題在各檔案中唯一）
dict1 = {post['標題']: post for post in posts1}
dict2 = {post['標題']: post for post in posts2}

# 取得兩個檔案中相同的標題
common_titles = set(dict1.keys()) & set(dict2.keys())

print("根據標題找到的相同文章：\n")
for title in common_titles:
    post1 = dict1[title]
    post2 = dict2[title]
    print("標題:", title)
    print("來源1:", post1.get("來源"))
    print("連結1:", post1.get("連結"))
    print("摘要1:", post1.get("摘要")[:100], "...\n")
    print("來源2:", post2.get("來源"))
    print("連結2:", post2.get("連結"))
    print("摘要2:", post2.get("摘要")[:100], "...\n")
    print("-" * 50)
