from auxiliary_functions import *

D = graphs.DiamondGraph() #diamond, K_4 minus one edge
Gamma3 = graphs.PathGraph(6)
Gamma3.add_edges([(0,6),(1,6),(4,7),(5,7)]) # two triangles connected by path
CM9 = graphs.CycleGraph(9)
CM9.allow_multiple_edges(True)
CM9.add_edges([(0,8),(2,3),(5,6)])

P5 = graphs.PathGraph(5)
D1 = P5.complement() # house, diamond with one edge subdivided (it is not K_{2,3})
K2_4 = graphs.CompleteBipartiteGraph(2,4) 
D2 = graphs.CycleGraph(6) # domino, 2 C_4s glued by one edge
D2.add_edge(2,5)
KM4_P4 = graphs.CompleteGraph(1) #K^{SM}_{2,4}
KM4_P4.add_edges([(0,2),(0,3),(0,4),(0,5),(2,6),(3,7),(4,8),(5,9),(1,6),(1,7),(1,8),(1,9)])

# there should be no diamond in M and no induced Gamma3 in L(M) and no flat fubgraph CM9 in M
def contains_D_or_Gamma3_or_CM9(M): 
    if contains_D(M):
        return True # M contains diamond subgraph (not necessarily induced)
    if contains_Gamma3(M):
        return True # L(M) contains induced Gamma3
    if contains_CM9(M):
        return True # M contains CM9 as a flat subgraph
    return False

def contains_D(M): 
    G = copy(M)
    G = G.to_simple() #simple graph G for M
    return has_subgraph(G, D)
    
def contains_Gamma3(M): 
    L = line_graph_of_multigraph(M)
    if L.subgraph_search(Gamma3, induced=True) == None:
        return False
    return True

def contains_CM9(M):
    return has_flat_subgraph(CM9, M)

# there should be at least 10 vertices of degree at least 3
def investigate_degrees(M):
    degree_1_and_2 = [v for v in M.vertices() if M.degree(v) <= 2]
    if M.order() - len(degree_1_and_2) >= 10: # there are enough vertices of degree at least 3
        return []
    return [[degree_1_and_2, []]]

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
                output.append([C, pair]) # 2-edge-cut pair gives non-trivial components, one ot them is C 
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
                output.append([C, [v]]) # cut-vertex v gives non-trivial components, one ot htem is C 
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

def investigate_K2_4s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(K2_4, induced = True): #also considers automorphisms
        internal_vertices = S[2:] #vertices of larger partity
        if degree_sum(G, internal_vertices) <= 8:
            output.append([internal_vertices, S])
    return output

def investigate_D2s(M):
    G = copy(M)
    G = G.to_simple()
    output = []
    for S in G.subgraph_search_iterator(D2, induced = False): #also considers automorphisms
        if G.degree(S[0]) + G.degree(S[4]) == 4: # also tests S[1], S[3] in another automorphism
            output.append([[S[0], S[4]], list(G.subgraph(S).edges(labels=False))]) # at least one of S[0], S[4] should have another neighbour in M 
    return output

#each subgraph K in K^{SM}_{2,4} should satisfy sum deg_M(u) >= 21
#where the sum is taken over all vertices of V(K) - {v_1, v_2}  
#(0,2),(0,3),(0,4),(0,5),(2,6),(3,7),(4,8),(5,9),(1,6),(1,7),(1,8),(1,9)
def investigate_KM4_P4s(M):
    G = copy(M)
    G = G.to_simple() # it is easier to find it without multiedges and then check
    output = []
    for S in G.subgraph_search_iterator(KM4_P4, induced = True): #also considers automorphisms
        internal_vertices = S[2:] #2,3,...,9
        if degree_sum(G, internal_vertices) == 16:
            if has_multiedge(M, (S[2],S[0])) or has_multiedge(M, (S[6],S[1])):
                if has_multiedge(M,(S[0],S[3])) or has_multiedge(M,(S[1],S[7])):
                    if has_multiedge(M,(S[0],S[4])) or has_multiedge(M,(S[1],S[8])):
                        if has_multiedge(M,(S[0],S[5])) or has_multiedge(M,(S[1],S[9])):
                            output.append([internal_vertices, S])
    return output

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