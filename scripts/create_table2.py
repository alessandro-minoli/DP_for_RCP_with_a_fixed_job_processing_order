import csv
import statistics
from collections import defaultdict

INPUT_CSV = "../computational_results_dataset_D1.csv"
OUTPUT_CSV = "table2.csv"

FIELDNAMES = ["m", "n", "median", "iqr"]


def main():
    groups = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["m"]), int(row["n"]))
            groups[key].append(float(row["exact_time"]))

    rows = []
    for m, n in sorted(groups):
        times = groups[(m, n)]
        q1, _, q3 = statistics.quantiles(times, n=4, method="inclusive")
        rows.append({
            "m": m,
            "n": n,
            "median": f"{statistics.median(times):.2f}",
            "iqr": f"{q3 - q1:.2f}",
        })

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
