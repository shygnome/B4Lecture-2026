import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Pitch

def load_output_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    # calculate bounding box center
    df["cx"] = df["x"] + df["w"] / 2
    df["cy"] = df["y"] + df["h"] / 2

    return df

def plot_player_trajectories(filtered_df, target_ids):
    plt.figure(figsize=(12, 7))

    for track_id in target_ids:
        player_data = filtered_df[filtered_df['track_id'] == track_id].sort_values('frame')
        
        plt.plot(player_data['cx'], player_data['cy'], label=f'Player ID {track_id}', alpha=0.5, linewidth=2)
        
        # Plot the scatter points with alpha based on frame progression
        norm_frame = (player_data['frame'] - player_data['frame'].min()) / (player_data['frame'].max() - player_data['frame'].min() + 1)
        plt.scatter(player_data['cx'], player_data['cy'], label=f'Player ID {track_id}', 
                    alpha=norm_frame.clip(0.1, 1.0), s=15)
        
        # Mark the starting position
        if not player_data.empty:
            plt.scatter(player_data['cx'].iloc[0], player_data['cy'].iloc[0], 
                        color='black', marker='X', s=100, zorder=5)
    
    plt.scatter([], [], color='black', marker='X', s=100, label='Start Position', zorder=5)

    plt.gca().invert_yaxis()
    plt.title('Player Trajectories (First 20s)', fontsize=14, fontweight='bold')
    plt.xlabel('X Coordinate [Pixels]', fontsize=12)
    plt.ylabel('Y Coordinate [Pixels]', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='lower right')

    plt.tight_layout()
    plt.savefig('player_trajectories.png', dpi=300)

def main():
    output_data_filename = "Deep-EIoU-output.txt"
    output_data = load_output_data(output_data_filename)
    print(output_data.head())

    # 課題1：選手軌跡の可視化
    target_ids = output_data['track_id'].unique()[:5]
    filtered_df = output_data[output_data['track_id'].isin(target_ids)]
    plot_player_trajectories(filtered_df, target_ids)

    # 課題2：速度・加速度を用いた分析
    

if __name__ == "__main__":
    main()
