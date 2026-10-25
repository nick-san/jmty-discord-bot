# jmty-discord-bot

ジモティー（jmty.jp）から指定の条件で新着商品・出品情報をスクレイピングし、Discord の Webhook 経由で定期通知する Bot です。  
GitHub Actions 上で定期実行（Cron）されるように設計されています。

---

## 📌 主な機能

- **新着商品の自動取得 & 通知**: ジモティーの指定カテゴリ・地域から最新出品を取得し、Discord へ通知
- **Discord 2,000文字制限対応**: 件数が多い場合でもメッセージが途切れないよう、2,000文字以内で自動分割して送信
- **YAML による簡単な設定管理**: 検索キーワードや監視対象地域・URLをコードを触らず YAML で編集可能
- **手元でのテスト対応 (`--dry-run`)**: Discord に送信せず、コンソール上で取得結果を確認可能
- **高速な GitHub Actions ワークフロー**: `uv` を採用し、パッケージのセットアップを高速化

---

## 📂 ディレクトリ構成

```text
jmty-discord-bot/
├── .github/
│   └── workflows/
│       └── discord-schedule.yml   # GitHub Actions 定期実行ワークフロー
├── config/
│   ├── car_parts.yaml             # 自動車パーツ監視の設定（函館・北斗・上磯・亀田）
│   └── cars_hokkaido.yaml         # 北海道の自動車監視設定（15万以下・MT車など）
├── src/
│   ├── scraper.py                 # ジモティーのスクレイピング・パース処理
│   ├── discord.py                 # Discord Webhook 送信・メッセージ分割
│   └── config.py                  # 設定 YAML ファイルの読み込み
├── tests/
│   ├── test_scraper.py            # パース処理の単体テスト
│   ├── test_discord.py            # メッセージ生成・送信処理の単体テスト
│   └── test_config.py             # 設定ファイル読み込みの単体テスト
├── jmty-car_parts.py              # 車パーツ監視エントリーポイント
├── jmty-cars_hokkaido.py          # 北海道自動車監視エントリーポイント
├── requirements.txt               # 依存パッケージ一覧
├── .gitignore
└── README.md
```

---

## 🚀 ローカルでのセットアップと実行

### 1. 仮想環境の準備とインストール

```bash
# 仮想環境を作成して有効化
python3 -m venv .venv
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. 動作確認（Dry-Run: Discord送信なし）

`--dry-run` オプションを付けることで、Discord に送信せず取得結果（タイトル、価格、URLなど）をコンソール上で確認できます。

```bash
# 自動車監視のテスト
python jmty-cars_hokkaido.py --dry-run

# 車パーツ監視のテスト
python jmty-car_parts.py --dry-run
```

### 3. 実際にDiscordへ送信テスト

環境変数に Webhook URL を指定して実行します。

```bash
# 自動車監視
DISCORD_WEBHOOK_URL_1="https://discord.com/api/webhooks/xxxx/yyyy" python jmty-cars_hokkaido.py

# 車パーツ監視（例: 函館）
DISCORD_WEBHOOK_URL_HAKODATE="https://discord.com/api/webhooks/xxxx/yyyy" python jmty-car_parts.py
```

### 4. 単体テストの実行

```bash
python -m unittest discover tests
```

---

## ⚙️ 設定のカスタマイズ (`config/*.yaml`)

### 1. 自動車の検索条件を変更したい場合
[`config/cars_hokkaido.yaml`](config/cars_hokkaido.yaml) を編集します：

```yaml
title: "☆ジモティー 新着商品情報のお届け☆"
webhook_env: DISCORD_WEBHOOK_URL_1
limit: 20

# 監視対象の検索結果URL
urls:
  - "https://jmty.jp/hokkaido/car?..."

# 絞り込みキーワード（タイトルまたは本文に含まれるもの）
keywords:
  - MT
  - mt
  - マニュアル
```

### 2. 車パーツの対象地域を追加・変更したい場合
[`config/car_parts.yaml`](config/car_parts.yaml) を編集します：

```yaml
targets:
  - name: 函館
    url: https://jmty.jp/hokkaido/sale-auto/g-all/a-2-hakodate
    webhook_env: DISCORD_WEBHOOK_URL_HAKODATE
    limit: 15
```

---

## 🤖 GitHub Actions の設定

GitHub リポジトリの **Settings > Secrets and variables > Actions** にて、以下の Repository Secrets を登録してください。

| Secret 名 | 用途 |
|---|---|
| `DISCORD_WEBHOOK_URL_HAKODATE` | 車パーツ（函館）の Webhook URL |
| `DISCORD_WEBHOOK_URL_HOKUTO` | 車パーツ（北斗）の Webhook URL |
| `DISCORD_WEBHOOK_URL_KAMIISO` | 車パーツ（上磯）の Webhook URL |
| `DISCORD_WEBHOOK_URL_KAMEDA` | 車パーツ（亀田）の Webhook URL |
| `DISCORD_WEBHOOK_URL_1` | 自動車（北海道）の Webhook URL |
