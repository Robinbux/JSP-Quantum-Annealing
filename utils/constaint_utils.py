import numpy as np

from utils.util import *


# Check for h3
def h3_constraint_is_fulfilled(operation_results, jobs_data):
    nbr_jobs = len(jobs_data)
    N = get_number_of_operations(jobs_data)
    if len(operation_results) != N:
        return False
    return True


# Check for h1
def h1_constraint_is_fulfilled(operation_results, jobs_data):
    nbr_jobs = len(jobs_data)
    for j in range(nbr_jobs):
        for i in get_operation_indexes_for_job_j(j, jobs_data)[:-1]:
            if operation_results[i] + get_operation_x(i, jobs_data)[1] > operation_results[i+1]:
                return False
    return True


# Check for h1
# def h1_constraint_is_fulfilled(operation_results, jobs_data):
#     nbr_jobs = len(jobs_data)
#     for j in range(nbr_jobs):
#         for k in range(len(jobs_data[j]) - 1):
#             for l in range(len(jobs_data[j]) - 1, k, -1):
#                 if operation_results[k] + get_operation_x(k, jobs_data)[1] > operation_results[l]:
#                     return False
#     return True


# Check for h2
def h2_constraint_is_fulfilled(operation_results, jobs_data, M):
    nbr_machines = get_number_of_machines(jobs_data)
    for m in range(nbr_machines):
        arr = np.zeros((M + 3,), dtype=np.int)
        for o in get_operation_indexes_for_machine_m(m, jobs_data):
            for i in range(operation_results[o], operation_results[o] + get_operation_x(o, jobs_data)[1]):
                if arr[i] == 1:
                    return False
                arr[i] = 1
    return True
