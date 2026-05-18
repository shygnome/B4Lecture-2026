import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Optional
import cv2
import numpy as np

def plot_trajectories(
    df: pd.DataFrame, 
    target_ids: List[int], 
    save_path: Optional[Path] = None
) -> None:
    """指定された track_id の中心座標軌跡を2Dプロットとして描画・保存する。

    Args:
        df (pd.DataFrame): 処理済みのトラッキングデータ（'id', 'cx', 'cy', 'frame' 列を含む想定）
        target_ids (List[int]): 描画対象の track_id リスト
        save_path (Optional[Path], optional): 画像の保存先パス。未指定時は plt.show() で表示する。
    """
    plt.figure(figsize=(12, 8))

    for track_id in target_ids:
        # 対象IDのデータを抽出（時系列順の担保のため frame でソート）
        target_data = df[df['id'] == track_id].sort_values('frame')
        
        if target_data.empty:
            continue

        plt.plot(
            target_data['cx'],
            target_data['cy'],
            marker='o',
            markersize=2,
            linewidth=1.5,
            label=f'ID: {track_id}',
            alpha=0.8
        )

    plt.title('Player Trajectories')
    plt.xlabel('X (cx)')
    plt.ylabel('Y (cy)')
    
    # 画像座標系に合わせるためY軸を反転
    plt.gca().invert_yaxis()
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    if save_path:
        # 保存先ディレクトリが存在しない場合は作成
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()

    plt.close()


def plot_speed_subplots(
    df: pd.DataFrame, 
    target_ids: List[int], 
    save_path: Optional[Path] = None
) -> None:
    """各指定IDの速度の時系列推移を、縦横グリッドで比較描画する。
    
    Args:
        df (pd.DataFrame): 速度算出済みのトラッキングデータ
        target_ids (List[int]): 描画対象の track_id リスト（最大6つ）
        save_path (Optional[Path], optional): 画像の保存先パス
    """
    # 2行3列のグリッドを作成
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8), sharey=True)
    axes = axes.flatten() 

    for i, track_id in enumerate(target_ids):
        if i >= len(axes):
            print(f"WARNING: 描画枠の上限(6)を超えたため、ID {track_id} 以降はスキップされます。")
            break
            
        ax = axes[i]
        target_data = df[df['id'] == track_id].sort_values('frame')
        
        if target_data.empty:
            continue

        # フレーム(X軸)に対する速度(Y軸)をプロット
        ax.plot(
            target_data['frame'], 
            target_data['speed'], 
            marker='.', 
            markersize=4, 
            linewidth=1.0, 
            color='tab:red'
        )
        ax.set_title(f'ID: {track_id} Speed')
        ax.set_xlabel('Frame')
        ax.set_ylabel('Speed (pixels/frame)')
        ax.grid(True, linestyle=':', alpha=0.6)

    # 指定されたIDが6つ未満の場合、余った空のグラフ枠を非表示にする
    for j in range(len(target_ids), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()

    plt.close()


def create_trajectory_video(
    df: pd.DataFrame,
    target_ids: List[int],
    input_video_path: Path,
    output_video_path: Path
) -> None:
    """入力映像を背景として、指定IDの軌跡を描画したアニメーション動画を生成する。
    
    Args:
        df (pd.DataFrame): 処理済みのトラッキングデータ
        target_ids (List[int]): 描画対象の track_id リスト
        input_video_path (Path): 元映像のパス
        output_video_path (Path): 生成する動画の保存先パス
    """
    cap = cv2.VideoCapture(str(input_video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"映像を開けませんでした: {input_video_path}")

    # 動画のプロパティを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 書き出し用の設定
    fourcc = cv2.VideoWriter_fourcc(*'vp80')
    out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))

    # 描画用の色定義 (BGR形式)
    colors = {
        6: (255, 100, 100),   # 青系
        7: (100, 200, 255),   # オレンジ系
        13: (100, 255, 100),  # 緑系
        27: (100, 100, 255),  # 赤系
        44: (255, 100, 255),  # 紫系
        51: (150, 150, 150)   # グレー系
    }

    # 各IDの過去の座標を保持する辞書
    history = {tid: [] for tid in target_ids}
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 背景映像を暗くする (元の明るさを40%にする)
        dark_frame = cv2.addWeighted(frame, 0.4, np.zeros_like(frame), 0, 0)

        # 現在のフレームのデータを取得
        current_data = df[df['frame'] == frame_idx]

        for tid in target_ids:
            person_data = current_data[current_data['id'] == tid]
            
            # そのフレームに該当IDが存在すれば履歴に追加
            if not person_data.empty:
                cx = int(person_data['cx'].values[0])
                cy = int(person_data['cy'].values[0])
                history[tid].append((cx, cy))

            pts = history[tid]
            color = colors.get(tid, (255, 255, 255))

            # 軌跡（線）を描画
            if len(pts) > 1:
                for i in range(1, len(pts)):
                    cv2.line(dark_frame, pts[i-1], pts[i], color, thickness=2)

            # 現在位置に点とIDを描画
            if len(pts) > 0:
                cv2.circle(dark_frame, pts[-1], radius=5, color=color, thickness=-1)
                cv2.putText(
                    dark_frame, f"ID:{tid}", (pts[-1][0] + 10, pts[-1][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                )

        # 編集したフレームを動画に書き込み
        out.write(dark_frame)
        
        if frame_idx % 100 == 0:
            print(f"INFO: {frame_idx}/{total_frames} フレーム処理完了...")
            
        frame_idx += 1

    cap.release()
    out.release()
    print("SUCCESS: アニメーション生成が完了しました！")