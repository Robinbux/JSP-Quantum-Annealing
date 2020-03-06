#
# Util methods
#

def get_number_of_machines(jobs_data):
    max_index = 1
    for j in range(len(jobs_data)):
        for o in range(len(jobs_data[0])):
            if (jobs_data[j][o][0] > max_index):
                max_index = jobs_data[j][o][0]
    return max_index + 1


def convert_indexes(i, j, M):
    return i * M + j


def get_job_from_operation(i, jobs):
    return int(i / len(jobs[0]))


def get_operation_x(x, jobs):
    # TODO: Error Handling
    row_index = int(x / len(jobs[0]))
    col_index = x % len(jobs[0])
    return jobs[row_index][col_index]


def get_operation_indexes_for_machine_m(m, jobs):
    indexes = []
    for j in range(len(jobs)):
        for o in range(len(jobs[0])):
            if jobs[j][o][0] == m:
                indexes.append(j * len(jobs[j]) + o)
    return indexes


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

def fill_Q_with_indexes(Q, i, t, k, t_prime, M, value):
    index_a = convert_indexes(i, t, M)
    index_b = convert_indexes(k, t_prime, M)
    if index_a > index_b:
        index_a, index_b = index_b, index_a
    Q[index_a][index_b] += value
