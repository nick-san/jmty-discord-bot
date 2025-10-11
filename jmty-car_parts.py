import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

# 監視したい地域、そのURL、対応する環境変数名をセットで管理する
TARGETS = [
    {
        "name": "函館",
        "url": "https://jmty.jp/hokkaido/sale-auto/g-all/a-2-hakodate",
        "webhook_env": "DISCORD_WEBHOOK_URL_HAKODATE"
    },
    {
        "name": "北斗",
        "url": "https://jmty.jp/hokkaido/sale-auto/g-all/a-35-hokuto",
        "webhook_env": "DISCORD_WEBHOOK_URL_HOKUTO"
    },
    {
        "name": "上磯",
        "url": "https://jmty.jp/hokkaido/sale-auto/g-all/a-89208-kamiiso",
        "webhook_env": "DISCORD_WEBHOOK_URL_KAMIISO"
    },
    {
        "name": "亀田",
        "url": "https://jmty.jp/hokkaido/sale-auto/g-all/a-89209-kameda",
        "webhook_env": "DISCORD_WEBHOOK_URL_KAMEDA"
    },

]


def extract_latest_items(url):
    """指定されたURLから最新の投稿情報を抽出する"""
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="p-articles-list-item")[:15]
    result = []

    for item in items:
        title_tag = item.find("div", class_="p-item-title")
        title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else "（タイトルなし）"
        item_url = title_tag.a["href"] if title_tag and title_tag.a else ""
        if item_url and not item_url.startswith("http"):
            item_url = "https://jmty.jp" + item_url
            
        price_tag = item.find("div", class_="p-item-most-important")
        price = price_tag.get_text(strip=True) if price_tag else ""
        location_tag = item.find("div", class_="p-item-supplementary-info")
        locations = [a.get_text(strip=True) for a in location_tag.find_all("a")] if location_tag else []
        location = " / ".join(locations)
        fav_tag = item.find("span", class_="js_fav_user_count")
        fav = fav_tag.get_text(strip=True) if fav_tag else "0"
        detail_tag = item.find("div", class_="p-item-detail")
        content = detail_tag.get_text(strip=True) if detail_tag else ""
        inquiry_url = item_url + "#inquiry_form"

        result.append({
            "title": title, "url": item_url, "price": price,
            "fav": fav, "location": location, "content": content,
            "inquiry_url": inquiry_url
        })

    return result

def send_to_discord(webhook_url, items, location_name):

    if not items:
        print(f"[{location_name}] 送信するアイテムがありませんでした。")
        return

    # 地域の名前をメッセージの先頭に追加
    header = f"【 {location_name} の新着情報 】\n"
    messages = []
    for i, item in enumerate(items, 1):
        msg = (
            f"**{i}. [{item['title']}]({item['url']})**\n"
            f"💴 {item['price']}｜📍 {item['location']}\n"
        )
        messages.append(msg)

    full_message = header + "\n---\n".join(messages)
    if len(full_message) > 2000:
        full_message = full_message[:1990] + "..."

    payload = {"content": full_message}
    
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        print(f"[{location_name}] Discordへの投稿に成功しました。")
    except requests.exceptions.RequestException as e:
        print(f"[{location_name}] Discordへの投稿に失敗しました。 Error: {e}")

if __name__ == "__main__":
    # 設定リスト（TARGETS）をループ処理
    for target in TARGETS:
        location_name = target["name"]
        region_url = target["url"]
        webhook_env_name = target["webhook_env"]

        # 対応する環境変数からWebhook URLを取得
        webhook_url = os.getenv(webhook_env_name)

        # Webhook URLが設定されていない場合はスキップ
        if not webhook_url:
            print(f"[{location_name}] Webhook URLが設定されていません。環境変数 '{webhook_env_name}' を確認してください。")
            continue

        print(f"[{location_name}] 処理を開始します... ({region_url})")
        latest_items = extract_latest_items(region_url)
        send_to_discord(webhook_url, latest_items, location_name)
