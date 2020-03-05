from utils.util import *


#
# h1 implementation
#
def add_h1_constraint(Q, jobs_data, M, eta):
    nbr_jobs = len(jobs_data)
    for n in range(nbr_jobs):
        for i in range(n * len(jobs_data[0]), n * len(jobs_data[0]) + len(jobs_data[0]) - 1):
            for t in range(M):
                for t_prime in range(M):
                    if (t + get_operation_x(i, jobs_data)[1]) > t_prime:
                        fill_Q_with_indexes(Q, i, t, i+1, t_prime, M, eta)
                        #Q[convert_indexes(i, t, M)][convert_indexes(i + 1, t_prime, M)] += eta


#
# h2 implementation
#
def add_h2_constraint(Q, jobs_data, M, alpha):
    def Am_condition_fulfilled(i, t, k, t_prime, M, jobs):
        return i != k and 0 <= t and t_prime <= M and 0 < t_prime - t < get_operation_x(i, jobs)[1]

    def Bm_condition_fulfilled(i, t, k, t_prime, M, jobs):
        return i < k and t_prime == t and get_operation_x(i, jobs)[1] > 0 and get_operation_x(k, jobs)[1] > 0

    nbr_machines = get_number_of_machines(jobs_data)
    for m in range(nbr_machines):
        operation_indexes_m = get_operation_indexes_for_machine_m(m, jobs_data)
        for i in operation_indexes_m:
            for k in operation_indexes_m:
                for t in range(M):
                    for t_prime in range(M):
                        if Am_condition_fulfilled(i, t, k, t_prime, M, jobs_data) \
                                or Bm_condition_fulfilled(i, t, k, t_prime, M, jobs_data):
                            fill_Q_with_indexes(Q, i, t, k, t_prime, M, alpha)
                            #Q[convert_indexes(i, t, M)][convert_indexes(k, t_prime, M)] += alpha


#
# h3 implementation
#
def add_h3_constraint(Q, jobs_data, M, beta):
    nbr_jobs = len(jobs_data)
    N = nbr_jobs * len(jobs_data[0])
    for i in range(N):
        for u in range(M):
            for t in range(u):
                fill_Q_with_indexes(Q, i, t, i, u, M, beta*2)
                #Q[convert_indexes(i, t, M)][convert_indexes(i, u, M)] += beta * 2
        for t in range(M):
            fill_Q_with_indexes(Q, i, t, i, t, M, -beta)
            #Q[convert_indexes(i, t, M)][convert_indexes(i, t, M)] -= beta
