import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Optional

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
