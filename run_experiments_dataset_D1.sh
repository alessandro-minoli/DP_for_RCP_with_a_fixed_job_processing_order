#!/bin/bash

echo "instance_path,m,n,seed,exact_sol,exact_time,u1_sol,u2_sol,h_rho1_sol,h_rho2_sol,h_rho2_time"

for filename in dataset_D1/*.txt; do
    ./bin/RCP_with_fixed_job_sequence "$filename" test
done
