import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
url = "https://jmty.jp/hokkaido/sale-auto/g-all/a-2-hakodate"

def extract_latest_items(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="p-articles-list-item")[:15]
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
    for i, item in enumerate(items, 1):
        msg = (
            f"**{i}. [{item['title']}]({item['url']})**\n"
            f"💴 {item['price']}｜📍 {item['location']}\n\n"
        )
        payload = {"content": msg}
        requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

if __name__ == "__main__":
    items = extract_latest_items(url)
    send_to_discord(items)
