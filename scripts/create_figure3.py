import csv
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt

INPUT_CSV = "../computational_results_dataset_D2.csv"
OUTPUT_FIGURE = "figure3.pdf"

N_VALUES = [10, 20, 30]
TRAVEL_VALUES = (10, 25, 50)
COLORS = {10: "tab:blue", 25: "tab:orange", 50: "tab:green"}

# Instance classes shown, in display order: tr_10_pr_{10..60}, tr_25_pr_{25..150}, tr_50_pr_{50..300}
ORDER = [
    (t, p)
    for t in TRAVEL_VALUES
    for p in range(t, 6 * t + 1, t)
]


def main():
    exact_times = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if int(row["m"]) != 12:
                continue
            key = (int(row["n"]), int(row["tr"]), int(row["pr"]))
            exact_times[key].append(float(row["exact_time"]))

    stats = {}
    for key, times in exact_times.items():
        q1, _, q3 = statistics.quantiles(times, n=4, method="inclusive")
        stats[key] = {"median": statistics.median(times), "q1": q1, "q3": q3}

    # Shared y range across all instance classes present at n in N_VALUES
    q1_values = [s["q1"] for key, s in stats.items() if key[0] in N_VALUES]
    q3_values = [s["q3"] for key, s in stats.items() if key[0] in N_VALUES]
    y_min = min(q1_values) * 0.8
    y_max = max(q3_values) * 1.2

    plt.rcParams.update({
        "font.size": 13,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "axes.linewidth": 1.0,
    })

    fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)

    cap_w = 0.15
    for i, (ax, n) in enumerate(zip(axes, N_VALUES)):
        classes = [(t, p) for (t, p) in ORDER if (n, t, p) in stats]
        xs = list(range(len(classes)))
        labels = [f"tr_{t}_pr_{p}" for (t, p) in classes]

        for x, (t, p) in zip(xs, classes):
            s = stats[(n, t, p)]
            color = COLORS[t]
            ax.bar(x, s["median"], color=color, alpha=0.4, width=0.6)
            ax.vlines(x=x, ymin=s["q1"], ymax=s["q3"], color=color, linewidth=1, zorder=3)
            ax.hlines(y=s["q1"], xmin=x - cap_w, xmax=x + cap_w, color=color, linewidth=1, zorder=3)
            ax.hlines(y=s["q3"], xmin=x - cap_w, xmax=x + cap_w, color=color, linewidth=1, zorder=3)
            ax.scatter(x, s["median"], color=color, s=10, zorder=4)

        ax.set_xticks(xs)
        ax.set_xticklabels(labels, rotation=90, ha="center", va="bottom", fontsize=10)
        ax.set_xlabel("Instance class", fontsize=12)
        ax.tick_params(axis="x", pad=70)

        ax.set_ylim(y_min, y_max)
        ax.set_yscale("log")
        if i == 0:
            ax.set_ylabel("Runtime [s]", fontsize=12)
        ax.set_title(f"$n$ = {n}", fontsize=12)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE, format="pdf")

    print(f"Wrote {OUTPUT_FIGURE}")


if __name__ == "__main__":
    main()
