"""ジモティー 車パーツ新着情報通知スクリプト"""

import os
import sys
from src.config import load_yaml
from src.scraper import fetch_latest_items
from src.discord import send_to_discord


def extract_latest_items(url, limit=15):
    """指定されたURLから最新の投稿情報を抽出する（後方互換用エイリアス）"""
    return fetch_latest_items(url, limit=limit)


def main():
    dry_run = "--dry-run" in sys.argv
    config = load_yaml("car_parts.yaml")
    targets = config.get("targets", [])

    for target in targets:
        location_name = target["name"]
        region_url = target["url"]
        webhook_env_name = target["webhook_env"]
        limit = target.get("limit", 15)

        # 対応する環境変数からWebhook URLを取得
        webhook_url = os.getenv(webhook_env_name)

        # Webhook URLが設定されていない場合はスキップ（dry-run時を除く）
        if not dry_run and not webhook_url:
            print(f"[{location_name}] Webhook URLが設定されていません。環境変数 '{webhook_env_name}' を確認してください。")
            continue

        print(f"[{location_name}] 処理を開始します... ({region_url})")
        try:
            latest_items = extract_latest_items(region_url, limit=limit)

            if dry_run:
                print(f"[{location_name}] [DRY-RUN] 取得結果: {len(latest_items)}件")
                for i, item in enumerate(latest_items, 1):
                    print(f"  {i}. {item['title']} | 💴 {item['price']} | 📍 {item['location']}")
                    print(f"     URL: {item['url']}")
                continue

            send_to_discord(webhook_url, latest_items, location_name=location_name)
        except Exception as e:
            print(f"[{location_name}] 処理中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
