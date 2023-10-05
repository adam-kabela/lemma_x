import time
from sage.all import *
from itertools import combinations

starting_time = time.time()

def line_graph_of_multigraph(M): # no such function in sage, so we implement it here
    E = list(M.edges(labels=False))
    L = graphs.CompleteGraph(len(E)).complement() # graph with the right number of vertices but no edges
    for u in range(len(E) - 1):
        for v in range(u+1, len(E)):
            if len(set(E[u]).union(set(E[v]))) <= 3: # common vertex in preimage
                L.add_edge(u,v) # adjacent in line graph
    return L

#subgraph of multigraph obtained by removing some vertices and replacing some mutiedges with simple edges 
def has_flat_subgraph(host_multigraph, subgraph_searched):
    S = copy(subgraph_searched)
    S = S.to_simple()
    H = copy(host_multigraph)
    H = H.to_simple()
    for I in H.subgraph_search_iterator(S, induced=True):
        multiedges_ok = True
        #each mulitedge of subgraph_searched must be a multiedge in host_multigraph
        for e in subgraph_searched.multiple_edges(labels=False):
            if has_multiedge(host_multigraph, (I[e[0]], I[e[1]])) == False:
                multiedges_ok = False
                break
        if multiedges_ok:
            return True
    return False

def at_least_one_is_multiedge(M, E):
    for e in E:
        if has_multiedge(M, e):
            return True
    return False

def has_multiedge(M, e):
    if e in M.multiple_edges(labels=False):
        return True
    if (e[1], e[0]) in M.multiple_edges(labels=False):
        return True
    return False

def number_of_pendant_twins(M, N):
    if sum(N) > 1:
        return
    G = copy(M)
    G = G.to_simple()
    number_of_twins = 0
    n = N.index(1)
    for u in G.neighbors(n):
        if G.degree(u) == 1:
            number_of_twins += 1
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

def simple_non_pendant_edges(M):
    output = []
    for e in M.edges(labels=False):
        if M.degree(e[0]) > 1 and M.degree(e[1]) > 1: #e is not pendant
            if has_multiedge(M, e) == False: #e is simple
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
"""
def min_degree(M):
    return min([M.degree(v) for v in M.vertices()])
"""