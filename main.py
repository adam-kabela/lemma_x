from manage_cases import *

def investigate(MaE, case, previously_solved_cases):
    choice = choose_problem_and_get_all_solution_attempts(MaE, case)  
    solved_cases = copy(previously_solved_cases)
    investigated_extensions = []
    for i in range(len(choice)): # branch over all relevant solution attempts for the chosen problem
        extension = choice[i]
        newMaE = extend(MaE, extension, investigated_extensions)
        subcase = case + "." + str(i+1)        
        log_subcase(subcase, newMaE.multigraph, "-- extension by " + attempts_as_string([extension], {0}))
        if is_solved_already(newMaE.multigraph, solved_cases) == False:
            investigate(newMaE, subcase, solved_cases) # recurrence
            solved_cases.append([newMaE.multigraph, subcase])
        investigated_extensions.append(extension)

# run #########################################################################
log_intro()
solved_cases = []
for k in range(7, 11):
    starting_graphs = get_starting_graphs(k)
    case = str(k - 6)
    log_case(case, k, len(starting_graphs))     
    for i in range(len(starting_graphs)):
        C = starting_graphs[i]
        L = get_all_non_empty_neighbourhoods(k)
        MaE = Multigraph_and_Extensions(C, L, C.edges(labels=False))
        update_extensions(MaE)
        subcase = "subcase " + case + "." + str(i+1)
        log_subcase(subcase, MaE.multigraph, "")
        investigate(MaE, subcase, solved_cases) #TODO send copy?
        solved_cases.append([C, subcase])
        print_and_log_proof(subcase, "finished, total runtime is", get_runtime(), "seconds.")
        