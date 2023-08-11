from sage.all import *
from printing import *
from manage_extensions import *
from fix_properties import *
from investigate_properties import *
from check_already_solved import *
from auxiliary_functions import *

def get_all_cycles_with_chords(n):
    if n == 10:
        C10 = graphs.CycleGraph(n)
        C10.allow_multiple_edges(True)
        C10plusChord = copy(C10)
        C10plusChord.add_edge(0, 5) #only non-isomorphic option such that no C7,C8,C9
        C10plusTwoChords = copy(C10plusChord)
        C10plusTwoChords.add_edge(1, 6) #only non-isomorphic option such that no C7,C8,C9
        C_with_chords = [C10, C10plusChord, C10plusTwoChords]
    else:
        C_with_chords = []
        for G in graphs(n):
            ok = True
            if check_D_and_H3(G) == False:
                ok = False
            elif has_subgraph(G, graphs.CycleGraph(n)) == False:
                ok = False
            else:    
                for solved in range(7, n):
                    if has_subgraph(G, graphs.CycleGraph(solved)):
                        ok = False
                        break
            if ok:
                G.relabel(cyclic_relabeling(G.subgraph_search(graphs.CycleGraph(n), induced=False)))
                G.allow_multiple_edges(True)
                C_with_chords.append(G)
    return C_with_chords

def get_all_non_empty_neighbourhoods(n):
    output = [[1]]
    for i in range(n-1):
        output = extend_list_of_neighbourhoods(output)
    return output

def investigate(MaE, case, previously_solved_cases):
    if contains_cactus9(MaE.multigraph) == False:
        solved_cases = copy(previously_solved_cases)
        choice = choose_problem_and_get_all_solution_attempts(MaE, case)  
        counter = 1
        investigated_extensions = []
        for extension in choice: # branch over all attempts on solving the chosen problem
            log_more("")    
            subcase = case + "." + str(counter)
            log_more("#", subcase, "-- extension by", attempts_as_string([extension], {0}))
            newMaE = extend(MaE, extension, investigated_extensions)
            log_more(multigraph_as_string(newMaE.multigraph))
            if is_solved_already(newMaE.multigraph, solved_cases) == False:
                investigate(newMaE, subcase, solved_cases) #recurrence
                solved_cases.append([newMaE.multigraph, subcase])
            investigated_extensions.append(extension)
            counter +=1

# run #########################################################################

print_and_log("Let's prove Lemma X.")
solved_cases = []
for k in range(7, 11):
    case = str(k - 6)
    log_more("")
    print_and_log("# Case", case, "-- we consider k =", k, "##################################################################")
    C_with_chords = get_all_cycles_with_chords(k)
    print_and_log("There are precisely", len(C_with_chords), "non-isomorphic graphs on", k, "vertices which contain a C_" + str(k))
    print_and_log("and contains neither diamond nor solved shorter cycle nor induced Gamma_3 in line graph. We investigate these graphs.")    
    all_non_empty_neighbourhoods = get_all_non_empty_neighbourhoods(k)
    counter = 1
    for C in C_with_chords:
        L = copy(all_non_empty_neighbourhoods)
        MaE = Multigraph_and_Extensions(C, L, C.edges(labels=False))
        update_extensions(MaE)
        log_more("")
        subcase = "subcase " + case + "." + str(counter)
        print_and_log("#", subcase, "##################################")
        log_more(multigraph_as_string(MaE.multigraph))
        investigate(MaE, subcase, solved_cases)
        solved_cases.append([C, subcase])
        print_and_log(subcase, "finished, total runtime =", get_runtime(), "seconds.")
        counter +=1