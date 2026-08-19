## A dynamic programming algorithm for the Robotic Cell Problem with a fixed job processing order

Alessandro Minoli, Giovanni Righini (2026)

<!-- #### TODO

assicurarsi che 
```
python3 MILP_formulation.py
```
produca un output coerente con computational_results_MILP_formulation.csv -->

### Usage

Compile with :

```
mkdir build
cd build
cmake ..
make
cd ..
```

Run on a specific instance with :

```
./bin/RCP_with_fixed_job_sequence <path_to_instance_file>
```

### Datasets

- Directory [dataset_D1/](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/tree/main/dataset_D1) contains the 1680 instance files of Dataset D1 
- Directory [dataset_D2/](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/tree/main/dataset_D2) contains the 3000 instance files of Dataset D2. This directory is furthed divided in 20 subdirectories (one for each instance class), that contain 150 instances each.

### Format of the instance files

```
m                                   # number of machines
n                                   # number of jobs
p_1,1    p_1,2    ...  p_1,n        # processing times
p_2,1    p_2,2    ...  p_2,n
...
p_m,1    p_m,2    ...  p_m,n
t_0,0    t_0,1    ...  t_0,m+1      # travel times
t_1,0    t_1,1    ...  t_1,m+1
...
t_m+1,0  t_m+1,1  ...  t_m+1,m+1
```

### Computational results

The following .csv files contain the computational results presented in the paper.

- [computational_results_MILP_formulation](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/blob/main/computational_results_MILP_formulation.csv), with fields:
``` 
instance_path,m,n,seed,milp_time,exact_time
```
- [computational_results_dataset_D1](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/blob/main/computational_results_dataset_D1.csv), with fields:
``` 
instance_path,m,n,seed,exact_sol,exact_time,u1_sol,u2_sol,h_rho1_sol,h_rho2_sol,h_rho2_time
``` 
- [computational_results_dataset_D2](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/blob/main/computational_results_dataset_D2.csv), with fields:
``` 
instance_path,tr,pr,m,n,seed,exact_sol,exact_time,u1_sol,u2_sol,h_rho1_sol,h_rho2_sol,h_rho2_time
``` 
This is the meaning of the fields:
- instance_path
- m : number of machines
- n : number of jobs
- seed 
- tr : maximum travel time, i.e. travel times in [1,tr]
- pr : maximum processing time, i.e. processing times in [1,pr]
- milp_time : runtime [s] of MILP formulation or "TIME_LIMIT"
- exact_sol : optimal completion time found by the exact DP algorithm
- exact_time : runtime [s] of the exact DP algorithm
- u1_sol : completion time found by the "*One job at a time*" heuristic
- u2_sol : completion time found by the "*One machine at a time*" heuristic
- h_rho1_sol : completion time found by the heuristic DP algorithm with $\rho=1$
- h_rho2_sol : completion time found by the heuristic DP algorithm with $\rho=2$
- h_rho2_time : runtime [s] of the heuristic DP algorithm with $\rho=2$

The tables and figures reported in the paper are meant to visualize the reported computational results.
To create the tables (in .csv format) and the figures (in .pdf format), run the following commands:

```
cd scripts
chmod +x run.sh
./run.sh
cd ..
```
You will find the output in the [scripts](https://github.com/alessandro-minoli/DP_for_RCP_with_a_fixed_job_processing_order/blob/main/scripts) directory.

