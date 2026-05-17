# src/data_processor.py
import pandas as pd
from src.config import DATA_PATH, COLUMN_NAMES


def load_tracking_data() -> pd.DataFrame:
    """MOTChallenge形式のトラッキングデータを読み込み、DataFrameとして返す関数。

    Returns:
        pd.DataFrame: 読み込まれたトラッキングデータ
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"データファイルが見つかりません: {DATA_PATH}")

    # カンマ区切りで読み込み、定義した列名を割り当てる
    df = pd.read_csv(DATA_PATH, header=None, names=COLUMN_NAMES)
    return df