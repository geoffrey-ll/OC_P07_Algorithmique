import itertools as it

len_entries = 20

def create_list_fictive():
    list_fictive = []
    for i in range(1, len_entries + 1):
        list_fictive.append("action" + str(i))
    return list_fictive

def combinations_with_itertools(list_fictive):
    combinations = []

    for i in range(len(list_fictive) + 1):
        temp = it.combinations(list_fictive, i)
        for elmt in temp:
            combinations.append(elmt)

    return combinations_with_itertools.__name__, combinations

# def combinations_with_progression(list_fictive):
#     combinations = [()]
#
#     for number_of_actions in range(1, len(list_fictive) + 1):
#         actions_in_combination = []
#         idx_first = 0
#         if number_of_actions != 1:
#             idx_start = idx_first + 1
#         else:
#             idx_start = idx_first
#         idx_end = idx_first + number_of_actions - 1
#         while (idx_first + number_of_actions) < (len(list_fictive) + 1):
#             actions_in_combination.append(list_fictive[idx_first])
#
#             while idx_start < len(list_fictive):
#                 if idx_start != idx_first:
#                     while idx_end < len(list_fictive):
#                         idx = idx_start
#                         print("number_of_actions", number_of_actions)
#                         print("idx_first", idx_first)
#                         print("idx_start ", idx_start)
#                         print("idx_end ", idx_end)
#                         while idx <= idx_end:
#                             print("idx ", idx)
#                             actions_in_combination.append(list_fictive[idx])
#                             idx += 1
#                         print("actions_in_combinations ", actions_in_combination)
#                         combinations.append(tuple(actions_in_combination))
#                         actions_in_combination = [list_fictive[idx_first]]
#
#                         idx_start += 1
#                         idx_end += 1
#                     idx_start = len(list_fictive)
#                 else:
#                     idx_start = len(list_fictive)
#             if number_of_actions == 1:
#                 combinations.append(tuple(actions_in_combination))
#             actions_in_combination = []
#             idx_first += 1
#             print("intermédiare", combinations)
#     print("final", combinations)





def results_combinations(result):
    name_function = result[0]
    combinations_find = result[1]
    if len(combinations_find) <= 20:
        print(combinations_find)
        print("Soit un total de {} combinaisons trouvées avec la "
              "fonction {}".format(len(combinations_find), name_function)
              )

    else:
        print("Avec la fonction {}, {} combinaisons ont "
              "été trouvées !".format(name_function, len(combinations_find))
              )




def main():
    list_fictive = create_list_fictive()
    result_with_itertools = combinations_with_itertools(list_fictive)
    # result_with_progression = combinations_with_progression(list_fictive)
    results_combinations(result_with_itertools)



main()