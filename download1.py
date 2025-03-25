import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scroll_and_load(driver, pause_time=2, max_scrolls=30):
    """
    模擬滾動到底部以觸發動態載入，
    若連續滾動後頁面高度不再變化則停止。
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0
    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1

def scrape_articles_from_url(url):
    """
    開啟指定 URL，用 Selenium 模擬滾動載入所有文章，
    再用 BeautifulSoup 分析頁面 HTML，取得所有文章資訊。
    """
    # 設定 headless 模式
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 建立 WebDriver（注意設定 chromedriver 路徑）
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # 模擬滾動
    scroll_and_load(driver, pause_time=2, max_scrolls=30)
    
    # 取得動態載入後的頁面原始碼
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, "html.parser")
    # 優先嘗試使用 <article> 標籤
    articles = soup.find_all("article")
    if not articles:
        articles = soup.find_all("div", class_="post")
    
    results = []
    for art in articles:
        # 嘗試取得標題，標題通常在 h1 或 h2 內包含 <a> 連結
        header = art.find(["h1", "h2"])
        if header:
            a_tag = header.find("a")
            if a_tag and a_tag.get("href"):
                title = a_tag.get_text(strip=True)
                link = a_tag.get("href")
            else:
                title = header.get_text(strip=True)
                link = url
        else:
            title = "無標題"
            link = url
        
        # 嘗試取得摘要，可能在 entry-content 或 post-content 中
        summary_tag = art.find("div", class_="entry-content")
        if not summary_tag:
            summary_tag = art.find("div", class_="post-content")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""
        
        results.append({
            "來源": url,
            "標題": title,
            "連結": link,
            "摘要": summary
        })
    return results

def main():
    sites = [
        "https://aubinchang1.wordpress.com/"
    ]
    
    all_articles = []
    for site in sites:
        print(f"開始爬取：{site}")
        articles = scrape_articles_from_url(site)
        all_articles.extend(articles)
    
    output_file = "all_posts1.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)
    
    print(f"爬取完成，共取得 {len(all_articles)} 筆資料，結果存於 {output_file}")

if __name__ == '__main__':
    main()
