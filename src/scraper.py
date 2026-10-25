"""ジモティー(jmty.jp)のスクレイピングモジュール"""

from typing import Dict, List, Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://jmty.jp"

# GitHub Actions等のクラウド環境で403 Forbiddenを回避するためのブラウザ偽装ヘッダー
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def fetch_html(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    session: Optional[requests.Session] = None,
    timeout: int = 15,
) -> str:
    """指定されたURLからHTMLを取得する"""
    client = session or requests
    req_headers = headers if headers is not None else DEFAULT_HEADERS

    response = client.get(url, headers=req_headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_items(
    html: str,
    keywords: Optional[List[str]] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, str]]:
    """HTMLから記事一覧を抽出し、必要に応じてキーワード絞り込みと件数制限を行う"""
    soup = BeautifulSoup(html, "html.parser")
    article_elements = soup.find_all("li", class_="p-articles-list-item")
    result: List[Dict[str, str]] = []

    for item in article_elements:
        title_tag = item.find("div", class_="p-item-title")
        title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else "（タイトルなし）"

        raw_url = title_tag.a.get("href", "") if title_tag and title_tag.a else ""
        item_url = urljoin(BASE_URL, raw_url) if raw_url else ""

        price_tag = item.find("div", class_="p-item-most-important")
        price = price_tag.get_text(strip=True) if price_tag else ""

        location_tag = item.find("div", class_="p-item-supplementary-info")
        locations = [a.get_text(strip=True) for a in location_tag.find_all("a")] if location_tag else []
        location = " / ".join(locations)

        fav_tag = item.find("span", class_="js_fav_user_count")
        fav = fav_tag.get_text(strip=True) if fav_tag else "0"

        detail_tag = item.find("div", class_="p-item-detail")
        content = detail_tag.get_text(strip=True) if detail_tag else ""

        inquiry_url = f"{item_url}#inquiry_form" if item_url else ""

        # キーワードフィルタ（指定がある場合のみ）
        if keywords:
            if not any(kw in title or kw in content for kw in keywords):
                continue

        result.append({
            "title": title,
            "url": item_url,
            "price": price,
            "fav": fav,
            "location": location,
            "content": content,
            "inquiry_url": inquiry_url,
        })

        if limit is not None and len(result) >= limit:
            break

    return result


def fetch_latest_items(
    url: str,
    keywords: Optional[List[str]] = None,
    limit: Optional[int] = None,
    headers: Optional[Dict[str, str]] = None,
    session: Optional[requests.Session] = None,
    timeout: int = 15,
) -> List[Dict[str, str]]:
    """指定URLから最新の投稿情報を取得・抽出する"""
    html = fetch_html(url, headers=headers, session=session, timeout=timeout)
    return parse_items(html, keywords=keywords, limit=limit)
