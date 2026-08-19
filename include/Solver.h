#ifndef SOLVER_H
#define SOLVER_H

#include "Globals.h"
#include "Instance.h"
#include "State.h"

#include <tuple>
#include <unordered_map>

class Solver
{
public:

    Solver() = default;
    std::tuple<int, double> run_exact_dp                        (Instance &ins,          bool verbose = false);
    std::tuple<int, double> run_heuristic_dp                    (Instance &ins, int rho, bool verbose = false);
    std::tuple<int, double> run_heuristic_one_job_at_a_time     (Instance &ins,          bool verbose = false);
    std::tuple<int, double> run_heuristic_one_machine_at_a_time (Instance &ins,          bool verbose = false);

private:

    std::tuple<int, double> run_heuristic_one_at_a_time(Instance &ins, bool verbose, bool one_job, bool one_machine);
    static void print_optimal_solution(State *s, std::unordered_map<State *, State *> pred);
};

#endif