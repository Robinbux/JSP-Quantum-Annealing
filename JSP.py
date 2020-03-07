import numpy as np
import yaml
import sys

from optimization import jsp_optimizations as jsp_op
from constraints import jsp_constraints as jsp_cst
from utils import dwave_sampler, constaint_utils, automatization_utils
from utils.scheduling_plot import plot_operations, plot_matrix
from utils.util import *
from utils.arg_parser import parse_arguments
from utils.param_util import load_params
import dwave.inspector


def main(args=None):
    options, unknown = parse_arguments(args)
    params = load_params()

    # Jobs
    jobs_data = [  # task = (machine_id, processing_time).
        [(0, 3), (1, 2), (2, 1)],  # Job0
        [(2, 2), (0, 1), (1, 2)]   # Job1
    ]

    # Other constants
    nbr_jobs = len(jobs_data)
    nbr_machines = get_number_of_machines(jobs_data)
    N = nbr_jobs * len(jobs_data[0])  # Num Operations -- Rows
    M = 7  # Upper Time Limit -- Cols

    operation_results = {}
    nbr_of_constraint_success = 0
    stop = False

    while nbr_of_constraint_success < 10 and not stop:
        # Initialize Matrix
        Q = np.zeros((M * N, M * N))

        # Space Minimization -- Machine level
        jsp_op.minimize_spaces_on_machine_level(Q, jobs_data, M, params["gamma"])
        # Space Minimization -- Job level
        jsp_op.minimize_spaces_on_job_level(Q, jobs_data, M, params["delta"])
        # Time Optimization
        jsp_op.optimize_time(Q, jobs_data, M, params["epsilon"])

        # h1 implementation
        jsp_cst.add_h1_constraint(Q, jobs_data, M, params["eta"])
        # h2 implementation
        jsp_cst.add_h2_constraint(Q, jobs_data, M, params["alpha"])
        # h3 implementation
        jsp_cst.add_h3_constraint(Q, jobs_data, M, params["beta"])

        # Converting the QUBO to BQM and sample on D-Wave machine
        response = dwave_sampler.sample_on_dwave(Q, options.q)

        # Ger operation results
        operation_results = convert_response_to_operation_results(response, M)
        if options.v:
            print(operation_results)

        # Check for constraint violations
        # Check for h3
        if not constaint_utils.h3_constraint_is_fulfilled(operation_results, jobs_data):
            if options.a:
                if options.v:
                    automatization_utils.print_failure("h3", params["eta"], params["alpha"],
                                                       params["beta"], nbr_of_constraint_success)
                    print("Increasing beta")
                    print("Trying again with values: ")
                    print(params)
                params["beta"] += 1
                nbr_of_constraint_success = 0
                continue
            else:
                automatization_utils.print_failure("h3", params["eta"], params["alpha"],
                                                   params["beta"], nbr_of_constraint_success)
                if options.v:
                    print("RESPONSE: ")
                    print(response)
                sys.exit()

        # Check for h1
        if not constaint_utils.h1_constraint_is_fulfilled(operation_results, jobs_data):
            if options.a:
                if options.v:
                    automatization_utils.print_failure("h1", params["eta"], params["alpha"],
                                                       params["beta"], nbr_of_constraint_success)
                    print("Increasing eta")
                    print("Trying again with values: ")
                    print(params)
                params["eta"] += 1
                nbr_of_constraint_success = 0
                continue
            else:
                automatization_utils.print_failure("h1", params["eta"], params["alpha"],
                                                   params["beta"], nbr_of_constraint_success)
                if options.v:
                    print("RESPONSE: ")
                    print(response)
                sys.exit()

        # Check for h2
        if not constaint_utils.h2_constraint_is_fulfilled(operation_results, jobs_data, M):
            if options.a:
                if options.v:
                    automatization_utils.print_failure("h2", params["eta"], params["alpha"],
                                                       params["beta"], nbr_of_constraint_success)
                    print("Increasing alpha")
                    print("Trying again with values: ")
                    print(params)
                params["alpha"] += 1
                nbr_of_constraint_success = 0
                continue
            else:
                automatization_utils.print_failure("h2", params["eta"], params["alpha"],
                                                   params["beta"], nbr_of_constraint_success)
                if options.v:
                    print("RESPONSE: ")
                    print(response)
                sys.exit()

        if not options.a:
            break

        # Increase number of success
        nbr_of_constraint_success += 1

    print(operation_results)

    print("BEFORE")
    if options.v:
        print("RESPONSE: ")
        print(response)
    print("AFTER")

    if options.i:
        dwave.inspector.show(response)

    if options.a:
        automatization_utils.print_success(params["eta"], params["alpha"], params["beta"], params["gamma"],
                                           params["delta"])

    # Replace params in yaml file:
    if options.r:
        with open('parameters.yaml', 'w') as outfile:
            yaml.dump(params, outfile, default_flow_style=False, sort_keys=False)

    # Plot chart
    plot_operations(jobs_data, operation_results)

    # Print Matrix
    if options.m:
        plot_matrix(Q, jobs_data, M)


if __name__ == "__main__":
    main()
