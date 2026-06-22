from itertools import product
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def solve(filename):

    # read DP optimal value
    with open(f"dataset_D1_out/{filename}") as f:
        lines = f.readlines()
        DP_objective = int(lines[3].split()[1])
        DP_time = float(lines[4].split()[1])

    with open(f"dataset_D1_out_UB2/{filename}") as f:
        UB2 = int(f.readlines()[2])

    assert UB2 >= DP_objective

    with open(f"dataset_D1/{filename}") as f:

        m = int(f.readline()) 
        n = int(f.readline())

        tmp = np.zeros((m,n), dtype=int)
        for i in range(m):
            p_i = list(map(int, f.readline().split()))
            for k in range(n):
                tmp[i,k] = p_i[k]
        tmp = np.transpose(tmp)

        p = []
        for j in range(n+1):
            p.append([None] * (m+1))
        for row in range(n):
            for col in range(m):
                p[row+1][col+1] = int(tmp[row,col])
        τ = []
        for i in range(0,m+2):
            τ.append(list(map(int, f.readline().split())))

    J = list(range(1,n+1))
    M = list(range(m+2))
    O = list(product(J,[h for h in M if h < m+1]))
    B = UB2

    with gp.Env() as env:
        with gp.Model("RCP", env=env) as model:

            model.setParam("OutputFlag", 0)
            model.setParam('TimeLimit', 5*60)

            x,y,t = dict(), dict(), dict()
            for (i,h) in O:
                t[(i,h)] = model.addVar(vtype=GRB.CONTINUOUS, lb=0)
                for (j,k) in O:
                    if i != j or h != k:
                        x[(i,h),(j,k)] = model.addVar(vtype=GRB.BINARY)
                        # y[(i,h),(j,k)] = model.addVar(vtype=GRB.CONTINUOUS, lb=0)

            model.setObjective(t[(n,m)]+τ[m][m+1], GRB.MINIMIZE)

            # Each operation must have one successor, with the exception of the last one, i.e. operation (n,m):
            model.addConstrs(
                gp.quicksum(x[(i,h),(j,k)] for (j,k) in O if j != i or k != h) == 1
                for (i,h) in O 
                    if i != n or h != m
            )

            # Each operation must have one precedessor, with the exception of the first one, i.e. operation (1,0):
            model.addConstrs(
                gp.quicksum(x[(i,h),(j,k)] for (i,h) in O if i != j or h != k) == 1
                for (j,k) in O 
                    if j != 1 or k != 0
            )

            # Travel times between any two consecutive operations
            model.addConstrs(
                t[(j,k)] >= t[(i,h)] + τ[h][h+1] + τ[h+1][k] - (B - τ[m][m+1] + τ[h][h+1] + τ[h+1][k]) * (1 - x[(i,h),(j,k)]) 
                for (i,h) in O
                    for (j,k) in O 
                        if i != j or h != k
            )

            # Blocking constraints
            model.addConstrs(
                t[(k,i)] >= t[(k-1,i+1)] + τ[i+1][i+2] + τ[i+2][i]
                for i in range(m)
                    for k in range(2,n+1)
            )

            # Completion times
            model.addConstrs(
                t[(j,k)] >= t[(j,k-1)] + τ[k-1][k] + p[j][k] 
                for (j,k) in O 
                    if k > 0
            )

            model.optimize()

            if model.Status == GRB.TIME_LIMIT:
                print(f"{filename} TIME_LIMIT")
            elif model.Status == GRB.OPTIMAL:
                print(f"{filename},{model.Runtime:.6f},{DP_time:.6f}")
                assert abs(model.ObjVal - DP_objective) < 0.001
            else:
                print(f"{filename} Status {model.Status}")
                assert False
                        

count = 0
for m in [4,5,6,7]:
    for n in [4,6,8,10]:
        for seed in range(10):
            filename = f"m_{m:02d}_n_{n:02d}_seed_{seed:02d}.txt"
            solve(filename)
            count += 1
print(count)