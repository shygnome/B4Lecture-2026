from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Path to Deep-EIoU tracking result txt file
DATA_PATH = Path("data/baseline/tracking_result.txt")

# Directory where analysis outputs will be saved
OUTPUT_DIR = Path("output")


def load_tracking_data(data_path: Path) -> pd.DataFrame:
    """Load MOT-format tracking result."""

    # MOTChallenge format:
    # frame, id, x, y, w, h, score, class, visibility, unused
    columns = [
        "frame",
        "track_id",
        "x",
        "y",
        "w",
        "h",
        "score",
        "class",
        "visibility",
        "unused",
    ]

    df = pd.read_csv(data_path, header=None, names=columns)

    # Calculate bounding box center coordinates
    # cx = x + w / 2
    # cy = y + h / 2
    df["cx"] = df["x"] + df["w"] / 2
    df["cy"] = df["y"] + df["h"] / 2

    return df


def plot_selected_trajectories(df: pd.DataFrame, output_path: Path) -> List[int]:
    """Plot clean trajectories of representative track IDs."""

    # Select the longest trajectories for visualization
    track_lengths = df.groupby("track_id").size().sort_values(ascending=False)
    selected_ids = track_lengths.head(5).index.tolist()

    plt.figure(figsize=(14, 7))

    for track_id in selected_ids:

        # Sort trajectory points by frame order
        track_df = df[df["track_id"] == track_id].sort_values("frame")

        # Draw player trajectory
        plt.plot(
            track_df["cx"],
            track_df["cy"],
            linewidth=2,
            label=f"ID {track_id}",
        )

        # Mark starting point
        plt.scatter(
            track_df.iloc[0]["cx"],
            track_df.iloc[0]["cy"],
            marker="o",
            s=70,
        )

        # Mark ending point
        plt.scatter(
            track_df.iloc[-1]["cx"],
            track_df.iloc[-1]["cy"],
            marker="X",
            s=90,
        )

    # Invert y-axis to match image coordinate system
    plt.gca().invert_yaxis()

    plt.xlabel("Center x [pixel]")
    plt.ylabel("Center y [pixel]")
    plt.title("Trajectories of Representative Track IDs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Selected track IDs: {selected_ids}")

    return selected_ids


def plot_trajectories_with_abnormal_points(
    df: pd.DataFrame,
    abnormal_df: pd.DataFrame,
    selected_ids: List[int],
    output_path: Path,
) -> None:
    """Plot selected trajectories and highlight abnormal movement points."""

    plt.figure(figsize=(14, 7))

    for track_id in selected_ids:

        track_df = df[df["track_id"] == track_id].sort_values("frame")

        # Draw full trajectory
        plt.plot(
            track_df["cx"],
            track_df["cy"],
            linewidth=2,
            label=f"ID {track_id}",
        )

        abnormal_track = abnormal_df[abnormal_df["track_id"] == track_id]

        # Highlight abnormal movement points
        if len(abnormal_track) > 0:
            plt.scatter(
                abnormal_track["cx"],
                abnormal_track["cy"],
                color="red",
                marker="x",
                s=120,
                linewidths=3,
                label=f"Abnormal ID {track_id}",
            )

    plt.gca().invert_yaxis()

    plt.xlabel("Center x [pixel]")
    plt.ylabel("Center y [pixel]")
    plt.title("Trajectories with Abnormal Movement Points")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def calculate_speed_acceleration(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate speed and acceleration for each track ID."""

    # Sort by track ID and frame number
    df = df.sort_values(["track_id", "frame"]).copy()

    # Calculate frame-to-frame displacement
    df["dx"] = df.groupby("track_id")["cx"].diff()
    df["dy"] = df.groupby("track_id")["cy"].diff()

    # Frame interval between consecutive observations
    df["frame_diff"] = df.groupby("track_id")["frame"].diff()

    # Speed calculation
    # speed = sqrt(vx^2 + vy^2)
    df["speed"] = np.sqrt(df["dx"] ** 2 + df["dy"] ** 2) / df["frame_diff"]

    # Acceleration = change in speed
    df["acceleration"] = df.groupby("track_id")["speed"].diff()

    return df


def plot_speed_acceleration(df: pd.DataFrame, output_path: Path) -> None:
    """Plot speed and acceleration of the longest track."""

    # Use the longest trajectory for motion analysis
    track_lengths = df.groupby("track_id").size().sort_values(ascending=False)
    target_id = track_lengths.index[0]

    track_df = df[df["track_id"] == target_id].sort_values("frame")

    plt.figure(figsize=(12, 6))

    # Speed curve
    plt.plot(
        track_df["frame"],
        track_df["speed"],
        label="Speed [pixel/frame]",
    )

    # Acceleration curve
    plt.plot(
        track_df["frame"],
        track_df["acceleration"],
        label="Acceleration [pixel/frame²]",
    )

    plt.xlabel("Frame")
    plt.ylabel("Value")
    plt.title(f"Speed and Acceleration of Track ID {target_id}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Speed/acceleration target track ID: {target_id}")


def get_abnormal_movements(df: pd.DataFrame) -> pd.DataFrame:
    """Get unusually large speed values."""

    valid_df = df.dropna(subset=["speed"]).copy()

    # Use top 1% speed values as abnormal movement threshold
    threshold = valid_df["speed"].quantile(0.99)

    abnormal_df = valid_df[valid_df["speed"] >= threshold]

    print(f"Abnormal speed threshold: {threshold:.2f} pixel/frame")
    print(f"Number of abnormal points: {len(abnormal_df)}")

    return abnormal_df


def save_abnormal_movements(abnormal_df: pd.DataFrame, output_path: Path) -> None:
    """Save abnormal movement points to CSV."""

    abnormal_df[
        ["frame", "track_id", "cx", "cy", "speed", "acceleration"]
    ].to_csv(output_path, index=False)


def save_extended_tracking_data(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save tracking data with added motion features."""

    df.to_csv(output_path, index=False)


def main() -> None:

    # Create output directory if it does not exist
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load Deep-EIoU tracking result
    df = load_tracking_data(DATA_PATH)

    print("Data shape:", df.shape)
    print("Number of unique track IDs:", df["track_id"].nunique())
    print("Frame range:", df["frame"].min(), "to", df["frame"].max())

    # Task 1: trajectory visualization
    clean_trajectory_output = OUTPUT_DIR / "selected_trajectories.png"

    selected_ids = plot_selected_trajectories(
        df,
        clean_trajectory_output,
    )

    # Task 2: motion feature calculation
    df = calculate_speed_acceleration(df)

    # Save extended dataset with speed and acceleration
    extended_output = OUTPUT_DIR / "tracking_with_motion_features.csv"

    save_extended_tracking_data(
        df,
        extended_output,
    )

    # Detect abnormal motion points
    abnormal_df = get_abnormal_movements(df)

    # Visualize abnormal movement locations
    abnormal_trajectory_output = OUTPUT_DIR / "trajectories_with_abnormal_points.png"

    plot_trajectories_with_abnormal_points(
        df,
        abnormal_df,
        selected_ids,
        abnormal_trajectory_output,
    )

    # Plot speed and acceleration curves
    speed_output = OUTPUT_DIR / "speed_acceleration.png"

    plot_speed_acceleration(df, speed_output)

    # Save abnormal points to CSV
    abnormal_output = OUTPUT_DIR / "abnormal_movements.csv"

    save_abnormal_movements(
        abnormal_df,
        abnormal_output,
    )


if __name__ == "__main__":
    main()