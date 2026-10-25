"""設定ファイル読み込みモジュール"""

from pathlib import Path
from typing import Any, Dict
import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def load_yaml(file_path: str | Path) -> Dict[str, Any]:
    """YAML設定ファイルを読み込む"""
    path = Path(file_path)
    if not path.is_absolute():
        path = CONFIG_DIR / path

    if not path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data or {}
