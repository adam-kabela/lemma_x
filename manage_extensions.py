from fix_properties import *

class Multigraph_and_Extensions:
  def __init__(self, multigraph, additions, multiplications):
    self.multigraph = multigraph
    self.additions = additions # possible additions of a new vertex while connected
    self.multiplications = multiplications # simple edges possibly extendable to multiedges

def extend(MaE, extension, investigated_extensions):
    # discard investigated_extensions since they lead to cases already solved
    non_investigated_neighbourhoods = []
    for N in MaE.additions:
        if N not in investigated_extensions:
            non_investigated_neighbourhoods.append(N)
    non_investigated_multiedges = []
    for e in MaE.multiplications:
        if e not in investigated_extensions:
            non_investigated_multiedges.append(e)
    # apply extension on multigraph
    if isinstance(extension, list): # new vertex
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

def extend_list_of_neighbourhoods(L): # possible vertex extensions while connected
    just_to_new_vertex = [0]*len(L[0]) + [1]
    output = [just_to_new_vertex]
    for N in L:
        output.append(N + [0])
        output.append(N + [1])
    return output

def discard_bad_additions(MaE):
    result = []
    for N in MaE.additions:
        Mprime = add_vertex_by_neighbourhood(MaE.multigraph, N)
        if contains_D_or_Gamma3_or_CM9(Mprime) == False: # TODO two functions testing this?
            result.append(N)
    MaE.additions = result

def discard_bad_multiplications(MaE):
    result = []
    for e in MaE.multiplications:
        Mprime = copy(MaE.multigraph)
        if e not in Mprime.multiple_edges(labels=False):
            Mprime.add_edge(e)
            if contains_D_or_Gamma3_or_CM9(Mprime) == False:
                result.append(e)
    MaE.multiplications = result          

def update_extensions(MaE):
    log_proof("Discarding all extensions that give diamond or Gamma_3 or C^M_9:") # TODO
    discard_bad_additions(MaE)
    discard_bad_multiplications(MaE)
