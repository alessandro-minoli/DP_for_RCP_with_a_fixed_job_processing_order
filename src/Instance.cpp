#include "Instance.h"

#include <fstream>

Instance::Instance(const std::string &filename)
{
    std::ifstream in(filename);
    if (!in)
    {
        std::cerr << "ERROR, " << __FILE__ << " : in function " << __func__ << " at line " << __LINE__ << std::endl
                  << "       Compiled on " << __DATE__ << " at " << __TIME__ << std::endl
                  << "       File " << filename << " does not exists" << std::endl;
        exit(EXIT_FAILURE);
    }

    in >> M;
    in >> J;

    std::vector<int> p_loading(J+1,0);
    p.push_back(p_loading);
    for (int i = 1; i != M + 1; ++i)
    {
        std::vector<int> p_i(J+1,0);
        for (int k = 1; k != J + 1; ++k)
        {
            in >> p_i[k];
        }
        p.push_back(p_i);
    }
    std::vector<int> p_unloading(J+1,0);
    p.push_back(p_unloading);

    for (int i = 0; i != M + 2; ++i)
    {
        std::vector<int> t_i(M+2);
        for (int j = 0; j != M + 2; ++j)
        {
            in >> t_i[j];
        }
        t.push_back(t_i);
    }

    in.close();

    max_number_of_extensions = M / 2 + 1;

    // initializing U, that is the bound given the "one job at a time" heuristic

    int tot_processing_time = 0;
    for (int i = 1; i != M + 1; ++i)
    {
        for (int k = 1; k != J + 1; ++k)
        {
            tot_processing_time += p[i][k];
        }
    }
    
    int tot_forward_travel_time = 0;
    for (int i = 0; i != M + 1; ++i)
    {
        tot_forward_travel_time += t[i][i + 1];
    }
    tot_forward_travel_time *= J;

    int tot_backward_travel_time = t[M + 1][0] * (J - 1);

    U = tot_processing_time + tot_forward_travel_time + tot_backward_travel_time;

    // computing lambda_factors

    for (int j = 0; j != J + 1; ++j)
    {
        std::vector<std::vector<int>> lambda_factors_j;

        for (int m = 0; m != M + 2; ++m)
        {
            std::vector<int> lambda_factors_m(M + 2, -1);
            if (j > 0)
            {
                lambda_factors_m[m] = 0;
                for (int k = m + 1; k != M + 2; ++k)
                {
                    lambda_factors_m[k] = lambda_factors_m[k - 1] + t[k - 1][k] + p[k][j];
                }
            }
            lambda_factors_j.push_back(lambda_factors_m);
        }
        lambda_factors.push_back(lambda_factors_j);
    }

    // computing mu_factors_1

    mu_factors_1.push_back(t[0][1] + t[1][0]);
    for (int m = 1; m != M + 1; ++m)
    {
        mu_factors_1.push_back(t[m][m + 1] + t[m + 1][m - 1] + t[m - 1][m]);// + p[m]);
    }

    // computing mu_factors_2

    for (int m = 0; m != M + 1; ++m)
    {
        std::vector<std::vector<int>> mu_factors_2_m;
        for (int j = 0; j != J + 1; ++j)
        {
            std::vector<int> mu_factors_2_mj(J + 1, -1);
            if (j > 0){
                mu_factors_2_mj[j] = 0;
                for (int i = j + 1; i != J + 1; ++i)
                {
                    mu_factors_2_mj[i] = mu_factors_2_mj[i - 1] + p[m][i];
                }
            }
            mu_factors_2_m.push_back(mu_factors_2_mj);
        }
        mu_factors_2.push_back(mu_factors_2_m);
    }
}

std::ostream &operator<<(std::ostream &os, const Instance &ins)
{
    os << "m = " << ins.M << std::endl;
    os << "n = " << ins.J << std::endl;
    os << "p =" << std::endl;
    for (int i = 0; i != ins.M + 2; ++i)
    {
        os << "\t";
        for (int k = 0; k != ins.J + 1; ++k)
        {
            os << ins.p[i][k] << " ";
        }
        os << std::endl;
    }

    os << "t =" << std::endl;
    for (int i = 0; i != ins.M + 2; ++i)
    {
        os << "\t";
        for (int j = 0; j != ins.M + 2; ++j)
        {
            os << ins.t[i][j] << " ";
        }
        os << std::endl;
    }

    // os << "U = " << ins.U << std::endl;
    // os << "max_number_of_extensions = " << ins.max_number_of_extensions << std::endl;

    /*
    os << "lambda_factors =" << std::endl;
    for (int j = 0; j != ins.J + 1; ++j)
    {
        os << "  j=" << j << std::endl;
        for (int m = 0; m != ins.M + 2; ++m)
        {
            os << "\t";
            for (int k = 0; k != ins.M + 2; ++k)
            {
                os << ins.lambda_factors[j][m][k] << " ";
            }
            os << std::endl;
        }
    }
    */
    
    /*
    os << "mu_factors_1 =\t";
    for (auto const &el : ins.mu_factors_1)
    {
        os << el << " ";
    }
    os << std::endl;
    */

    /*
    os << "mu_factors_2 =" << std::endl;
    for (int m = 0; m != ins.M + 1; ++m)
    {
        os << "  m=" << m << std::endl;
        for (int j = 0; j != ins.J + 1; ++j)
        {
            os << "\t";
            for (int i = 0; i != ins.J + 1; ++i)
            {
                os << ins.mu_factors_2[m][j][i] << " ";
            }
            os << std::endl;
        }
    }
    */

    return os;
}