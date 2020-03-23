from utils.util import *


class JSPOptimization:

    def __init__(self, jobs_data, T, gamma, delta, epsilon):
        self.jobs_data = jobs_data
        self.T = T
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon

    def add_optimizations(self, QUBO):
        self.__minimize_spaces_on_machine_level(QUBO)
        self.__minimize_spaces_on_job_level(QUBO)
        self.__optimize_time(QUBO)

    #
    # Space Minimization -- Machine level
    #
    def __minimize_spaces_on_machine_level(self, QUBO):
        nbr_machines = get_number_of_machines(self.jobs_data)
        for m in range(nbr_machines):  # Fix
            operation_indexes_m = get_operation_indexes_for_machine_m(m, self.jobs_data)
            for i in range(len(operation_indexes_m)):
                for k in range(len(operation_indexes_m)):
                    for t_prime in range(self.T):
                        for t in range(t_prime):
                            if k == i:
                                continue
                            penalty = (t_prime - (t + get_operation_x(operation_indexes_m[i], self.jobs_data)[1]))**2
                            fill_QUBO_with_indexes(QUBO, operation_indexes_m[i], t, operation_indexes_m[k], t_prime, self.T,
                                                   self.gamma * penalty)

    #
    # Space Minimization -- Job level
    #
    def __minimize_spaces_on_job_level(self, QUBO):
        nbr_jobs = len(self.jobs_data)
        for j in range(nbr_jobs):
            for i in get_operation_indexes_for_job_j(j, self.jobs_data)[:-1]:
                for t in range(self.T):
                    for t_prime in range(self.T):
                        penalty = (t_prime - (t + get_operation_x(i, self.jobs_data)[1]))**2
                        fill_QUBO_with_indexes(QUBO, i, t, i + 1, t_prime, self.T, self.delta * penalty)

    #
    # General time optimization
    #
    def __optimize_time(self, QUBO):
        N = get_number_of_operations(self.jobs_data)
        for i in range(N):
            for t in range(self.T):
                fill_QUBO_with_indexes(QUBO, i, t, i, t, self.T, self.epsilon * (t + get_operation_x(i, self.jobs_data)[1]))
