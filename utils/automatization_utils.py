def print_failure(constraint_nbr, eta, alpha, beta, nbr_of_constraint_success):
    print("FAILED AT " + constraint_nbr + ".")
    print("ETA: " + str(eta))
    print("ALPHA: " + str(alpha))
    print("BETA: " + str(beta))
    print("Previous successful tries: " + str(nbr_of_constraint_success))

def print_success(eta, alpha, beta, gamma, delta, epsilon):
    print("*************************")
    print("*************************")
    print("SUCCESS!!!")
    print("ETA: " + str(eta))
    print("ALPHA: " + str(alpha))
    print("BETA: " + str(beta))
    print("GAMMA: " + str(gamma))
    print("DELTA: " + str(delta))
    print("EPSILON: " + str(epsilon))
    print("*************************")
    print("*************************")
