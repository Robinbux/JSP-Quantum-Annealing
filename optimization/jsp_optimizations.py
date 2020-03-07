### Optimization functions
from utils.util import *


#
# Space Minimization -- Machine level
#
def minimize_spaces_on_machine_level(Q, jobs_data, M, gamma):
    nbr_machines = get_number_of_machines(jobs_data)
    for m in range(nbr_machines):  # Fix
        operation_indexes_m = get_operation_indexes_for_machine_m(m, jobs_data)
        for i in range(len(operation_indexes_m)):
            for k in range(len(operation_indexes_m)):
                for t_prime in range(M):
                    for t in range(t_prime):
                        if (k == i):
                            continue
                        penalty = abs(t_prime - (t + get_operation_x(operation_indexes_m[i], jobs_data)[1]))
                        fill_Q_with_indexes(Q, operation_indexes_m[i], t, operation_indexes_m[k], t_prime, M, gamma * penalty)
                        #Q[convert_indexes(operation_indexes_m[i], t, M)][
                        #    convert_indexes(operation_indexes_m[k], t_prime, M)] += gamma * penalty


#
# Space Minimization -- Job level
#
def minimize_spaces_on_job_level(Q, jobs_data, M, delta):
    nbr_jobs = len(jobs_data)
    for n in range(nbr_jobs):
        for i in range(n * len(jobs_data[0]), n * len(jobs_data[0]) + len(jobs_data[0]) - 1):
            for t in range(M):
                for t_prime in range(M):
                    penalty = abs(t_prime - (t + get_operation_x(i, jobs_data)[1]))
                    fill_Q_with_indexes(Q, i, t, i+1, t_prime, M, delta * penalty)
                    #Q[convert_indexes(i, t, M)][convert_indexes(i + 1, t_prime, M)] += delta * penalty


#
# General time optimization
#
def optimize_time(Q, jobs_data, M, epsilon):
    nbr_jobs = len(jobs_data)
    N = nbr_jobs * len(jobs_data[0])
    for i in range(N):
        for t in range(M):
            fill_Q_with_indexes(Q, i, t, i, t, M, epsilon * t)
