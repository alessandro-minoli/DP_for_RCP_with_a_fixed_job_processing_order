import csv
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

INPUT_CSV = "../computational_results_dataset_D1.csv"
OUTPUT_FIGURE = "figure2.pdf"

M_VALUES = list(range(5, 16, 2))
N_VALUES = list(range(4, 31, 2))


def main():
    exact_times = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["m"]), int(row["n"]))
            exact_times[key].append(float(row["exact_time"]))

    plt.rcParams.update({
        "font.size": 13,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "axes.linewidth": 1.0,
    })

    fig, ax = plt.subplots(figsize=(8, 5))

    for m in M_VALUES:
        q0_values, q25_values, median_values, q75_values, q100_values = [], [], [], [], []

        for n in N_VALUES:
            times = exact_times.get((m, n))
            if times:
                q25, _, q75 = statistics.quantiles(times, n=4, method="inclusive")
                q0_values.append(min(times))
                q25_values.append(q25)
                median_values.append(statistics.median(times))
                q75_values.append(q75)
                q100_values.append(max(times))
            else:
                q0_values.append(None)
                q25_values.append(None)
                median_values.append(None)
                q75_values.append(None)
                q100_values.append(None)

        # Outer band (0-100%)
        ax.fill_between(
            N_VALUES, q0_values, q100_values,
            color="C0", alpha=0.20, linewidth=0,
        )

        # IQR band (25-75%)
        ax.fill_between(
            N_VALUES, q25_values, q75_values,
            color="C0", alpha=0.45, linewidth=0,
        )

        # Median line
        ax.plot(N_VALUES, median_values, color="black", linewidth=1.5)

        # Direct label for m
        valid_idx = [i for i, v in enumerate(median_values) if v is not None]
        if valid_idx:
            last = valid_idx[-1]
            ax.text(
                N_VALUES[last] + 0.3,
                median_values[last],
                f"$m={m}$",
                verticalalignment="center",
                fontsize=12,
                color="black",
            )

    legend_elements = [
        Line2D([0], [0], color="black", lw=1.5, label="Median"),
        Patch(facecolor="C0", alpha=0.45, label="25th–75th percentile"),
        Patch(facecolor="C0", alpha=0.20, label="0th–100th percentile"),
    ]

    ax.legend(handles=legend_elements, loc="upper left", frameon=False)

    ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("Runtime [s]")
    ax.set_xticks(N_VALUES)

    ax.grid(True, which="major", linestyle="--", linewidth=0.6, alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE, format="pdf")

    print(f"Wrote {OUTPUT_FIGURE}")


if __name__ == "__main__":
    main()
