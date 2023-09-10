from investigate_properties import *
from printing import *

# choose problems for investigating multigraph M         
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
    output = []
    all_problems = get_all_problems(MaE.multigraph)
    extensions = MaE.additions + MaE.multiplications
    shift = len(MaE.additions) # split of list of extensions to two parts
    short_list = minimal_problems_and_solution_attempts(all_problems, extensions, shift, MaE.multigraph)
    if len(short_list) == 0:
        print_and_log_family("#", case)
        print_and_log_family("F.append(", MaE.multigraph.edges(labels = False), ")")
        log_proof("There is no problem, cannot force particular extensions, so lets test all non-investigated extesnions.")
        for A in extensions:
            if isinstance(A, list): #extra vertex 
                if sum(A) >= 2:
                    output.append(A)
                elif number_of_twins(MaE.multigraph, A) <= 1:
                    output.append(A)
            else: #multiedge
                if MaE.multigraph.degree(A[1]) >= 2: #do not multiply pendant edges
                    output.append(A)
    elif len(short_list[0][1]) == 0:
        log_proof("There is a problem which cannot be solved:")
        log_problem(short_list[0][0])
        log_proof("Tried all non-investigated extension with a poterntial to solve this, but none of them works. Case closed.")
    else:
        C = short_list[random_but_probability_tweaked(len(short_list))]
        for PaE in short_list:
            if len(PaE[0][1]) == 0: 
                C = PaE
                break
        #log_proof("Relevant problems and solution attempts are:")
        #for PaE in short_list:
        #    log_problem(PaE[0])
        #    log_proof(attempts_as_string(extensions, PaE[1]))
        log_proof("Choose problem at random:")
        log_problem(C[0])
        log_proof("Branch over all relevant solution attempts:")
        log_proof(attempts_as_string(extensions, C[1]))
        for i in C[1]:
            output.append(extensions[i])
    return output
    
# we choose just problems whose set of solution attempts is inclusion minimal
def minimal_problems_and_solution_attempts(L, extensions, shift, M):
    problems_and_solution_attempts = []
    for P in L:
        attempts = get_indices_of_all_attempts(P, extensions, shift, M)
        problems_and_solution_attempts.append([P, attempts])
    problems_and_solution_attempts.sort(key = lambda x: len(x[1])) #sort by number of solution attampts
    output = []
    for PaS in problems_and_solution_attempts:
        if not any(O[1].issubset(PaS[1]) for O in output): #keep inclusion minimal 
            output.append(PaS)
    return output
    
def get_indices_of_all_attempts(problem, extensions, shift, M):
    if len(problem[1]) == 0: #not enough vertices of degree at least 3
        return get_indices_of_all_attempts_for_degrees(problem, extensions, shift, M)
    A = get_indices_of_all_attempts_of_adding_vertex(problem, extensions, shift, M)
    if len(problem[1]) == 2: # 2-edge-cut and one of non-trivial components
        return A.union(get_indices_of_all_attempts_of_adding_multiedge(problem, extensions, shift, M)) 
    return A #cut-vertex or triangle or D1 or K2_4

# for a problematic vertex add new neighbour which has degree at least 2 or has no twin
def get_indices_of_all_attempts_of_adding_vertex(problem, extensions, shift, M):
    output = set()
    for i in range(shift): # extensions by new vertex
        N = extensions[i]
        for v in problem[0]:         
            if N[v] > 0: # new vertex is neighbour of v
                if sum(N) >= 2 or number_of_twins(M, N) <= 1: # new vertex has degree at least 2 or has no twin
                    output.add(i)
                    break # prevent adding i twice
    return output

# multiply a problematic simple edge
def get_indices_of_all_attempts_of_adding_multiedge(problem, extensions, shift, M):
    output = set()
    for e in problem[1]:
        if M.degree(e[1]) >= 2: #do not multiply pendant edges
            for i in range(shift, len(extensions)): # extension by multiedge
                if e == extensions[i]:                
                    output.add(i)
                    break
    return output

def get_indices_of_all_attempts_for_degrees(problem, extensions, shift, M):
    output = set()
    for i in range(shift): # extensions by new vertex
        N = extensions[i]
        if sum(N) >= 2 or number_of_twins(M, N) <= 1: # new vertex has degree at least 2 or has no twin
            output.add(i)
    for i in range(shift, len(extensions)): # extension by multiedge
        e = extensions[i]
        if M.degree(e[0]) == 2 or M.degree(e[1]) == 2: # increases a low degree of vertex by multiedge
            output.add(i)
    return output    