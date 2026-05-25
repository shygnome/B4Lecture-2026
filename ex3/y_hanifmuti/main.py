import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_results_with_parameters(metric='TI-HOTA'):
    df = pd.read_csv('results.csv')

    plt.figure(figsize=(9, 6))
    sns.set_theme(style="whitegrid")

    ax = sns.lineplot(
        data=df,
        x='Params_M',
        y=metric,
        hue='Tracker',
        style='Tracker',
        markers=True,
        markersize=9,
        linewidth=2.5,
        palette={'ByteTrack': '#1f77b4', 'BoT-SORT': '#ff7f0e'}
    )

    plt.title('Tracking Performance vs. Detector Parameter Size',
              fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Detector Parameters (Millions)',
               fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel(f'Tracking Performance ({metric})',
               fontsize=12, fontweight='bold', labelpad=10)

    plt.xticks([2.6, 9.4, 20.1, 25.3, 56.9], labels=['2.6M\n(YOLO11n)',
               '9.4M\n(YOLO11s)', '20.1M\n(YOLO11m)', '25.3M\n(YOLO11l)', '56.9M\n(YOLO11x)'],
               rotation=15, fontsize=10)
    plt.ylim(0.0, 1.0)
    plt.legend(title='Tracker Algorithm', loc='lower right', frameon=True)
    sns.despine()

    plt.tight_layout()
    plt.savefig('detector_parameter_scaling_curve.png', dpi=300)


def main():
    plot_results_with_parameters()


if __name__ == "__main__":
    main()
