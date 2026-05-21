import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import fire


class Player_analysis:
    def __init__(self, data_path="117093_trimmed.txt", output_dir="result"):
        self.data_path = data_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def load_and_process_data(self):
        cols = ["frame", "id", "x", "y", "w", "h", "conf", "class", "vis", "none"]
        df = pd.read_csv(self.data_path, header=None, names=cols)
        df["cx"] = df["x"] + df["w"] / 2
        df["cy"] = df["y"] + df["h"] / 2

        print("INFO: Calculating kinematics...")

        def calculate_kinematics(group):
            group = group.sort_values("frame")
            dt = group["frame"].diff()
            dcx = group["cx"].diff()
            dcy = group["cy"].diff()

            group["speed"] = np.sqrt(dcx**2 + dcy**2) / dt
            group["acceleration"] = group["speed"].diff() / dt
            return group

        df = df.groupby("id", group_keys=False).apply(calculate_kinematics)

        # Select target IDs (GK 13 + Top 4 fastest)
        valid_df = df.dropna(subset=["speed"])
        top4 = (
            valid_df.loc[valid_df["id"] != 13]
            .groupby("id")["speed"]
            .max()
            .nlargest(4)
            .index.tolist()
        )
        target_ids = [13] + list(top4)
        print(f"INFO: Target IDs for plotting: {target_ids}\n")
        return df, target_ids

    def plot_trajectories(self, df, target_ids):
        plt.figure(figsize=(12, 8))

        for tid in target_ids:
            player_data = df[df["id"] == tid]
            plt.plot(
                player_data["cx"],
                player_data["cy"],
                marker="o",
                markersize=2,
                label=f"ID: {tid}",
                alpha=0.7,
            )

        plt.title("Player Trajectories")
        plt.xlabel("X coordinate (pixels)")
        plt.ylabel("Y coordinate (pixels)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.gca().invert_yaxis()
        plt.tight_layout()

        # Save processed trajectory graph
        save_path = os.path.join(self.output_dir, "trajectories.png")
        plt.savefig(save_path)
        plt.close()
        print(f"SUCCESS: Save the trajectory graph -> {os.path.abspath(save_path)}")

    def plot_speed(self, df, target_ids):
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for i, tid in enumerate(target_ids):
            ax = axes[i]
            player_data = df[df["id"] == tid]

            ax.plot(
                player_data["frame"],
                player_data["speed"],
                color="firebrick",
                marker="o",
                markersize=2,
                linestyle="-",
                linewidth=1,
                alpha=0.8,
            )
            ax.set_title(f"ID: {tid} Speed", fontsize=12)
            ax.set_xlabel("Frame", fontsize=10)
            ax.set_ylabel("Speed (pixels/frame)", fontsize=10)
            ax.grid(True, linestyle="--", alpha=0.5)

        if len(target_ids) < len(axes):
            axes[-1].axis("off")

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, "speed_subplots.png")
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"SUCCESS: Save the speed subplots -> {os.path.abspath(save_path)}")

    def run(self):
        """Main pipeline execution method."""
        df, target_ids = self.load_and_process_data()
        self.plot_trajectories(df, target_ids)
        self.plot_speed(df, target_ids)


if __name__ == "__main__":
    fire.Fire(Player_analysis)
