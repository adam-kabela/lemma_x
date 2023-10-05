from fix_properties import *

class Multigraph_and_Extensions:
  def __init__(self, multigraph, additions, multiplications, length):
    self.multigraph = multigraph
    self.additions = additions # possible additions of a new vertex while connected
    self.multiplications = multiplications # simple edges possibly extendable to multiedges
    self.length = length # length of the starting cycle

def extend(MaE, extension, investigated_extensions):
    # discard investigated_extensions since they lead to cases already solved
    non_investigated_additions = []
    for A in MaE.additions:
        if A not in investigated_extensions:
            non_investigated_additions.append(A)
    non_investigated_multiplications = []
    for e in MaE.multiplications:
        if e not in investigated_extensions:
            if e != extension: # each edge can be mutiplied at most once
                non_investigated_multiplications.append(e)
    # apply extension to multigraph
    if isinstance(extension, list): # new vertex
        newM = add_vertex_by_neighbourhood(MaE.multigraph, extension)
        newM_additions = extend_list_of_neighbourhoods(non_investigated_additions)
        newM_multiplications = non_investigated_multiplications + additional_edges(newM.order() - 1, extension)
    else: #new multiedge
        newM = copy(MaE.multigraph)
        newM.add_edge(extension)
        newM_additions = non_investigated_additions
        newM_multiplications = non_investigated_multiplications
    newMaE = Multigraph_and_Extensions(newM, newM_additions, newM_multiplications, MaE.length)
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

# all possible vertex additions while connected
def extend_list_of_neighbourhoods(L): 
    just_to_new_vertex = [0]*len(L[0]) + [1]
    output = [just_to_new_vertex]
    for N in L:
        output.append(N + [0])
        output.append(N + [1])
    return output

def discard_bad_additions(MaE):
    result = []
    for A in MaE.additions:
        Mprime = add_vertex_by_neighbourhood(MaE.multigraph, A)
        if multigraph_is_ok(Mprime, MaE.length):
            result.append(A)
    MaE.additions = result

def discard_bad_multiplications(MaE):
    result = []
    for e in MaE.multiplications:
        Mprime = copy(MaE.multigraph)
        Mprime.add_edge(e)
        if multigraph_is_ok(Mprime, MaE.length):
            result.append(e)
    MaE.multiplications = result          

def update_extensions(MaE):
    log_proof("Discarding all extensions that give diamond or Gamma_3 or C^M_9 or solved shorter cycle.")
    discard_bad_additions(MaE)
    discard_bad_multiplications(MaE)