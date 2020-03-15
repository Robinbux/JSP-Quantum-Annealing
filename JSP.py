import numpy as np
import sys

from constraints.JSPConstraint import JSPConstraint
from optimization.JSPOptimization import JSPOptimization
from utils import dwave_sampler, constaint_utils, automatization_utils
from utils.util import *
from utils.arg_parser import parse_arguments, execute_flags
from utils.param_util import load_params


def main(args=None):
    options, unknown = parse_arguments(args)
    params = load_params()

    # Jobs
    jobs_data = [  # task = (machine_id, processing_time).
        [(0, 3), (1, 2), (2, 2)],  # Job0
        [(0, 2), (2, 1), (1, 4)],  # Job1
        [(1, 4), (2, 3)]  # Job2
    ]

    # Other constants
    nbr_operations = get_number_of_operations(jobs_data)  # Num Operations -- Rows
    T = 9  # Upper Time Limit -- Cols

    operation_results = {}
    nbr_of_constraint_success = 0
    stop = False

    while nbr_of_constraint_success < 50 and not stop:

        jsp_constraint = JSPConstraint(jobs_data, T, params["alpha"], params["beta"], params["eta"])
        jso_optimization = JSPOptimization(jobs_data, T, params["gamma"], params["delta"], params["epsilon"])

        # Initialize Matrix
        QUBO = np.zeros((T * nbr_operations, T * nbr_operations))

        jso_optimization.add_optimizations(QUBO)
        jsp_constraint.add_constraints(QUBO)

        # Converting the QUBO to BQM and sample on D-Wave machine
        response = dwave_sampler.sample_on_dwave(QUBO, options.q)

        # Ger operation results
        operation_results = convert_response_to_operation_results(response, T)
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
                execute_flags(options, response, jobs_data, operation_results, params, QUBO, T)
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
                execute_flags(options, response, jobs_data, operation_results, params, QUBO, T)
                sys.exit()

        # Check for h2
        if not constaint_utils.h2_constraint_is_fulfilled(operation_results, jobs_data, T):
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
                execute_flags(options, response, jobs_data, operation_results, params, QUBO, T)
        if not options.a:
            break

        # Increase number of success
        nbr_of_constraint_success += 1

    print(operation_results)

    execute_flags(options, response, jobs_data, operation_results, params, QUBO, T, success=True)

    if options.a:
        automatization_utils.print_success(params["eta"], params["alpha"], params["beta"], params["gamma"],
                                           params["delta"], params["epsilon"])


if __name__ == "__main__":
    main()
