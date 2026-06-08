from pathlib import Path

# パスの設定
BASE_DIR = Path(__file__).resolve().parent.parent # f_terasawaディレクトリ
DATA_PATH = BASE_DIR / "data" / "tracking_data.txt"
OUTPUT_DIR = BASE_DIR / "data" / "output"
TRAJECTORY_PLOT_PATH = OUTPUT_DIR / "trajectories.png"
SPEED_PLOT_PATH = OUTPUT_DIR / "speed_subplots.png"
INPUT_VIDEO_PATH = BASE_DIR / "data" / "117093_trimmed.mp4"
ANIMATION_OUTPUT_PATH = OUTPUT_DIR / "trajectory_animation.webm"

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