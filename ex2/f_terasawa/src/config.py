# src/config.py
from pathlib import Path

# パスの設定
BASE_DIR = Path(__file__).resolve().parent.parent # f_terasawaディレクトリ
DATA_PATH = BASE_DIR / "data" / "tracking_data.txt"

# MOTChallenge形式の列名定義
COLUMN_NAMES = [
    "frame",
    "id",
    "x",
    "y",
    "w",
    "h",
    "conf",
    "dummy1",
    "dummy2",
    "dummy3",
]