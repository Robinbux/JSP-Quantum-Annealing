import numpy as np
import pandas as pd
import yaml
import argparse
import sys

from optimization import jsp_optimizations as jsp_op
from constraints import jsp_constraints as jsp_cst
from utils import dwave_sampler, constaint_utils, automatization_utils
from utils.scheduling_plot import plot_operations, plot_matrix
from utils.util import *
import dwave.inspector


def run(args=None):
    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--automatically", dest='a',
                        help="Automatically increase 'Eta', 'Alpha' and 'Beta', until no constraint is violated anymore.",
                        action='store_true')
    parser.add_argument('-r', "--replace", dest='r',
                        help="Replace old values in the yaml file, with the automatically chosen ones.",
                        action='store_true')
    parser.add_argument('-v', "--verbose", dest='v', help="More verbose output.", action='store_true')
    parser.add_argument('-m', "--matrix", dest='m', help="Show an interactive confusion matrix of the final Q.",
                        action='store_true')
    parser.add_argument('-s', "--simulated", dest='s', help="Use the simulated annealer", action='store_true')
    parser.add_argument('-q', "--quantum", dest='q', help="Use the D-Wave quantum computer", action='store_true')
    parser.add_argument('-i', "--inspect", dest='i', help="Use the D-Wave inspector", action='store_true')

    options, unknown = parser.parse_known_args(args=args) if args is not None else parser.parse_known_args()


    with open("parameters.yaml", 'r') as stream:
        try:
            params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Lambdas
    # eta = params["eta"]  # h1
    # alpha = params["alpha"]  # h2
    # beta = params["beta"]  # h3
    # gamma = params["gamma"]  # Minimization -- Machine level
    # delta = params["delta"]  # Minimization -- Job level

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

    while nbr_of_constraint_success < 40 and not stop:
        # Initialize Matrix
        Q = np.zeros((M * N, M * N))

        # Space Minimization -- Machine level
        jsp_op.minimize_spaces_on_machine_level(Q, jobs_data, M, params["gamma"])
        # Space Minimization -- Job level
        jsp_op.minimize_spaces_on_job_level(Q, jobs_data, M, params["delta"])

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
                sys.exit()

        if not options.a:
            break

        # Increase number of success
        nbr_of_constraint_success += 1

    print(operation_results)

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
    run()
