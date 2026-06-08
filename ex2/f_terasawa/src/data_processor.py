import pandas as pd
from src.config import DATA_PATH, COLUMN_NAMES


def load_tracking_data() -> pd.DataFrame:
    """MOTChallenge形式のトラッキングデータを読み込む。

    Returns:
        pd.DataFrame: 読込済みのトラッキングデータ
    
    Raises:
        FileNotFoundError: 指定パスにデータファイルが存在しない場合
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"データファイルが見つかりません: {DATA_PATH}")

    return pd.read_csv(DATA_PATH, header=None, names=COLUMN_NAMES)


def calculate_centers(df: pd.DataFrame) -> pd.DataFrame:
    """バウンディングボックス情報から中心座標(cx, cy)を算出する。
    
    Args:
        df (pd.DataFrame): トラッキングデータ
        
    Returns:
        pd.DataFrame: 'cx', 'cy' 列が追加されたDataFrameオブジェクト
    """

    processed_df = df.copy()
    
    # バウンディングボックスの座標とサイズから中心座標を計算
    processed_df['cx'] = processed_df['x'] + processed_df['w'] / 2
    processed_df['cy'] = processed_df['y'] + processed_df['h'] / 2
    
    return processed_df


def calculate_kinematics(df: pd.DataFrame) -> pd.DataFrame:
    """中心座標から各track_idの速度と加速度を算出する。
    
    Args:
        df (pd.DataFrame): 中心座標(cx, cy)追加済みのトラッキングデータ
        
    Returns:
        pd.DataFrame: 速度・加速度の列が追加されたDataFrameオブジェクト
    """
    processed_df = df.copy()
    
    # 時系列の計算を正しく行うため、idとframeでソート
    processed_df = processed_df.sort_values(['id', 'frame'])
    
    # 同一ID内でのフレーム間の差分(t - t-1)を計算
    processed_df['vx'] = processed_df.groupby('id')['cx'].diff()
    processed_df['vy'] = processed_df.groupby('id')['cy'].diff()
    
    # 速度の計算
    processed_df['speed'] = (processed_df['vx']**2 + processed_df['vy']**2)**0.5
    
    # 加速度の計算
    processed_df['acceleration'] = processed_df.groupby('id')['speed'].diff()
    
    # ソート順を元のフレーム順に戻す
    processed_df = processed_df.sort_values(['frame', 'id']).reset_index(drop=True)
    
    return processed_df