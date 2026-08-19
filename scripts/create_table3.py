import csv
import statistics
from collections import defaultdict

INPUT_CSV = "../computational_results_dataset_D2.csv"
OUTPUT_CSV = "table3.csv"

FIELDNAMES = ["tr", "pr", "m", "n", "median", "iqr"]

EXCLUDED_TR_PR = {(50, 10), (50, 25)}


def main():
    groups = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            key = (int(row["tr"]), int(row["pr"]), int(row["m"]), int(row["n"]))
            groups[key].append(float(row["exact_time"]))

    rows = []
    for tr, pr, m, n in sorted(groups):
        if (tr, pr) in EXCLUDED_TR_PR:
            continue

        times = groups[(tr, pr, m, n)]
        q1, _, q3 = statistics.quantiles(times, n=4, method="inclusive")
        rows.append({
            "tr": tr,
            "pr": pr,
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
