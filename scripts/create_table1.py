import csv
import re
from collections import defaultdict

INPUT_CSV = "../computational_results_MILP_formulation.csv"
OUTPUT_CSV = "table1.csv"

FIELDNAMES = ["m", "n", "milp_min_time", "milp_max_time", "tl_count"]

FILENAME_RE = re.compile(r"m_(\d+)_n_(\d+)_seed_(\d+)\.txt$")


def main():
    groups = defaultdict(list)
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            match = FILENAME_RE.search(row["instance_path"])
            m, n = int(match.group(1)), int(match.group(2))
            groups[(m, n)].append(row["milp_time"])

    rows = []
    for m, n in sorted(groups):
        times = groups[(m, n)]
        tl_count = sum(1 for t in times if t == "TIME_LIMIT")
        numeric_times = [float(t) for t in times if t != "TIME_LIMIT"]

        rows.append({
            "m": m,
            "n": n,
            "milp_min_time": f"{min(numeric_times):.2f}" if numeric_times else "",
            "milp_max_time": f"{max(numeric_times):.2f}" if numeric_times else "",
            "tl_count": tl_count,
        })

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
