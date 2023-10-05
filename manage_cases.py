from manage_extensions import *

def get_starting_graphs(n):
    if n == 10:
        C10 = graphs.CycleGraph(10)
        C10.allow_multiple_edges(True)
        C10plusChord = copy(C10)
        C10plusChord.add_edge(0, 5) #only non-isomorphic option such that no C7,C8,C9
        C10plusTwoChords = copy(C10plusChord)
        C10plusTwoChords.add_edge(1, 6) #only non-isomorphic option such that no C7,C8,C9
        return [C10, C10plusChord, C10plusTwoChords] #only three graphs of order 10 contain C_10 and none of C_9, C_8, C_7 
    output = []
    for G in graphs(n): # test all graphs on n vertices
        if multigraph_is_ok(G, n): # check if graph should be investigated 
            if has_subgraph(G, graphs.CycleGraph(n)):
                G.relabel(cyclic_relabeling(G.subgraph_search(graphs.CycleGraph(n), induced=False)))
                G.allow_multiple_edges(True)
                output.append(G)
    return output
    
def get_all_non_empty_neighbourhoods(n):
    output = [[1]]
    for i in range(n-1):
        output = extend_list_of_neighbourhoods(output)
    return output

def is_solved_already(current_case, solved_cases):
    for solved in solved_cases:
        if has_flat_subgraph(current_case, solved[0]): # current contains solved[0] as a flat subgraph
            log_proof("Already solved in", solved[1]) # solved[1] is the subcase string
            return True
    return False