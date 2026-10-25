"""設定ファイル読み込みモジュール"""

import os
from pathlib import Path
from typing import Any, Dict
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


def load_env_file(file_path: str | Path | None = None) -> None:
    """プロジェクト直下の .env ファイルが存在すれば環境変数に読み込む"""
    env_path = Path(file_path) if file_path else PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            # 既に環境変数が設定されている場合はそれを優先
            if key not in os.environ:
                os.environ[key] = val


# モジュール読み込み時に .env があれば自動で読み込む
load_env_file()


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
