import unittest
from src.scraper import parse_items

SAMPLE_HTML = """
<html>
<body>
  <ul class="p-articles-list">
    <li class="p-articles-list-item">
      <div class="p-item-title">
        <a href="/hokkaido/sale-auto/g-all/a-2-hakodate/12345">スタッドレスタイヤ 4本セット</a>
      </div>
      <div class="p-item-most-important">10,000円</div>
      <div class="p-item-supplementary-info">
        <a href="#">函館市</a>
        <a href="#">五稜郭駅</a>
      </div>
      <span class="js_fav_user_count">5</span>
      <div class="p-item-detail">状態良好です。MT車にも使えます。</div>
    </li>
    <li class="p-articles-list-item">
      <div class="p-item-title">
        <a href="https://jmty.jp/hokkaido/car/99999">軽自動車 AT</a>
      </div>
      <div class="p-item-most-important">50,000円</div>
      <div class="p-item-supplementary-info">
        <a href="#">北斗市</a>
      </div>
      <span class="js_fav_user_count">2</span>
      <div class="p-item-detail">オートマ車です。</div>
    </li>
  </ul>
</body>
</html>
"""


class TestScraper(unittest.TestCase):
    def test_parse_items_basic(self):
        items = parse_items(SAMPLE_HTML)
        self.assertEqual(len(items), 2)

        item1 = items[0]
        self.assertEqual(item1["title"], "スタッドレスタイヤ 4本セット")
        self.assertEqual(item1["url"], "https://jmty.jp/hokkaido/sale-auto/g-all/a-2-hakodate/12345")
        self.assertEqual(item1["price"], "10,000円")
        self.assertEqual(item1["location"], "函館市 / 五稜郭駅")
        self.assertEqual(item1["fav"], "5")
        self.assertEqual(item1["content"], "状態良好です。MT車にも使えます。")
        self.assertEqual(item1["inquiry_url"], "https://jmty.jp/hokkaido/sale-auto/g-all/a-2-hakodate/12345#inquiry_form")

        item2 = items[1]
        self.assertEqual(item2["title"], "軽自動車 AT")
        self.assertEqual(item2["url"], "https://jmty.jp/hokkaido/car/99999")
        self.assertEqual(item2["price"], "50,000円")
        self.assertEqual(item2["location"], "北斗市")
        self.assertEqual(item2["fav"], "2")

    def test_parse_items_keywords(self):
        items = parse_items(SAMPLE_HTML, keywords=["MT", "マニュアル"])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "スタッドレスタイヤ 4本セット")

    def test_parse_items_limit(self):
        items = parse_items(SAMPLE_HTML, limit=1)
        self.assertEqual(len(items), 1)


if __name__ == "__main__":
    unittest.main()
