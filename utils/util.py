#
# Util methods
#


def get_number_of_machines(jobs_data):
    machines = set()
    for j in jobs_data:
        for o in j:
            machines.add(o[0])
    return len(machines)


def get_number_of_operations(jobs_data):
    nbr_operations = 0
    for j in jobs_data:
        for o in j:
            nbr_operations += 1
    return nbr_operations


def convert_indexes(i, j, M):
    return i * M + j


def get_job_from_operation(i, jobs):
    op_idx = 0
    for idx, j in enumerate(jobs):
        op_idx += len(j)
        if op_idx > i:
            return idx


def get_operation_x(x, jobs):
    op_idx = 0
    for j in jobs:
        for o in j:
            if op_idx == x:
                return o
            op_idx += 1


def get_operation_indexes_for_machine_m(m, jobs):
    indexes = []
    op_idx = 0
    for j in jobs:
        for o in j:
            if o[0] == m:
                indexes.append(op_idx)
            op_idx += 1
    return indexes


def get_operation_indexes_for_job_j(j, jobs):
    op_idx = 0
    for i in range(j):
        for o in jobs[i]:
            op_idx += 1
    return list(range(op_idx, op_idx + len(jobs[j])))


def extract_ij_from_k(k, M):
    j = k % M
    i = int((k - j) / M)
    return [i, j]


def convert_response_to_operation_results(response, M):
    operation_results = {}
    for k, v in response.first[0].items():
        if (v == 1):
            res = extract_ij_from_k(k, M)
            operation_results[res[0]] = res[1]
    return operation_results


def fill_QUBO_with_indexes(Q, i, t, k, t_prime, M, value):
    index_a = convert_indexes(i, t, M)
    index_b = convert_indexes(k, t_prime, M)
    if index_a > index_b:
        index_a, index_b = index_b, index_a
    Q[index_a][index_b] += value


def print_first_N_responses(response, N):
    # print("FIRST-----------------------------")
    # print(response.first)
    # print("INFO-----------------------------")
    # print(response.info)
    # print("RECORD-----------------------------")
    # print(response.record)
    # print("VARIABLES-----------------------------")
    # print(response.variables)
    # print("VARTYPE-----------------------------")
    # print(response.vartype)
    # print("TOTAL-----------------------------")
    # print(response)
    print(response.to_pandas_dataframe().head(N))
    # for res in response:
    #     print(res)
    #     N -= 1
    #     if N == 0:
    #         return