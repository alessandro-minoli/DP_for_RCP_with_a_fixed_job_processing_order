#!/bin/bash

echo "instance_path,tr,pr,m,n,seed,exact_sol,exact_time,u1_sol,u2_sol,h_rho1_sol,h_rho2_sol,h_rho2_time"

for subdir in dataset_D2/*/; do
    for filename in "$subdir"*.txt; do
        ./bin/RCP_with_fixed_job_sequence "$filename" test
    done
done
