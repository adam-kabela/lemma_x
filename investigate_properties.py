from auxiliary_functions import *
from printing import *

D = graphs.DiamondGraph() # diamond a.k.a. K_4 minus one edge
Gamma3 = graphs.PathGraph(6)
Gamma3.add_edges([(0,6),(1,6),(4,7),(5,7)]) # two triangles connected by path with three edges
CM9 = graphs.CycleGraph(9)
CM9.allow_multiple_edges(True)
CM9.add_edges([(0,8),(2,3),(5,6)])

P5 = graphs.PathGraph(5)
D1 = P5.complement() # house a.k.a. diamond with one edge subdivided (it is not K_{2,3})
K2_4 = graphs.CompleteBipartiteGraph(2,4) 
D2 = graphs.CycleGraph(6) 
D2.add_edge(2,5) # domino a.k.a two C_4s glued by one edge
KM4_P4 = graphs.CompleteGraph(1) 
KM4_P4.add_edges([(0,2),(0,3),(0,4),(0,5),(2,6),(3,7),(4,8),(5,9),(1,6),(1,7),(1,8),(1,9)]) # four P4s with common ends

# there should be no diamond in M and no induced Gamma3 in L(M)
# and no flat fubgraph CM9 in M and no solved shorter cycle in M 
def multigraph_is_ok(M, n, printing, extension):
    message = ""
    if extension is not None:
        message = "\t " + attempts_as_string([extension], [0]) + " "
    is_ok = False
    if contains_D(M): # M contains D as a subgraph
        message += "would create D as a subgraph,"
    elif contains_Gamma3(M): # L(M) contains induced Gamma3
        message += "would create Gamma_3 as an induced subgraph in the line graph,"
    elif contains_CM9(M): # M contains CM9 as a flat subgraph
        message += "would create C^M_9 as a flat subgraph,"
    elif contains_solved_cycle(M, n):
        message += "would create shorter solved cycle as a subgraph,"
    else:
        is_ok = True
        message += "is ok"
    if is_ok == False:
        message += " this extension is discarded"
    if printing:
        log_proof(message)
    return is_ok

def contains_D(M): 
    G = copy(M)
    G = G.to_simple() #simple graph G for multigraph M
    return has_subgraph(G, D)
    
def contains_Gamma3(M): 
    L = line_graph_of_multigraph(M)
    return (L.subgraph_search(Gamma3, induced=True) is not None)
        
def contains_CM9(M):
    return has_flat_subgraph(M, CM9)
       
def contains_solved_cycle(M, n): 
    G = copy(M)
    G = G.to_simple() #simple graph G for M
    for solved in range(7, n):
        if has_subgraph(G, graphs.CycleGraph(solved)):
            return True
    return False

# there should be at least 10 vertices of degree at least 3
def investigate_degrees(M):
    degree_at_least_3 = [v for v in M.vertices() if M.degree(v) >= 3]
    if len(degree_at_least_3) >= 10: # there are enough vertices of degree at least 3
        return []
    return [[degree_at_least_3, []]]

# each 2-edge-cut should form at most one nontrivial component        
def investigate_2_edge_cuts(M):
    output = []
    E = simple_non_pendant_edges(M)
    for pair in get_pairs(E):
        Mprime = copy(M)
        Mprime.delete_edges(pair)
        non_trivial_components = get_nontrivial_components(Mprime)
        if len(non_trivial_components) >= 2: #has at least two non-trivial components
            for C in non_trivial_components:
                output.append([C, pair]) # 2-edge-cut pair gives non-trivial components, one of them is C 
    return output # list of problematic components and corresponding 2-edge-cuts

# each cut-vertex should form at most one non-trivial component
def investigate_cut_vertices(M):
    output = []
    for v in M.vertices():
        Mprime = copy(M)
        Mprime.delete_vertex(v)
        non_trivial_components = get_nontrivial_components(Mprime)
        if len(non_trivial_components) >= 2: #Gprime has at least two non-trivial components
            for C in non_trivial_components:
                output.append([C, [v]]) # cut-vertex v gives non-trivial components, one ot them is C 
    return output # list of problematic components and corresponding cut-vertices

