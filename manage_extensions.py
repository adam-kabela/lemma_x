from sage.all import *
from investigate_properties import *

class Multigraph_and_Extensions:
  def __init__(self, multigraph, neighbourhoods, multiedges):
    self.multigraph = multigraph
    self.neighbourhoods = neighbourhoods #possible additions of a new vertex while connected
    self.multiedges = multiedges #edges possible extendable to multiedges

def extend(MaE, extension, investigated_extensions):
    #discard investigated_extensions since they lead to cases already solved
    non_investigated_neighbourhoods = []
    for N in MaE.neighbourhoods:
        if N not in investigated_extensions:
            non_investigated_neighbourhoods.append(N)
    non_investigated_multiedges = []
    for e in MaE.multiedges:
        if e not in investigated_extensions:
            non_investigated_multiedges.append(e)
    #apply extension on multigraph
    if isinstance(extension, list): #new vertex
        newM = add_vertex_by_neighbourhood(MaE.multigraph, extension)
        newM_neighbourhoods = extend_list_of_neighbourhoods(non_investigated_neighbourhoods)
        newM_multiedges = non_investigated_multiedges + additional_edges(newM.order() - 1, extension)
    else: #new multiedge
        newM = copy(MaE.multigraph)
        newM.add_edge(extension)
        newM_neighbourhoods = non_investigated_neighbourhoods
        newM_multiedges = non_investigated_multiedges
    newMaE = Multigraph_and_Extensions(newM, newM_neighbourhoods, newM_multiedges)
    update_extensions(newMaE)
    return newMaE 

def additional_edges(extra_vertex, N):
    output = []
    for neighbour in range(len(N)):
        if N[neighbour] == 1: 
            output.append((neighbour, extra_vertex))
    return output
    
def add_vertex_by_neighbourhood(M, N):
    Mprime = copy(M)
    extra_vertex = M.order()
    Mprime.add_vertex(extra_vertex)
    Mprime.add_edges(additional_edges(extra_vertex, N))
    return Mprime

# possible vertex extensions while connected
def extend_list_of_neighbourhoods(L):
    just_to_new_vertex = [0]*len(L[0]) + [1]
    output = [just_to_new_vertex]
    for N in L:
        output.append(N + [0])
        output.append(N + [1])
    return output
    
def discard_bad_neighbourhoods(MaE):
    result = []
    for N in MaE.neighbourhoods:
        Mprime = add_vertex_by_neighbourhood(MaE.multigraph, N)
        if check_D_and_H3(Mprime):
            result.append(N)
    MaE.neighbourhoods = result

def discard_bad_multiedges(MaE):
    result = []
    for e in MaE.multiedges:
        Mprime = copy(MaE.multigraph)
        if e not in Mprime.multiple_edges(labels=False):
            Mprime.add_edge(e)
            if check_D_and_H3(Mprime):
                result.append(e)
    MaE.multiedges = result          

def update_extensions(MaE):
    discard_bad_neighbourhoods(MaE)
    discard_bad_multiedges(MaE)        
