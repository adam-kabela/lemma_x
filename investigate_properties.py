from sage.all import *
from auxiliary_functions import *

D = graphs.DiamondGraph() #K_4 minus one edge
H3 = graphs.PathGraph(6)
H3.add_edges([(0,6),(1,6),(4,7),(5,7)]) # two triangles connected by path
D1 = graphs.CycleGraph(4)
D1.add_edges([(0,4),(1,4)]) # diamond with one edge subdivided (it is not K_{2,3})
K2_4 = graphs.CompleteBipartiteGraph(2,4) 
KS2_4 = graphs.CompleteGraph(1) #K^{SM}_{2,4}
KS2_4.add_edges([(0,2),(0,3),(0,4),(0,5),(2,6),(3,7),(4,8),(5,9),(1,6),(1,7),(1,8),(1,9)])
C6halved = graphs.CycleGraph(6) # 2 C_4s glued by one edge
C6halved.add_edge(2,5)
cactus9 = graphs.CycleGraph(9)
cactus9.allow_multiple_edges(True)
cactus9.add_edges([(0,8),(2,3),(5,6)])
#cactus9.add_edges([(0,11),(3,10),(6,9),(10,12),(11,13),(12,14),(9,15),(15,16),(13,17)])
#cactus9.add_edges([(14,18),(14,18),(16,20),(16,20),(17,19),(17,19)])
#cactus9.add_edges([(14,18),(16,20),(17,19)])

# there should be no diamond in graph and no induced H3 in line graph
def check_D_and_H3(M): 
    G = copy(M)
    G = G.to_simple() #simple graph G for M
    if has_subgraph(G, D):
        return False # M contains diamond (not necessarily induced)
    L = line_graph_of_multigraph(M)
    if L.subgraph_search(H3, induced=True) != None:
        return False # L(M) contains induced H3
    return True

# there should be at least 10 vertices of degree at least 3
def investigate_degrees(M):
    degree_1_and_2 = []
    for v in M.vertices():
        if M.degree(v) <= 2:
            degree_1_and_2.append(v)        
    if M.order() - len(degree_1_and_2) >= 10: # there are enough vertices of degree at least 3
        return []
    else:
        return [[degree_1_and_2, []]]

# each vertex of each triangle should have an additional neighbour
def investigate_triangles(M):
    output = []
    for v in M.vertices():
        N = M.neighbors(v)
        if len(N) == 2: # precisely two neighbours
            if M.has_edge(N[0],N[1]): # and the neighbours are adjacent, so it is a triangle       
                output.append([[v], N+[v]]) # triangle N+[v] contains vertex v with no neighbour outside
    return output # list of problematic vertices of triangles

# each cut-vertex should form at most one non-trivial component
def investigate_cut_vertices(M):
    output = []
    for v in M.vertices():
        Mprime = copy(M)
        Mprime.delete_vertex(v)
        non_trivial_components = get_nontrivial_components(Mprime)
        if len(non_trivial_components) >= 2: #Gprime has at least two non-trivial components
            for C in non_trivial_components:
                output.append([C, [v]]) # cut-vertex v gives non-trivial components, one ot htem is C 
    return output # list of problematic components and corresponding cut-vertices

# each 2-edge-cut should form at most one nontrivial component        
def investigate_2_edge_cuts(M):
    output = []
    E = edges_without_diplicities(M)
    for pair in get_pairs(E):
        Mprime = copy(M)
        Mprime.delete_edges(pair)
        non_trivial_components = get_nontrivial_components(Mprime)
        if len(non_trivial_components) >= 2: #has at least two non-trivial components
            for C in non_trivial_components:
                output.append([C, pair]) # 2-edge-cut pair gives non-trivial components, one ot them is C 
    return output # list of problematic components and corresponding 2-edge-cuts

# for each D1 each vertex of degree 2 in simplified D1 should have an additional neighbour
def investigate_D1s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(D1, induced = True): #also considers automorphisms
        for v in S:
            if G.degree(v) == 2:
                output.append([[v], S])
    return output # list of problematic vertices and corresponding D1s

#for each K^M_{2,4} at least one of w_i should have a non-pendant neighbour other than v_1, v_2
def investigate_KM2_4s(M):
    G = copy(M)
    G = G.to_simple() # it is easier to find it without multiedges and then check
    output = []
    for S in G.subgraph_search_iterator(K2_4, induced = True): #also considers automorphisms
        K = M.subgraph(S)    
        if min_degree(K) >= 3: #check multiedges, see definition of K^M_{2,4}
            K = K.to_simple()
            V = [v for v in K.vertices() if K.degree(v) == 4] #vertices v_1, v_2 from definitin
            W = [w for w in K.vertices() if w not in V] #vertices w_i from definition
            K_needs_extension = True
            Gprime = copy(G)
            Gprime.delete_vertices(V)
            for w in W:
                for n in Gprime.neighbors(w):
                    if G.degree(n) >= 2: # w has a non-pendant neighbour other than v_1, v_2
                        K_needs_extension = False
            if K_needs_extension:
                X = []
                for w in W:
                    X.append(w) # add aneighbour of some w_i
                    X += Gprime.neighbors(w) # increase degree of neighbour by adding its neighbour
                output.append([X, S])
    return output # list of problematic sets of vertices, and corresponding K^M_{2,4}s

#each subgraph K in K^{SM}_{2,4} should satisfy sum deg_M(u) >= 21
#where the sum is taken over all vertices of V(K) - {v_1, v_2}  
def investigate_KM4_P4s(M):
    G = copy(M)
    G = G.to_simple() # it is easier to find it without multiedges and then check
    output = []
    for S in G.subgraph_search_iterator(KS2_4, induced = True): #also considers automorphisms
        internal_vertices = S[2:] #2,3,...,9
        if degree_sum(G, internal_vertices) == 16:
            #(2,6),(3,7),(4,8),(5,9)
            if (S[0],S[2]) in M.multiple_edges(labels=False) or (S[1],S[6]) in M.multiple_edges(labels=False):
                if (S[0],S[3]) in M.multiple_edges(labels=False) or (S[1],S[7]) in M.multiple_edges(labels=False):
                    if (S[0],S[4]) in M.multiple_edges(labels=False) or (S[1],S[8]) in M.multiple_edges(labels=False):
                        if (S[0],S[5]) in M.multiple_edges(labels=False) or (S[1],S[9]) in M.multiple_edges(labels=False):
                            output.append([internal_vertices, S])
    return output

def investigate_K2_4s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(K2_4, induced = True): #also considers automorphisms
        internal_vertices = S[2:] #vertices of larger partity
        if degree_sum(G, internal_vertices) <= 8:
            output.append([internal_vertices, S])
    return output

def investigate_C6halved(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(C6halved, induced = False): #also considers automorphisms
        if G.degree(S[0]) + G.degree(S[4]) == 4: # also tests S[1], S[3] in another automorphism
            if induces_no_multiedges(M, S):
                output.append([[S[0], S[4]], list(G.subgraph(S).edges(labels=False))]) # at least one of S[0], S[4] should have another neighbour in M 
                #output.append([[S[0], S[4]], list(G.subgraph(S).edges(labels=False))]) # experimental
    return output

def contains_cactus9(M):
    if M.order() <= 8:
        return False
    return is_subgraph_of_multigraph_induced_in_simple(cactus9, M)