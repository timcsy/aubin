import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def load_all_posts(url):
    """
    使用 Selenium 進入指定網址，重複點擊「Older posts」按鈕，
    直到所有文章皆載入，回傳最終頁面的 HTML 原始碼。
    """
    # 設定 headless 模式與視窗大小
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)  # 初步等待網頁載入

    while True:
        try:
            # 使用新的 XPath 針對 id="infinite-handle" 下的 button 進行定位
            older_posts_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='infinite-handle']//button[contains(text(), 'Older posts')]"))
            )
            # 滾動到按鈕位置
            driver.execute_script("arguments[0].scrollIntoView(true);", older_posts_button)
            time.sleep(1)
            # 使用 JavaScript 點擊按鈕
            driver.execute_script("arguments[0].click();", older_posts_button)
            # 等待新文章載入，根據實際網速調整等待時間
            time.sleep(2)
        except Exception as e:
            print("找不到或已無『Older posts』按鈕，停止點擊。")
            break

    html = driver.page_source
    driver.quit()
    return html

def scrape_articles(html, source_url):
    """
    使用 BeautifulSoup 分析 HTML，取得所有文章的標題、連結與摘要。
    """
    soup = BeautifulSoup(html, "html.parser")
    # 優先使用 <article> 標籤，若找不到則嘗試 div.post
    articles = soup.find_all("article")
    if not articles:
        articles = soup.find_all("div", class_="post")
    
    results = []
    for art in articles:
        header = art.find(["h1", "h2"])
        if header:
            a_tag = header.find("a")
            if a_tag and a_tag.get("href"):
                title = a_tag.get_text(strip=True)
                link = a_tag.get("href")
            else:
                title = header.get_text(strip=True)
                link = source_url
        else:
            title = "無標題"
            link = source_url
        
        # 嘗試抓取摘要，常見於 entry-content 或 post-content 區塊
        summary_tag = art.find("div", class_="entry-content")
        if not summary_tag:
            summary_tag = art.find("div", class_="post-content")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        results.append({
            "來源": source_url,
            "標題": title,
            "連結": link,
            "摘要": summary
        })
    return results

def main():
    target_url = "https://aubinchang.wordpress.com/"
    print(f"開始處理：{target_url}")
    html = load_all_posts(target_url)
    articles = scrape_articles(html, target_url)
    print(f"取得 {len(articles)} 筆文章")
    
    output_file = "all_posts.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"全部文章共 {len(articles)} 筆，結果存於 {output_file}")

if __name__ == '__main__':
    main()
