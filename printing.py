import logging
#logging.basicConfig(filename='proof.txt', format='%(message)s', encoding='utf-8', level=logging.INFO, force=True)

proof = logging.FileHandler("proof.txt")
proof.setLevel(logging.INFO)
exceptions = logging.FileHandler("exceptions.txt")
exceptions.setLevel(logging.WARNING)
logging.basicConfig(handlers=[proof, exceptions], format='%(message)s', encoding='utf-8', level=logging.INFO, force=True)

#console = logging.StreamHandler()

def log_problem(P):
    if len(P[1]) == 0:
        log_more("The multigraph does not have 10 vertices of degree at least 3, vertices of smaller degree are", P[0], "a new vertex or muliedge should be added.")
    elif len(P[1]) == 1: #cut-vertex
        log_more("Cut-vertex", P[1], "gives non-trivial components and the component", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 2: #2-edge-cut
        log_more("2-edge-cut", P[1], "gives non-trivial components and the component", P[0], "should have an additional neighbour or one of", P[1], "should be a multiedge.")
    elif len(P[1]) == 3: #triangle
        log_more("Triangle", P[1], "contains vertex", P[0], "and", P[0], "should have a neighbour outside the triangle.")
    elif len(P[1]) == 5: #D1 -- its 5 vertices 
        log_more("Subdivided diamant D1", P[1], "contains vertex", P[0], "and", P[0], "should have a neighbour outside D1.")
    elif len(P[1]) == 6: #K2_4 -- its 6 vertices
        if len(P[0]) == 2:
            log_more("subgraph C6halved", P[1], "so some of", P[0], "should have an additional neighbour.")    
        elif len(P[0]) == 4:
            log_more("subgraph K_{2,4}", P[1], "so some of", P[0], "should have an additional neighbour.")
        else:
            log_more("multigraph from K^m_{2,4}", P[1], "so some of", P[0], "should have an additional neighbour.")
    elif len(P[1]) == 10: #SK2_4 -- its 10 vertices
        log_more("multigraph from K^{M}_{4,P_4}", P[1], "so some of", P[0], "should have a greater degree sum.")

def attempts_as_string(extensions, indices):
    output = ""
    do_vertex_line = True
    do_edge_line = True
    for i in sorted(indices):
        attempt = extensions[i]
        if isinstance(attempt, list): #new vertex
            if do_vertex_line:
                output += "adding a new vertex whose neighbourhood is: "
                do_vertex_line = False
            N = [v for v in range(len(attempt)) if attempt[v] == 1]
            output += str(N) + " or "
        else: #new multiedge
            if do_edge_line:
                output += "adding a multiplicity for edge: "
                do_edge_line = False
            output += str(attempt) + " or "
    return output[:-4]
            
def multigraph_as_string(M):
    return "Testing multigraph with edges: " + str(M.edges(labels= False))
    
def log_more(*arguments):
    output = ""
    for a in arguments:
        output += str(a) + " "
    logger = logging.getLogger()
    logger.info(output[:-1])
    #logging.info(output[:-1])

def log_exceptions(*arguments):
    print(*arguments)
    output = ""
    for a in arguments:
        output += str(a) + " "
    logger = logging.getLogger()
    logger.warning(output[:-1])
    
def print_and_log(*arguments):
    print(*arguments)
    log_more(*arguments)