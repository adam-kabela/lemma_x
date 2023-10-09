import time
import sys 
from sage.all import *
from F import *
from hamiltonian_connectedness_certificate import *

starting_time = time.time()

def verify_hamiltonian_connectedness(G, paths):
    n = G.order()    
    index = 0
    for i in range(n-1):
        for j in range(i+1, n):
            P = paths[index]
            verify_hamiltonian_path(G, P, i, j)
            index += 1    

def verify_hamiltonian_path(G, P, start, end):
    if len(P) != G.order():
        sys.exit("Wrong length.")
    if P[0] != start:
        sys.exit("Wrong start.")
    if P[-1] != end:
        sys.exit("Wrong end.")
    for k in range(len(P) - 1):
        edge = (P[k], P[k+1])
        if G.has_edge(edge) == False:
            sys.exit("Not a path.")
                
def line_graph_of_multigraph(M): # no such function in sage, so we implement it here
    E = list(M.edges(labels=False))
    L = graphs.CompleteGraph(len(E)).complement() # graph with the right number of vertices but no edges
    for u in range(len(E) - 1):
        for v in range(u+1, len(E)):
            if len(set(E[u]).union(set(E[v]))) <= 3: # common vertex in preimage
                L.add_edge(u,v) # adjacent in line graph
    return L

def get_runtime():
    return round(time.time() - starting_time, 3)

for i in range(len(F)):
    E = F[i]
    paths = certificate[i]
    M = graphs.CompleteGraph(1)
    M.allow_multiple_edges(True)
    M.add_edges(E)
    G = line_graph_of_multigraph(M)
    verify_hamiltonian_connectedness(G, paths)
    #if the graph is not Hamiltonian-connected, then the program is terminated
    print("Multigraph", i, "with edges:", M.edges(labels=False), "gives line graph with edges:", G.edges(labels=False))
    print("The line graph is Hamiltonian-connected. Total runtime is", get_runtime(), "seconds.")