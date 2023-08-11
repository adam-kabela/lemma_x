from sage.all import *
from printing import *
from auxiliary_functions import *

def is_solved_already_v0(current_case, solved_cases):
    for M in simplyfy_subsets_of_multiedges(current_case):
        for solved in solved_cases:
            if is_subgraph_of_multigraph(solved[0], M): # subgraph of current contains induced solved[0]
                log_more("Already solved in", solved[1]) # solved[1] is the subcase string
                return True
    return False

def is_solved_already(current_case, solved_cases):
    for solved in solved_cases:
        if is_subgraph_of_multigraph_induced_in_simple(solved[0], current_case): # subgraph of current contains induced solved[0]
            log_more("Already solved in", solved[1]) # solved[1] is the subcase string
            return True
    return False

def simplyfy_subsets_of_multiedges(M):
    multiedges = set(M.multiple_edges(labels = False))
    output = []
    for S in subsets(multiedges):
        Mprime = copy(M)
        Mprime.delete_edges(S)
        output.append(Mprime)
    return output