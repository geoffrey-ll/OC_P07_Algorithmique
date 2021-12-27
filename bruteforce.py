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

def combinations_with_progression(list_fictive):
    combinations = [()]
    for action in list_fictive:
        combinations_with_action = []
        for combination in combinations:
            combinations_with_action.append(combination + (action,))
        combinations += combinations_with_action
    return combinations_with_progression.__name__, combinations



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
    results = []
    results.append(combinations_with_itertools(list_fictive))
    results.append(combinations_with_progression(list_fictive))

    for result in results:
        results_combinations(result)



main()