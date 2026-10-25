import unittest
from src.discord import build_messages, send_to_discord


class TestDiscord(unittest.TestCase):
    def test_build_messages_empty(self):
        self.assertEqual(build_messages([]), [])

    def test_build_messages_with_title(self):
        items = [
            {"title": "商品1", "url": "https://example.com/1", "price": "1,000円", "location": "函館"},
            {"title": "商品2", "url": "https://example.com/2", "price": "2,000円", "location": "北斗"},
        ]
        msgs = build_messages(items, title="函館")
        self.assertEqual(len(msgs), 1)
        self.assertIn("【 函館 の新着情報 】", msgs[0])
        self.assertIn("1. [商品1](https://example.com/1)", msgs[0])
        self.assertIn("2. [商品2](https://example.com/2)", msgs[0])

    def test_build_messages_chunking(self):
        # 2000文字を超えるような大量のアイテム
        items = [
            {"title": f"長いタイトルでテストする商品_{i}" * 5, "url": f"https://example.com/item/{i}", "price": "10,000円", "location": "北海道各地"}
            for i in range(30)
        ]
        msgs = build_messages(items, title="大量テスト")
        self.assertGreater(len(msgs), 1)
        for msg in msgs:
            self.assertLessEqual(len(msg), 2000)

    def test_send_to_discord_no_webhook(self):
        result = send_to_discord(None, [{"title": "test", "url": "", "price": "", "location": ""}])
        self.assertFalse(result)

    def test_send_to_discord_empty_items(self):
        result = send_to_discord("https://discord.com/api/webhooks/dummy", [])
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
