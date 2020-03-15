import argparse
import dwave.inspector
import yaml

from utils.scheduling_plot import plot_operations, plot_matrix
from utils.util import *


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--automatical", dest='a',
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
    parser.add_argument('-p', "--plot", dest='p', help="Plot the graph", action='store_true')

    return parser.parse_known_args(args=args) if args is not None else parser.parse_known_args()


def execute_flags(options, response, jobs_data, operation_results, params, Q, M, success=False):
    if options.v:
        print_first_N_responses(response, 10)

    if options.i:
        dwave.inspector.show(response)

    # Replace params in yaml file:
    if options.r:
        with open('parameters.yaml', 'w') as outfile:
            yaml.dump(params, outfile, default_flow_style=False, sort_keys=False)

    # Plot chart
    if options.p and success:
        plot_operations(jobs_data, operation_results)

    # Plot QUBO as confusion matrix
    if options.m:
        plot_matrix(Q, jobs_data, M)
