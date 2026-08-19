import csv
import statistics
from collections import defaultdict

INPUT_CSV = "../computational_results_dataset_D2.csv"
OUTPUT_CSV = "table7.csv"

FIELDNAMES = ["tr", "pr", "m", "n", "median", "iqr", "red"]

TR_VALUES = {50}
PR_VALUES = {10, 25, 50, 100, 150, 200, 250, 300}
M_VALUES = {12}
N_VALUES = {30}


def main():
    exact_times = defaultdict(list)
    h_rho2_times = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            tr, pr, m, n = int(row["tr"]), int(row["pr"]), int(row["m"]), int(row["n"])
            if tr not in TR_VALUES or pr not in PR_VALUES or m not in M_VALUES or n not in N_VALUES:
                continue
            key = (tr, pr, m, n)
            exact_times[key].append(float(row["exact_time"]))
            h_rho2_times[key].append(float(row["h_rho2_time"]))

    rows = []
    for tr, pr, m, n in sorted(exact_times):
        times = h_rho2_times[(tr, pr, m, n)]
        q1, _, q3 = statistics.quantiles(times, n=4, method="inclusive")
        median_h_rho2 = statistics.median(times)
        median_exact = statistics.median(exact_times[(tr, pr, m, n)])

        rounded_median_h_rho2 = round(median_h_rho2, 2)
        rounded_median_exact = round(median_exact, 2)
        red = 100.0 * (rounded_median_exact - rounded_median_h_rho2) / rounded_median_exact

        rows.append({
            "tr": tr,
            "pr": pr,
            "m": m,
            "n": n,
            "median": f"{median_h_rho2:.2f}",
            "iqr": f"{q3 - q1:.2f}",
            "red": f"{red:.2f}",
        })

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
