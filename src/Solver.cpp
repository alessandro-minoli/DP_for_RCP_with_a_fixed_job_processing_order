#include "Solver.h"
#include "State.h"
#include "Pool.h"

#include <algorithm>
#include <assert.h>
#include <chrono>
#include <iostream>
#include <vector>
#include <limits>

using std::tuple;
using std::vector;

int J;
int M;
vector<vector<int>> G_p;
vector<vector<int>> G_t;
vector<vector<vector<int>>> G_lambda_factors;
vector<int> G_mu_factors_1;
vector<vector<vector<int>>> G_mu_factors_2;

tuple<int, double> Solver::run_exact_dp(Instance &ins, bool verbose)
{
    J = ins.J;
    M = ins.M;
    G_p = ins.p;
    G_t = ins.t;
    G_lambda_factors = ins.lambda_factors;
    G_mu_factors_1 = ins.mu_factors_1;
    G_mu_factors_2 = ins.mu_factors_2;

    auto start = std::chrono::high_resolution_clock::now();

    int best_obj_val = ins.U;
    State *best_state = nullptr;

    // creating the initial state

    State *initial = new State();

    std::fill((initial->x).begin(), (initial->x).end(), 0);
    initial->x[0] = 1;

    std::fill((initial->C).begin(), (initial->C).end(), INF);
    initial->C[0] = 0;

    std::fill((initial->n).begin(), (initial->n).end(), 0);

    initial->set_e();

    std::unordered_map<State *, State *> pred;
    pred.emplace(initial, nullptr);

    Pool pool(ins.U);
    pool.try_push(initial);

    while (!pool.is_empty())
    {

        State *s = pool.pop();

        // the first final state we reach is the optimal solution,
        // because states with lower t are popped from the pool first
        if (s->is_final())
        {
            assert(s->t <= best_obj_val);
            best_obj_val = s->t;
            best_state = s;
            break;
        }

        for (int m = 0; m != M + 1; ++m)
        {
            if (s->machine_is_non_idle_and_non_blocked(m))
            {

                int j = s->x[m];

                State *s_next = new State(*s);

                assert(s->C[m] != INF);
                s_next->t = std::max(s->t + G_t[s->y][m], s->C[m]) + G_t[m][m + 1];

                s_next->y = m + 1;

                if (m > 0 || j == J)
                {
                    s_next->x[m] = 0;
                    s_next->C[m] = INF;
                }
                else
                {
                    assert(m == 0 && j < J);
                    s_next->x[m] = j + 1;
                    s_next->C[m] = s_next->t;
                }

                if (m + 1 < M + 1)
                {
                    s_next->x[m + 1] = j;
                    s_next->C[m + 1] = s_next->t + G_p[m + 1][j];
                }

                ++(s_next->n[m]);
                s_next->set_e();

                bool pushed = pool.try_push(s_next);

                if (pushed)
                {
                    assert(pred.count(s_next) == 0);
                    pred.emplace(s_next, s);
                }
                else
                {
                    delete s_next;
                }
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    assert(best_state != nullptr);
    if (verbose)
    {
        std::cout << "--- SOLUTION ----------------------------" << std::endl;
        print_optimal_solution(best_state, pred);
    }

    // int extended_states_cnt = pred.size();
    // int used_IDs_cnt = pool.get_next_free_id();

    for (const auto &key : pred)
    {
        delete key.first;
    }
    pred.clear();

    int z_optimal = best_obj_val;
    double execution_time = elapsed.count();
    return std::make_tuple(z_optimal, execution_time);
}

tuple<int, double> Solver::run_heuristic_dp(Instance &ins, int rho, bool verbose)
{
    J = ins.J;
    M = ins.M;
    G_p = ins.p;
    G_t = ins.t;
    G_lambda_factors = ins.lambda_factors;
    G_mu_factors_1 = ins.mu_factors_1;
    G_mu_factors_2 = ins.mu_factors_2;

    auto start = std::chrono::high_resolution_clock::now();

    int best_obj_val = std::numeric_limits<int>::max();
    State *best_state = nullptr;

    vector<tuple<int, int>> heuristic_extension_candidates;
    auto cmp_function = [](const std::tuple<int, int> &a, const std::tuple<int, int> &b)
    {
        return std::get<1>(a) < std::get<1>(b);
    };

    State *initial = new State();

    std::fill((initial->x).begin(), (initial->x).end(), 0);
    initial->x[0] = 1;

    std::fill((initial->C).begin(), (initial->C).end(), INF);
    initial->C[0] = 0;

    std::fill((initial->n).begin(), (initial->n).end(), 0);

    initial->set_e();

    std::unordered_map<State *, State *> pred;
    pred.emplace(initial, nullptr);

    // if this heuristic has worse objective than ins.U, 
    // then the following line must be changed to ins.U + value.
    // for our instances, value=15000 works.
    Pool pool(ins.U + 15000);  
    pool.try_push(initial);

    while (!pool.is_empty())
    {

        State *s = pool.pop();

        if (s->is_final())
        {
            assert(s->t <= best_obj_val);
            best_obj_val = s->t;
            best_state = s;
            break;
        }

        heuristic_extension_candidates.clear();

        for (int m = 0; m != M + 1; ++m)
        {
            if (s->machine_is_non_idle_and_non_blocked(m))
            {
                assert(s->C[m] != INF);
                heuristic_extension_candidates.emplace_back(m, s->e[m]);
            }
        }

        if (rho >= heuristic_extension_candidates.size())
        {
            std::sort(
                heuristic_extension_candidates.begin(),
                heuristic_extension_candidates.end(),
                cmp_function);
        }
        else
        {
            std::partial_sort(
                heuristic_extension_candidates.begin(),
                heuristic_extension_candidates.begin() + rho,
                heuristic_extension_candidates.end(),
                cmp_function);
        }

        for (int i = 0; i != std::min(rho, static_cast<int>(heuristic_extension_candidates.size())); ++i)
        {
            int m = std::get<0>(heuristic_extension_candidates[i]);

            int j = s->x[m];

            State *s_next = new State(*s);

            assert(s->C[m] != INF);
            s_next->t = std::max(s->t + G_t[s->y][m], s->C[m]) + G_t[m][m + 1];

            // can only be true in heuristic case
            if (s_next->t > best_obj_val)
            {
                delete s_next;
                continue;
            }

            s_next->y = m + 1;

            if (m > 0 || j == J)
            {
                s_next->x[m] = 0;
                s_next->C[m] = INF;
            }
            else
            {
                assert(m == 0 && j < J);
                s_next->x[m] = j + 1;
                s_next->C[m] = s_next->t;
            }

            if (m + 1 < M + 1)
            {
                s_next->x[m + 1] = j;
                s_next->C[m + 1] = s_next->t + G_p[m + 1][j];
            }

            ++(s_next->n[m]);
            s_next->set_e();

            bool pushed = pool.try_push(s_next);

            if (pushed)
            {
                assert(pred.count(s_next) == 0);
                pred.emplace(s_next, s);
            }
            else
            {
                delete s_next;
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    if (verbose)
    {
        if (best_state != nullptr)
        {
            std::cout << "--- SOLUTION ----------------------------" << std::endl;
            print_optimal_solution(best_state, pred);
        }
        else
        {
            std::cerr << "ERROR: best_state == nullptr" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    for (const auto &key : pred)
    {
        delete key.first;
    }
    pred.clear();

    int z_optimal = best_obj_val;
    double execution_time = elapsed.count();
    return std::make_tuple(z_optimal, execution_time);
}

std::tuple<int, double> Solver::run_heuristic_one_job_at_a_time(Instance &ins, bool verbose)
{
    return run_heuristic_one_at_a_time(ins,verbose,true,false);
}

std::tuple<int, double> Solver::run_heuristic_one_machine_at_a_time(Instance &ins, bool verbose)
{
    return run_heuristic_one_at_a_time(ins,verbose,false,true);
}

std::tuple<int, double> Solver::run_heuristic_one_at_a_time(Instance &ins, bool verbose, bool one_job, bool one_machine)
{
    if ((one_job && one_machine) || !(one_job || one_machine))
    {
        std::cerr << "ERROR: invalid setting of parameters 'one_job' and 'one_machine'" << std::endl;
        exit(EXIT_FAILURE);
    }

    J = ins.J;
    M = ins.M;
    G_p = ins.p;
    G_t = ins.t;
    G_lambda_factors = ins.lambda_factors;
    G_mu_factors_1 = ins.mu_factors_1;
    G_mu_factors_2 = ins.mu_factors_2;

    auto start = std::chrono::high_resolution_clock::now();

    int best_obj_val = std::numeric_limits<int>::max();
    State *best_state = nullptr;

    State *initial = new State();

    std::fill((initial->x).begin(), (initial->x).end(), 0);
    initial->x[0] = 1;

    std::fill((initial->C).begin(), (initial->C).end(), INF);
    initial->C[0] = 0;

    std::fill((initial->n).begin(), (initial->n).end(), 0);

    initial->set_e();

    std::unordered_map<State *, State *> pred;
    pred.emplace(initial, nullptr);

    State *s = initial;

    while (true)
    {

        if (s->is_final())
        {
            assert(s->t <= best_obj_val);
            best_obj_val = s->t;
            best_state = s;
            break;
        }

        int m_destination = -1;
        
        if (one_job) // one job at a time
        {
            for (int m = M; m >= 0; --m)
            {
                if (s->machine_is_non_idle_and_non_blocked(m))
                {
                    assert(s->C[m] != INF);
                    m_destination = m;
                    break;
                }
            }
        }
        else // one machine at a time
        {
            for (int m = 0; m != M + 1; ++m)
            {
                if (s->machine_is_non_idle_and_non_blocked(m))
                {
                    assert(s->C[m] != INF);
                    m_destination = m;
                    break;
                }
            }
        }
        if (m_destination == -1)
        {
            std::cerr << "ERROR: unreachable code" << std::endl;
            exit(EXIT_FAILURE);
        }

        int m = m_destination;

        int j = s->x[m];

        State *s_next = new State(*s);

        assert(s->C[m] != INF);
        s_next->t = std::max(s->t + G_t[s->y][m], s->C[m]) + G_t[m][m + 1];

        s_next->y = m + 1;

        if (m > 0 || j == J)
        {
            s_next->x[m] = 0;
            s_next->C[m] = INF;
        }
        else
        {
            assert(m == 0 && j < J);
            s_next->x[m] = j + 1;
            s_next->C[m] = s_next->t;
        }

        if (m + 1 < M + 1)
        {
            s_next->x[m + 1] = j;
            s_next->C[m + 1] = s_next->t + G_p[m + 1][j];
        }

        ++(s_next->n[m]);
        s_next->set_e();
        
        assert(pred.count(s_next) == 0);
        pred.emplace(s_next, s);
        s = s_next;
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    if (verbose)
    {
        if (best_state != nullptr)
        {
            std::cout << "--- SOLUTION ----------------------------" << std::endl;
            print_optimal_solution(best_state, pred);
        }
        else
        {
            std::cerr << "ERROR: best_state == nullptr" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    for (const auto &key : pred)
    {
        delete key.first;
    }
    pred.clear();

    int z_optimal = best_obj_val;
    double execution_time = elapsed.count();
    return std::make_tuple(z_optimal, execution_time);
}

void Solver::print_optimal_solution(State *s, std::unordered_map<State *, State *> pred)
{
    if (pred[s] != nullptr)
        print_optimal_solution(pred[s], pred);
    std::cout << *s;
}