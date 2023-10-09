import time
import logging
import numpy 
from sage.all import *
from F import *
from sage.graphs.generic_graph_pyx import find_hamiltonian

logging.basicConfig(filename='hamiltonian_connectedness_certificate.py', encoding='utf-8', format='%(message)s', level=logging.INFO)
starting_time = time.time()

def find_hamiltonian_paths(G): #testing hamiltonian cycle O(n^2) times
    logging.info("paths = []")        
    n = G.order()    
    #path_matrix = numpy.zeros((n, n))    
    path_matrix = [[0] * n for i in range(n)]
    for i in range(n-1):
        for j in range(i+1, n):
            while path_matrix[i][j] == 0:
                result = find_hamiltonian(G,find_path=True)
                if result[0]: #Hamiltonian path found
                    path = result[1]     
                    if path[0] > path[-1]:
                        path.reverse()
                    path_matrix[path[0]][path[-1]] = str(path)
            logging.info("# Hamiltonian path from " + str(i) + " to " + str(j))
            logging.info("paths += [ " + path_matrix[i][j] + " ]")
    logging.info("certificate += [paths]")

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

logging.info("certificate = []")

for i in range(len(F)):
    E = F[i]
    M = graphs.CompleteGraph(1)
    M.allow_multiple_edges(True)
    M.add_edges(E)
    G = line_graph_of_multigraph(M)
    find_hamiltonian_paths(G)
    print("Multigraph", i, "with edges:", M.edges(labels=False), "gives line graph with edges:", G.edges(labels=False))
    print("Found Hamiltonian paths between all pairs of vertices. Total runtime is", get_runtime(), "seconds.")
