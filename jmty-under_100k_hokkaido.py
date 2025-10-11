import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL_1")

# 北海道 自動車 10万以下
url0 = "https://jmty.jp/hokkaido/car?model_year%5Bmin%5D=&model_year%5Bmax%5D=&mileage%5Bmin%5D=&mileage%5Bmax%5D=&min=&max=100000&commit=%E6%A4%9C%E7%B4%A2"

urls = [url0]

keywords = ["MT", "mt", "マニュアル"]

def extract_latest_items(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="p-articles-list-item")[:20]
    result = []

    for item in items:
        title_tag = item.find("div", class_="p-item-title")
        title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else "（タイトルなし）"
        url = title_tag.a["href"] if title_tag and title_tag.a else ""
        price_tag = item.find("div", class_="p-item-most-important")
        price = price_tag.get_text(strip=True) if price_tag else ""
        location_tag = item.find("div", class_="p-item-supplementary-info")
        locations = [a.get_text(strip=True) for a in location_tag.find_all("a")] if location_tag else []
        location = " / ".join(locations)
        fav_tag = item.find("span", class_="js_fav_user_count")
        fav = fav_tag.get_text(strip=True) if fav_tag else "0"
        detail_tag = item.find("div", class_="p-item-detail")
        content = detail_tag.get_text(strip=True) if detail_tag else ""
        inquiry_url = url + "#inquiry_form"

        # キーワードのいずれかがtitleまたはcontentに含まれているか
        if any(kw in title or kw in content for kw in keywords):
            result.append({
                "title": title,
                "url": url,
                "price": price,
                "fav": fav,
                "location": location,
                "content": content,
                "inquiry_url": inquiry_url
            })

    return result

def send_to_discord(items):
    messages = []
    messages.append("☆ジモティー 新着商品情報のお届け☆\n")
    for i, item in enumerate(items, 1):
        msg = (
            f"**{i}. [{item['title']}]({item['url']})**\n"
            f"💴 {item['price']}｜📍 {item['location']}\n\n"
        )
        messages.append(msg)

    full_message ="\n---\n".join(messages)
    payload = {"content": full_message}
    requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

if __name__ == "__main__":
    for url in urls:
        items = extract_latest_items(url)
        send_to_discord(items)
