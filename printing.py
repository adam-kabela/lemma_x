import logging

proof = logging.FileHandler("output/proof.txt", mode="w")
#proof.terminator = ""
proof.setLevel(logging.INFO)
family = logging.FileHandler("output/F.py", mode="w")
family.setLevel(logging.WARNING)
logging.basicConfig(handlers=[proof, family], format='%(message)s', encoding='utf-8', level=logging.INFO, force=True)

def attempts_as_string(extensions, indices):
    if len(indices) == 0:
        return "There is no applicable extension. Subcase closed."
    output = ""
    do_vertex_line = True
    do_edge_line = True
    for i in sorted(indices):
        attempt = extensions[i]
        if isinstance(attempt, list): #new vertex
            if do_vertex_line:
                output += "adding a new vertex whose neighbourhood is "
                do_vertex_line = False
            N = [v for v in range(len(attempt)) if attempt[v] == 1]
            output += str(N) + " or "
        else: #new multiedge
            if do_edge_line:
                output += "adding a multiplicity for edge "
                do_edge_line = False
            output += str(attempt) + " or "
    return output[:-4]

def log_intro():
    log_family("# The computer investigates all multigraphs that might satisfy the lemma and logs the details in two files.")
    log_family("# File proof.txt is used for a computer-generated proof of the lemma. This file is long and describes the detailed steps of the proof.")
    log_family("# https://stackoverflow.com/questions/159521/text-editor-to-open-big-giant-huge-large-text-files")
    log_family("# File F.py lists all multigraphs from family F by their edges. This file is short and can be easily used in another Python program by: from F import *")
    log_family("F = [] # members of F are appended to this list.")

def log_case(case, k, number): 
    print_and_log_proof("\n# Case", case, "-- we consider k =", k, "##################################################################")
    print_and_log_proof("There are precisely", number, "non-isomorphic graphs on", k, "vertices which contain a C_" + str(k))
    print_and_log_proof("and contain neither solved shorter cycle nor diamond as a subgraph nor induced Gamma_3 in line graph.")    

def log_subcase(subcase, M, text):
    log_proof("\n#", subcase, text)
    log_proof("Testing multigraph with edges:", str(M.edges(labels=False)))
    
def log_problem(P):
    if len(P[1]) == 0:
        log_proof("\t", "The multigraph has fewer than 10 vertices of degree at least 3. Namely,", str(P[0]) + ".", "A new vertex should be added or an edge should be multiplied.")
    elif len(P[1]) == 1: #cut-vertex
        log_proof("\t", "Cut-vertex", P[1], "gives non-trivial components. The component", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 2: #2-edge-cut
        log_proof("\t", "2-edge-cut", P[1], "gives non-trivial components. The component", P[0], "should have an additional neighbour or one of", P[1], "should be a multiedge.")
    elif len(P[1]) == 3: #triangle
        log_proof("\t", "Triangle", P[1], "contains vertex", P[0], "which has only two neighbours. Vertex", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 5: #D1 -- its 5 vertices 
        log_proof("\t", "Subgraph D_1", P[1], "contains vertex", P[0], "which has only two neighbours. Vertex", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 6: #K2_4 -- its 6 vertices
        if len(P[0]) == 2:
            log_proof("\t", "Subgraph D_2", P[1], "contains vertics", P[0], "each of which has only two neighbours. Some of", P[0], "should have an additional neighbour.")
        elif len(P[0]) == 4:
            log_proof("\t", "Subgraph K_{2,4}", P[1], "contains vertics", P[0], "each of which has only two neighbours. Some of", P[0], "should have an additional neighbour.")
        else:
            log_proof("\t", "Submultigraph from K^M_{2,4}", P[1], "violates condition (14). Some of", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 10: #SK2_4 -- its 10 vertices
        log_proof("\t", "Submultigraph from K^M_{4,P_4}", P[1], "contains vertics", P[0], "each of which has only two neighbours. Some of", P[0], "should have an additional neighbour.")
    
def log_proof(*arguments):
    logger = logging.getLogger()
    logger.info(assemble_string(*arguments))
    
def log_family(*arguments):
    logger = logging.getLogger()
    logger.warning(assemble_string(*arguments))
    
def assemble_string(*arguments):
    output = ""
    for a in arguments:
        output += str(a) + " "
    return output[:-1]
    
def print_and_log_proof(*arguments):
    print(*arguments)
    log_proof(*arguments)
    
def print_and_log_family(*arguments):
    print(*arguments)
    log_family(*arguments)