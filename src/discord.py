"""Discord Webhook通知モジュール"""

from typing import Dict, List, Optional
import json
import requests

MAX_DISCORD_MESSAGE_LENGTH = 2000


def build_messages(items: List[Dict[str, str]], title: Optional[str] = None) -> List[str]:
    """アイテム一覧から2000文字以内に収まるDiscordメッセージのリストを作成する"""
    if not items:
        return []

    header = f"【 {title} の新着情報 】\n" if title else ""

    formatted_items = []
    for i, item in enumerate(items, 1):
        item_text = (
            f"**{i}. [{item['title']}]({item['url']})**\n"
            f"💴 {item['price']}｜📍 {item['location']}\n"
        )
        formatted_items.append(item_text)

    messages: List[str] = []
    current_content = header
    delimiter = "---\n"

    for item_text in formatted_items:
        addition = (delimiter if current_content and current_content != header else "") + item_text
        # Discordの文字数上限2000文字を超えないよう分割
        if len(current_content) + len(addition) > (MAX_DISCORD_MESSAGE_LENGTH - 20):
            if current_content.strip():
                messages.append(current_content.strip())
            current_content = (header if header else "") + item_text
        else:
            current_content += addition

    if current_content.strip():
        messages.append(current_content.strip())

    return messages


def send_to_discord(
    webhook_url: Optional[str],
    items: List[Dict[str, str]],
    title: Optional[str] = None,
    location_name: Optional[str] = None,
) -> bool:
    """Discord Webhookにアイテム一覧を送信する"""
    name_for_log = location_name or title or "Discord"
    tag = f"[{name_for_log}]"

    if not webhook_url:
        print(f"{tag} Webhook URLが設定されていません。送信をスキップします。")
        return False

    if not items:
        print(f"{tag} 送信するアイテムがありませんでした。")
        return True

    messages = build_messages(items, title=title or location_name)
    all_success = True

    for i, message_text in enumerate(messages):
        payload = {"content": message_text}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            print(f"{tag} Discordへの投稿に成功しました。({i + 1}/{len(messages)})")
        except requests.exceptions.RequestException as e:
            print(f"{tag} Discordへの投稿に失敗しました。({i + 1}/{len(messages)}) Error: {e}")
            all_success = False

    return all_success
