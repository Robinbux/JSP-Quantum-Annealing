import argparse

def parse_arguments(args):
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

    return parser.parse_known_args(args=args) if args is not None else parser.parse_known_args()