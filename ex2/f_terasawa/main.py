from src.config import ANIMATION_OUTPUT_PATH, INPUT_VIDEO_PATH, TRAJECTORY_PLOT_PATH, SPEED_PLOT_PATH
from src.data_processor import load_tracking_data, calculate_centers, calculate_kinematics
from src.visualizer import plot_trajectories, plot_speed_subplots, create_trajectory_video

def main():
    try:
        # 1. データのロードと前処理
        print("INFO: Loading data...")
        df = load_tracking_data()
        processed_df = calculate_centers(df)
        
        # 2. 速度・加速度の計算
        print("INFO: Calculating kinematics (speed, acceleration)...")
        kinematics_df = calculate_kinematics(processed_df)

        # 3. speed異常値検出
        # 速度が計算できない最初のフレーム(NaN)を除外してから、速度のトップ5を抽出
        valid_df = kinematics_df.dropna(subset=['speed'])
        anomalies = valid_df.nlargest(5, 'speed')
        
        print("INFO: Anomaly frames detected:")
        print("="*50)
        # 必要な列だけ絞り込んで表示
        print(anomalies[['frame', 'id', 'cx', 'cy', 'speed', 'acceleration']].to_string(index=False))
        print("="*50 + "\n")

        # 4. 軌跡の可視化
        target_ids = [6, 7, 13, 27, 44, 51]
        print(f"INFO: Generating trajectory plot for IDs: {target_ids}")
        plot_trajectories(
            df=processed_df,
            target_ids=target_ids,
            save_path=TRAJECTORY_PLOT_PATH
        )
        print(f"SUCCESS: Plot saved to {TRAJECTORY_PLOT_PATH}")

        # 5. 速度のサブプロット描画
        print("INFO: Generating speed subplots...")
        plot_speed_subplots(
            df=kinematics_df,
            target_ids=target_ids,
            save_path=SPEED_PLOT_PATH
        )
        print(f"SUCCESS: Speed plot saved to {SPEED_PLOT_PATH}")

        # 6. 軌跡アニメーションの生成
        print("\nINFO: Generating trajectory animation video...")
        create_trajectory_video(
            df=kinematics_df,
            target_ids=target_ids,
            input_video_path=INPUT_VIDEO_PATH,
            output_video_path=ANIMATION_OUTPUT_PATH
        )
        print(f"SUCCESS: Animation saved to {ANIMATION_OUTPUT_PATH}")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()