# each vertex of each triangle should have an additional neighbour
def investigate_triangles(M):
    output = []
    for v in M.vertices():
        N = M.neighbors(v)
        if len(N) == 2: # precisely two neighbours
            if M.has_edge(N[0],N[1]): # and the neighbours are adjacent, so it is a triangle       
                output.append([[v], N+[v]]) # triangle N+[v] contains vertex v with no neighbour outside
    return output # list of problematic vertices of triangles

# for each D1 each vertex of degree 2 in D1 should have an additional neighbour
def investigate_D1s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    # each D1 sungraph of G is induced since G does not contain D as a subgraph
    for S in G.subgraph_search_iterator(D1, induced = True): #also considers automorphisms
        for v in S:
            if G.degree(v) == 2:
                output.append([[v], S])
                # possibly v is appended more than once with different S,
                # it is discarded later with minimal_problems_and_solution_attempts 
    return output # list of problematic vertices and corresponding D1s

def investigate_K2_4s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    # each K_{2,4} sungraph of G is induced since G does not contain D as a subgraph
    for S in G.subgraph_search_iterator(K2_4, induced = True): #also considers automorphisms
        internal_vertices = S[2:] #vertices of larger partity
        if degree_sum(G, internal_vertices) == 8:
            output.append([internal_vertices, S])
            # possibly internal_vertices are appended more than once with different S, it is discarded later
    return output

def investigate_D2s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(D2, induced = False): #also considers automorphisms
        if degree_sum(G, [S[0], S[4]]) == 4: # also tests S[1], S[3] in another automorphism
            output.append([[S[0], S[4]], S]) # at least one of S[0], S[4] should have another neighbour in M 
            # possibly [S[0], S[4]] are appended more than once with different S, it is discarded later
    return output

#each subgraph F from K^M_{4,P_4} should satisfy sum |N_M(u)| > 16
#where the sum is taken over all vertices of V(F) - {v_1, v_2}  
#E(F) = {(0,2),(0,3),(0,4),(0,5),(2,6),(3,7),(4,8),(5,9),(1,6),(1,7),(1,8),(1,9)}
def investigate_KM4_P4s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(KM4_P4, induced = False): #also considers automorphisms
        internal_vertices = S[2:] #2,3,...,9
        if degree_sum(G, internal_vertices) == 16:
            if at_least_one_is_multiedge(M, [(S[0],S[2]), (S[2],S[6]), (S[6],S[1])]): # see definition of K^M_{4,P_4}
                if at_least_one_is_multiedge(M, [(S[0],S[3]), (S[3],S[7]), (S[7],S[1])]):
                    if at_least_one_is_multiedge(M, [(S[0],S[4]), (S[4],S[8]), (S[8],S[1])]):
                        if at_least_one_is_multiedge(M, [(S[0],S[5]), (S[5],S[9]), (S[9],S[1])]):
                            output.append([internal_vertices, S])
                            # possibly internal_vertices are appended more than once with different S, it is discarded later
    return output

#for each K^M_{2,4} at least one of w_i should have a non-pendant neighbour distinct from v_1, v_2
def investigate_KM2_4s(M):
    G = copy(M)
    G = G.to_simple() # it is easier to find it without multiedges and then check
    output = []
    # each K_{2,4} sungraph of G is induced since G does not contain D as a subgraph
    for S in G.subgraph_search_iterator(K2_4, induced = True): #also considers automorphisms
        if at_least_one_is_multiedge(M, [(S[0],S[2]), (S[2],S[1])]): # see definition of K^M_{2,4}
            if at_least_one_is_multiedge(M, [(S[0],S[3]), (S[3],S[1])]):
                if at_least_one_is_multiedge(M, [(S[0],S[4]), (S[4],S[1])]):
                    if at_least_one_is_multiedge(M, [(S[0],S[5]), (S[5],S[1])]):
                        needs_extension = True
                        internal_vertices = S[2:] #2,3,...,5
                        Gprime = copy(G)
                        Gprime.delete_vertices([S[0],S[1]])
                        for w in internal_vertices:
                            if needs_extension:
                                for n in Gprime.neighbors(w): # neighbours of w distinct from v_1, v_2
                                    if G.degree(n) >= 2: # non-pendant
                                        needs_extension = False
                                        break
                        if needs_extension:
                            X = copy(internal_vertices)
                            for w in internal_vertices:
                                X += Gprime.neighbors(w) # increase degree of neighbour by adding its neighbour
                            output.append([X, S])
    return output # list of problematic sets of vertices, and corresponding K^M_{2,4}s