# main.py
from src.data_processor import load_tracking_data


def main():
    print("--- ステップ1: データの読み込みテスト ---")
    try:
        # データの読み込み
        df = load_tracking_data()

        # 正しく読み込めているか先頭5行を表示して確認
        print("データの一部の読み込みに成功しました：")
        print(df.head())
        print(f"総データ行数: {len(df)}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()