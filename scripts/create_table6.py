import csv
import statistics
from collections import defaultdict

INPUT_CSV = "../computational_results_dataset_D2.csv"
OUTPUT_CSV = "table6.csv"

FIELDNAMES = ["heuristic", "tr", "pr", "m", "n", "avg", "std"]

TR_VALUES = {50}
PR_VALUES = {10, 25, 50, 100, 150, 200, 250, 300}
M_VALUES = {12}
N_VALUES = {30}

HEURISTIC_FIELDS = [
    ("u1", "u1_sol"),
    ("u2", "u2_sol"),
    ("h_rho1", "h_rho1_sol"),
    ("h_rho2", "h_rho2_sol"),
]


def optimality_gap(sol, exact_sol):
    """Percentage optimality gap of a (minimization) solution above the exact optimum."""
    return 100.0 * (sol - exact_sol) / exact_sol


def main():
    groups = defaultdict(lambda: defaultdict(list))
    with open(INPUT_CSV, newline="") as f:
        for row in csv.DictReader(f):
            tr, pr, m, n = int(row["tr"]), int(row["pr"]), int(row["m"]), int(row["n"])
            if tr not in TR_VALUES or pr not in PR_VALUES or m not in M_VALUES or n not in N_VALUES:
                continue
            exact_sol = int(row["exact_sol"])
            for heuristic, field in HEURISTIC_FIELDS:
                gap = round(optimality_gap(int(row[field]), exact_sol), 2)
                groups[(tr, pr, m, n)][heuristic].append(gap)

    rows = []
    for heuristic, _ in HEURISTIC_FIELDS:
        for tr, pr, m, n in sorted(groups):
            gaps = groups[(tr, pr, m, n)][heuristic]
            rows.append({
                "heuristic": heuristic,
                "tr": tr,
                "pr": pr,
                "m": m,
                "n": n,
                "avg": f"{statistics.mean(gaps):.2f}",
                "std": f"{statistics.stdev(gaps):.2f}",
            })

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
