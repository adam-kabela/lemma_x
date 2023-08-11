import time
from sage.all import *
from itertools import combinations

starting_time = time.time()

def induces_no_multiedges(M, S):
    subM = M.subgraph(S)
    return len(subM.multiple_edges()) == 0

def line_graph_of_multigraph(M): # no such function in sage, so...
    E = list(M.edges(labels=False))
    L = graphs.CompleteGraph(len(E)).complement() # graph with right number of vertices but no edges
    for u in range(len(E) - 1):
        for v in range(u+1, len(E)):
            if len(set(E[u]).union(set(E[v]))) <= 3: # common vertex in preimage
                L.add_edge(u,v) # adjacent in line graph
    return L

# finding an (induced) submultigraph of a multigraph
# the only function I found is isomorphic_substructures_iterator documentation at
# http://www2.math.ritsumei.ac.jp/doc/static/reference/combinat/sage/combinat/designs/subhypergraph_search.html
def is_subgraph_of_multigraph(subgraph_searched, host_multigraph):
    S = IncidenceStructure(subgraph_searched.edges())
    H = IncidenceStructure(host_multigraph.edges())
    for dummy in H.isomorphic_substructures_iterator(S, induced=True):
        return True
    return False  # empty iterator means no subgraph

#induced subgraph of multigraph except the host graph may have extra multiplicities
def is_subgraph_of_multigraph_induced_in_simple(subgraph_searched, host_multigraph):
    S = copy(subgraph_searched)
    S = S.to_simple()
    H = copy(host_multigraph)
    H = H.to_simple()
    for I in H.subgraph_search_iterator(S, induced=True):
        multiedges_ok = True
        #each mulitedge of subgraph_searched must be a multiedge in host_multigraph
        for e in subgraph_searched.multiple_edges(labels=False):
            u, v = I[e[0]], I[e[1]] #e mapped to vertices u,v 
            if u < v:
                e_host = (u,v)
            else:
                e_host = (v, u)
            if e_host not in host_multigraph.multiple_edges(labels=False):
                multiedges_ok = False
                break
        if multiedges_ok:
            return True
    return False

def has_twin(M, N): # twin incident with no multiedge
    G = copy(M)
    G = G.to_simple()
    for v in G.vertices():
        if G.degree(v) == M.degree(v): # v is incident with no multiedge
            if G.degree(v) == sum(N): # same degrees
                is_twin = True
                for u in G.neighbors(v):
                    if N[u] == 0:
                        is_twin = False # N does not give a twin of v
                        break
                if is_twin:
                    return True # N gives a twin of v (same neighbourhoods)
    return False

def number_of_twins(M, N): # twin incident with no multiedge
    G = copy(M)
    G = G.to_simple()
    number_of_twins = 0
    for v in G.vertices():
        if G.degree(v) == M.degree(v): # v is incident with no multiedge
            if G.degree(v) == sum(N): # same degrees
                is_twin = True
                for u in G.neighbors(v):
                    if N[u] == 0:
                        is_twin = False # N does not give a twin of v
                        break
                if is_twin:
                    number_of_twins += 1 # N gives a twin of v (same neighbourhoods)
    return number_of_twins

def has_subgraph(host_graph, subgraph):
    if host_graph.subgraph_search(subgraph, induced=False) == None:
        return False
    return True

def degree_sum(M, V):
    return sum([M.degree(u) for u in V])

def get_nontrivial_components(M):
    output = []
    for C in M.connected_components():
        if len(C) >= 2: # component is non-trivial
            output.append(C)
    return output

def get_pairs(L):
    return list(combinations(L, 2)) 

def edges_without_diplicities(M):
    output = []
    G = copy(M)
    G = G.to_simple()
    for e in G.edges(labels=False): # give only one edge of each multiedge
        output.append(e)
    return output

def cyclic_relabeling(C): # relabel vertices of Hamiltonian graph so that it has cycle 0,1,...,n-1
    output = [0]*C.order()
    u = 0
    for i in range(1, len(output)):
        v = C.neighbors(u)[0]
        output[v] = i
        C.delete_edge(u,v)
        u = v
    return output

def random_but_probability_tweaked(n): # so that smaller numbers appear more often
    r = randint(0, (n)**2 - 1)
    index = n - 1 - int(math.sqrt(r)) #small indices have higher probability
    return index

def get_runtime():
    return round(time.time() - starting_time, 3)

def min_degree(M):
    return min([M.degree(v) for v in M.vertices()])