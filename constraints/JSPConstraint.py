from utils.util import *


class JSPConstraint:

    def __init__(self, jobs_data, T, alpha, beta, eta):
        self.jobs_data = jobs_data
        self.T = T
        self.alpha = alpha
        self.beta = beta
        self.eta = eta

    def add_constraints(self, QUBO):
        self.__add_h1_constraint(QUBO)
        self.__add_h2_constraint(QUBO)
        self.__add_h3_constraint(QUBO)

    #
    # h1 implementation
    #
    def __add_h1_constraint(self, QUBO):
        nbr_jobs = len(self.jobs_data)
        for j in range(nbr_jobs):
            for i in get_operation_indexes_for_job_j(j, self.jobs_data)[:-1]:
                for t in range(self.T):
                    for t_prime in range(self.T):
                        if (t + get_operation_x(i, self.jobs_data)[1]) > t_prime:
                            fill_QUBO_with_indexes(QUBO, i, t, i + 1, t_prime, self.T, self.eta)

    #
    # h2 implementation
    #
    def __add_h2_constraint(self, QUBO):
        def Rm_condition_fulfilled(i, t, k, t_prime, M, jobs):
            return i != k and 0 <= t and t_prime <= M and 0 <= t_prime - t < get_operation_x(i, jobs)[1]

        nbr_machines = get_number_of_machines(self.jobs_data)
        for m in range(nbr_machines):
            operation_indexes_m = get_operation_indexes_for_machine_m(m, self.jobs_data)
            for i in operation_indexes_m:
                for k in operation_indexes_m:
                    for t in range(self.T):
                        for t_prime in range(self.T):
                            if Rm_condition_fulfilled(i, t, k, t_prime, self.T, self.jobs_data):
                                fill_QUBO_with_indexes(QUBO, i, t, k, t_prime, self.T, self.alpha)

    #
    # h3 implementation
    #
    def __add_h3_constraint(self, QUBO):
        N = get_number_of_operations(self.jobs_data)
        for i in range(N):
            for u in range(self.T):
                for t in range(u):
                    fill_QUBO_with_indexes(QUBO, i, t, i, u, self.T, self.beta * 2)
            for t in range(self.T):
                fill_QUBO_with_indexes(QUBO, i, t, i, t, self.T, -self.beta)
