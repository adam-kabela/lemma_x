from investigate_properties import *

# get all violation of properties for multigraph M         
def get_all_problems(M):
    output = investigate_degrees(M)
    output += investigate_2_edge_cuts(M)
    output += investigate_cut_vertices(M)
    output += investigate_triangles(M)
    output += investigate_D1s(M)
    output += investigate_K2_4s(M)
    output += investigate_D2s(M)
    output += investigate_KM4_P4s(M)
    output += investigate_KM2_4s(M)
    return output

def choose_problem_and_get_all_solution_attempts(MaE, case):
    # extensions
    log_proof("Considering all problems and all non-investigated applicable extensions.")
    applicable_additions = get_all_applicable_additions(MaE)
    applicable_multiplications = get_all_applicable_multiplications(MaE)
    applicable_extensions = applicable_additions + applicable_multiplications
    # problems
    M = MaE.multigraph
    all_problems = get_all_problems(M)
    short_list = minimal_problems_and_solution_attempts(all_problems, M, applicable_additions, applicable_multiplications)
    if len(short_list) == 0: # no property is violated
        log_proof("There is no problem.")
        print_and_log_family("# In", case + ",", "a new member of F is added.")
        print_and_log_family("F += [", M.edges(labels = False), "]")
        log_proof("Branch over all applicable extensions:")
        log_proof("\t", attempts_as_string(applicable_extensions, list(range(len(applicable_extensions)))))
        return applicable_extensions 
    if len(short_list[0][1]) == 0: # zero possible solution attempts
        log_proof("There is a problem which cannot be solved:")
        log_problem(short_list[0][0])
        log_proof("Tried all non-investigated extension with a potential to solve this. None of them works. Subcase closed.")
        return []
    C = short_list[random_but_probability_tweaked(len(short_list))]
    log_proof("Choose a problem at random:")
    log_problem(C[0])
    log_proof("Branch over all solution attempts relevant to the problem:")
    log_proof("\t", attempts_as_string(applicable_extensions, C[1]))
    return [applicable_extensions[i] for i in C[1]]

# we choose just problems whose set of solution attempts is inclusion minimal
def minimal_problems_and_solution_attempts(problems, M, applicable_additions, applicable_multiplications):
    problems_and_solution_attempts = []
    for P in problems:
        attempts = get_indices_of_all_attempts(P, M, applicable_additions, applicable_multiplications)
        problems_and_solution_attempts.append([P, attempts])
    problems_and_solution_attempts.sort(key = lambda x: len(x[1])) #sort by number of solution attampts
    output = []
    for PaS in problems_and_solution_attempts: #filter by inclusion minimality
        minimal = True
        for known in output:
            if known[1].issubset(PaS[1]):  
                minimal = False
                break
        if minimal:
            output.append(PaS)
    return output

def get_all_applicable_additions(MaE):
    output = []
    for A in MaE.additions:
        if sum(A) >= 2: # new vertex has degree at least 2
            output.append(A)
        elif number_of_pendant_twins(MaE.multigraph, A) <= 1: # new vertex has at most one twin
            output.append(A)
    return output

def get_all_applicable_multiplications(MaE):
    output = []
    non_applicable = []
    for e in MaE.multiplications:
        if MaE.multigraph.degree(e[0]) > 1 and MaE.multigraph.degree(e[1]) > 1: #edge is non-pendant, and hence can be multiplied
            output.append(e)
    return output    
    
def get_indices_of_all_attempts(problem, M, applicable_additions, applicable_multiplications):
    addition_indices = get_indices_of_adding_vertex(problem, applicable_additions)
    shift = len(applicable_additions) # index shift
    multiplication_indices = get_indices_of_adding_multiedge(problem, applicable_multiplications, M, shift)
    return addition_indices.union(multiplication_indices) 
    
def get_indices_of_adding_vertex(problem, applicable_additions):
    output = set()
    if len(problem[1]) == 0: #not enough vertices of degree at least 3
        output = set(range(len(applicable_additions))) # indices of all applicable additions    
    else:
        for i in range(len(applicable_additions)): # extensions by new vertex
            N = applicable_additions[i]
            for v in problem[0]:         
                if N[v] == 1: # new vertex is neighbour of v
                    output.add(i)
                    break # prevent adding i twice
    return output

def get_indices_of_adding_multiedge(problem, applicable_multiplications, M, shift):
    output = set()
    if len(problem[1]) == 0: #not enough vertices of degree at least 3
        for i in range(len(applicable_multiplications)): 
            e = applicable_multiplications[i]
            if M.degree(e[0]) == 2 or M.degree(e[1]) == 2: # increases a low degree of vertex by multiedge
                output.add(i + shift) # index shifted to distinguish from vertex additions
    elif len(problem[1]) == 2: # problematic 2-edge-cut
        for e in problem[1]:
            for i in range(len(applicable_multiplications)):
                if e == applicable_multiplications[i]:                
                    output.add(i + shift)
                    break # prevent adding index twice
    return output