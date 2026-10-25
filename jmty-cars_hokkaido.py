"""ジモティー 北海道 自動車新着通知スクリプト"""

import os
import sys
from src.config import load_yaml
from src.scraper import fetch_latest_items
from src.discord import send_to_discord


def extract_latest_items(url, keywords=None, limit=20):
    """指定されたURLから最新の投稿情報を抽出する（後方互換用エイリアス）"""
    return fetch_latest_items(url, keywords=keywords, limit=limit)


def main():
    dry_run = "--dry-run" in sys.argv
    config = load_yaml("cars_hokkaido.yaml")
    webhook_env = config.get("webhook_env", "DISCORD_WEBHOOK_URL_1")
    webhook_url = os.getenv(webhook_env)
    title = config.get("title", "☆ジモティー 新着商品情報のお届け☆")
    urls = config.get("urls", [])
    keywords = config.get("keywords", [])
    limit = config.get("limit", 20)

    if not dry_run and not webhook_url:
        print(f"Webhook URLが設定されていません。環境変数 '{webhook_env}' を確認してください。")
        print("※画面で取得結果だけ確認したい場合は '--dry-run' を付けて実行してください。")
        return

    for url in urls:
        print(f"処理を開始します... ({url})")
        try:
            items = extract_latest_items(url, keywords=keywords, limit=limit)

            if dry_run:
                print(f"[DRY-RUN] 取得結果: {len(items)}件")
                for i, item in enumerate(items, 1):
                    print(f"  {i}. {item['title']} | 💴 {item['price']} | 📍 {item['location']}")
                    print(f"     URL: {item['url']}")
                continue

            send_to_discord(
                webhook_url=webhook_url,
                items=items,
                title=title,
            )
        except Exception as e:
            print(f"処理中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
