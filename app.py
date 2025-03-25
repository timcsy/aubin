from flask import Flask, render_template, abort
import json
import os
import markdown

app = Flask(__name__)

# 讀取 summary.json (裡面包含每篇文章的標題、連結、date 與 Markdown 檔案路徑)
with open("summary.json", "r", encoding="utf-8") as f:
    summary_list = json.load(f)

@app.route("/")
def index():
    # 文章列表頁，列出所有文章標題與日期
    return render_template("index.html", posts=summary_list)

@app.route("/post/<int:post_id>")
def post(post_id):
    # 依照索引讀取指定文章
    if post_id < 0 or post_id >= len(summary_list):
        abort(404)
    post_info = summary_list[post_id]
    md_file = post_info.get("markdown_file")
    if not md_file or not os.path.exists(md_file):
        content = "<p>找不到文章內容。</p>"
    else:
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
        # 使用 markdown 套件轉換 Markdown 內容為 HTML，附加一些擴展功能
        content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    return render_template("post.html", post=post_info, content=content)

if __name__ == "__main__":
    app.run(debug=True)
