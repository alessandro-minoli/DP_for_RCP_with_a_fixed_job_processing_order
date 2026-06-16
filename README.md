#### A dynamic programming algorithm for the Robotic Cell Problem with a fixed job processing order

Alessandro Minoli, Giovanni Righini (2026)

##### Usage

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

##### Format of instance files

```
J                                   # number of jobs
M                                   # number of machines
p_1,1    p_1,2    ...  p_1,J        # processing time on each machine of each job
p_2,1    p_2,2    ...  p_2,J
...
p_M,1    p_M,2    ...  p_M,J
t_0,0    t_0,1    ...  t_0,M+1      # travel time between each pair of stations
t_1,0    t_1,1    ...  t_1,M+1
...
t_M+1,0  t_M+1,1  ...  t_M+1,M+1
```
